#!/usr/bin/env python3
"""Download the NZP&M survey products selected for Attention3D pretraining.

RealMe is an interactive SAML login and NZP&M also presents a human-verification
challenge.  Consequently this script never accepts or stores a RealMe username
or password.  Log in with a browser, solve the challenge, and either:

1. export the geodata.nzpam.govt.nz cookies in Netscape cookies.txt format;
2. paste each final download URL into a hidden terminal prompt or a private
   JSON file; or
3. paste the browser request's Cookie header into a hidden terminal prompt.

The script resumes partial transfers, rejects HTML challenge/login pages, and
keeps the uncertain 13.35 GB Kerry PR4184 product disabled unless explicitly
requested.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import getpass
import json
import shutil
import subprocess
import sys
import threading
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse


BASE_URL = "https://geodata.nzpam.govt.nz"
DEFAULT_OUTPUT = (
    Path(__file__).resolve().parents[1] / "data" / "raw" / "nz_pretraining"
)
DEFAULT_COOKIES = Path("~/.config/nzpam/cookies.txt").expanduser()
PRINT_LOCK = threading.Lock()


@dataclass(frozen=True)
class Product:
    key: str
    survey: str
    product: str
    record_url: str
    download_url: str | None
    output_name: str
    expected_gb: float
    confidence: str
    note: str


PRODUCTS = {
    "opunake": Product(
        key="opunake",
        survey="Opunake 3D / PR3461",
        product="Seismic Project - PSTM (OPUNAKE-3D-PR3461-T-PSTM)",
        record_url=f"{BASE_URL}/survey/78683ccd-4fb8-5eff-98fe-e5b04358450d",
        download_url=(
            f"{BASE_URL}/dataset/78683ccd-4fb8-5eff-98fe-e5b04358450d/"
            "resource/8ecd25f5-522f-59da-bcef-6c4f9d6d03c3/fpx"
        ),
        output_name="OPUNAKE-3D-PR3461-T-PSTM.sgy",
        expected_gb=9.67,
        confidence="high",
        note=(
            "Current processed PSTM counterpart of the historical public "
            "Final_Stack volume; do not select Raw PSTM."
        ),
    ),
    "kahu": Product(
        key="kahu",
        survey="Kahu 3D / PR3177",
        product="Seismic Project - PSTM (KAHU-3D-PR3177-T-PSTM-FULL)",
        record_url=f"{BASE_URL}/survey/80d2c7f4-ae54-57ed-bfc7-5a08ae48099e",
        download_url=(
            f"{BASE_URL}/dataset/80d2c7f4-ae54-57ed-bfc7-5a08ae48099e/"
            "resource/f2366d42-a04e-5aca-bcf0-9d07f6f0d27a/fpx"
        ),
        output_name="KAHU-3D-PR3177-T-PSTM-FULL.sgy",
        expected_gb=5.78,
        confidence="high",
        note=(
            "Full processed PSTM counterpart of the historical public "
            "Final_Migration volume; do not select Raw PSTM or angle stacks."
        ),
    ),
    "kerry": Product(
        key="kerry",
        survey="Kerry 3D canonical public cube",
        product="Kerry3D.segy",
        record_url="https://wiki.seg.org/wiki/Kerry-3D",
        download_url=None,
        output_name="Kerry3D.segy",
        expected_gb=1.0,
        confidence="target identified; current source unresolved",
        note=(
            "The historical public object is approximately 1 GB (reported cube "
            "287 x 735 x 1252), but its old S3 URL currently returns HTTP 403. "
            "No current NZP&M resource has been proven identical."
        ),
    ),
    "kerry-pr4184": Product(
        key="kerry-pr4184",
        survey="Kerry 3D reprocessing / PR4184",
        product="Seismic Project - Final Stack (KERRY-3D-PR4184-FS)",
        record_url=f"{BASE_URL}/survey/fcb71940-67a7-5b98-876d-75d05d82a3b3",
        download_url=(
            f"{BASE_URL}/dataset/fcb71940-67a7-5b98-876d-75d05d82a3b3/"
            "resource/e3f8885f-a7e1-5666-958b-8355bec72d97/fpx"
        ),
        output_name="KERRY-3D-PR4184-FS.sgy",
        expected_gb=13.35,
        confidence="candidate only",
        note=(
            "Only current catalogue product explicitly called Final Stack. It "
            "is not proven equivalent to the authors' canonical Kerry3D.segy."
        ),
    ),
}


def eprint(message: str) -> None:
    with PRINT_LOCK:
        print(message, file=sys.stderr, flush=True)


def show_product(product: Product) -> None:
    endpoint = product.download_url or "UNRESOLVED"
    print(f"{product.key}: {product.survey}")
    print(f"  product:    {product.product}")
    print(f"  catalogue:  {product.record_url}")
    print(f"  endpoint:   {endpoint}")
    print(f"  output:     {product.output_name}")
    print(f"  listed size:{product.expected_gb:>7.2f} GB")
    print(f"  confidence: {product.confidence}")
    print(f"  note:       {product.note}")


def load_direct_urls(path: Path | None) -> dict[str, str]:
    if path is None:
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"Cannot read direct URL file {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise SystemExit("The direct URL file must contain one JSON object.")

    urls: dict[str, str] = {}
    for key, value in payload.items():
        if key not in PRODUCTS:
            raise SystemExit(f"Unknown dataset key in {path}: {key!r}")
        if not isinstance(value, str) or urlparse(value).scheme != "https":
            raise SystemExit(f"Direct URL for {key!r} must be an https URL.")
        urls[key] = value
    return urls


def looks_like_html(path: Path) -> bool:
    with path.open("rb") as handle:
        prefix = handle.read(8192).lower()
    markers = (
        b"<!doctype html",
        b"<html",
        b"human verification challenge",
        b"login with realme",
        b"accessdenied",
        b"<error>",
    )
    return any(marker in prefix for marker in markers)


def is_zip(path: Path) -> bool:
    with path.open("rb") as handle:
        return handle.read(4) in (b"PK\x03\x04", b"PK\x05\x06", b"PK\x07\x08")


def cookie_header_has(cookie_header: str | None, name: str) -> bool:
    """Check for a cookie name without logging or otherwise exposing values."""
    if not cookie_header:
        return False
    wanted = name.casefold()
    for item in cookie_header.split(";"):
        cookie_name, separator, _ = item.strip().partition("=")
        if separator and cookie_name.casefold() == wanted:
            return True
    return False


def quarantine_bad_partial(part_path: Path) -> Path | None:
    """Move a tiny error body or HTML response aside so it cannot be resumed."""
    if not part_path.exists():
        return None
    if part_path.stat().st_size >= 1_000_000 and not looks_like_html(part_path):
        return None
    rejected_path = part_path.with_name(part_path.name + ".rejected")
    rejected_path.unlink(missing_ok=True)
    part_path.replace(rejected_path)
    return rejected_path


def download_one(
    product: Product,
    output_root: Path,
    cookie_file: Path | None,
    cookie_header: str | None,
    user_agent: str,
    direct_url: str | None,
    restart: bool,
) -> tuple[str, bool, str]:
    dataset_dir = output_root / product.key
    dataset_dir.mkdir(parents=True, exist_ok=True)
    final_path = dataset_dir / product.output_name
    zip_path = final_path.with_suffix(".zip")
    part_path = final_path.with_name(final_path.name + ".part")
    headers_path = final_path.with_name(final_path.name + ".headers")

    if not restart:
        for candidate in (final_path, zip_path):
            if candidate.exists():
                if candidate.stat().st_size >= 100_000_000 and not looks_like_html(candidate):
                    return product.key, True, f"already present: {candidate}"
                return (
                    product.key,
                    False,
                    f"existing output is too small or HTML: {candidate}; "
                    "use --restart after inspection",
                )

    if restart:
        for stale in (part_path, headers_path):
            stale.unlink(missing_ok=True)
    else:
        rejected = quarantine_bad_partial(part_path)
        if rejected is not None:
            eprint(f"[{product.key}] quarantined invalid partial response as {rejected}")

    url = direct_url or product.download_url
    if url is None:
        return product.key, False, "no working source URL is known"

    command = [
        "curl",
        "--fail-with-body",
        "--location",
        "--retry",
        "8",
        "--retry-delay",
        "5",
        "--connect-timeout",
        "30",
        "--speed-time",
        "120",
        "--speed-limit",
        "1024",
        "--continue-at",
        "-",
        "--dump-header",
        str(headers_path),
        "--output",
        str(part_path),
        "--referer",
        product.record_url,
        "--user-agent",
        user_agent,
    ]
    if cookie_file is not None:
        command.extend(("--cookie", str(cookie_file)))
    if cookie_header is not None:
        # curl reads this header from stdin. The session cookie therefore does
        # not appear in shell history, the process list, or a project file.
        command.extend(("--header", "@-"))
    command.append(url)

    eprint(f"[{product.key}] downloading to {part_path}")
    header_input = (
        f"Cookie: {cookie_header}\n".encode("utf-8")
        if cookie_header is not None
        else None
    )
    result = subprocess.run(command, check=False, input=header_input)
    if result.returncode != 0:
        rejected = quarantine_bad_partial(part_path)
        detail = (
            f"invalid response saved as {rejected}"
            if rejected is not None
            else "large partial file kept for resumption"
        )
        return product.key, False, f"curl exited with status {result.returncode}; {detail}"
    if not part_path.exists():
        return product.key, False, "curl reported success but created no file"
    if looks_like_html(part_path):
        challenge_path = part_path.with_name(part_path.name + ".html")
        part_path.replace(challenge_path)
        if not cookie_header_has(cookie_header, "RS_CHALLENGE_COOKIE"):
            reason = (
                "the pasted Cookie value did not include RS_CHALLENGE_COOKIE; "
                "solve Human Verification in the browser, then copy the full "
                "Cookie value from the subsequent authenticated /fpx request"
            )
        else:
            reason = (
                "NZP&M rejected RS_CHALLENGE_COOKIE; it may have expired or may "
                "be bound to the browser's network address/session/User-Agent"
            )
        return (
            product.key,
            False,
            f"NZP&M returned the Human Verification page: {reason} "
            f"(saved as {challenge_path})",
        )

    # All selected SGY products are at least 1 GB. This catches short error pages
    # and expired-ticket responses while allowing differences in GB/GiB display.
    minimum_size = max(500_000_000, int(product.expected_gb * 1_000_000_000 * 0.70))
    actual_size = part_path.stat().st_size
    if actual_size < minimum_size:
        return (
            product.key,
            False,
            f"download is unexpectedly small ({actual_size:,} bytes); partial file kept",
        )

    resolved_path = zip_path if is_zip(part_path) else final_path
    part_path.replace(resolved_path)
    payload_kind = "ZIP package" if resolved_path == zip_path else "SEG-Y candidate"
    return (
        product.key,
        True,
        f"complete {payload_kind}: {resolved_path} ({actual_size:,} bytes)",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Safely download the matched NZP&M Attention3D pretraining volumes."
    )
    parser.add_argument(
        "--datasets",
        nargs="+",
        choices=tuple(PRODUCTS),
        default=("opunake", "kahu"),
        help="Products to plan/download (default: opunake kahu).",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"Destination root (default: {DEFAULT_OUTPUT}).",
    )
    parser.add_argument(
        "--cookies",
        type=Path,
        default=DEFAULT_COOKIES,
        help=(
            "Netscape-format browser cookie export. Default: "
            f"{DEFAULT_COOKIES}"
        ),
    )
    parser.add_argument(
        "--direct-url-file",
        type=Path,
        help=(
            "JSON mapping dataset keys to fresh final browser download URLs. "
            "These override catalogue endpoints."
        ),
    )
    parser.add_argument(
        "--prompt-direct-urls",
        action="store_true",
        help=(
            "Prompt invisibly for a fresh browser download URL for each selected "
            "dataset. This avoids saving ticket URLs or placing them in shell history."
        ),
    )
    parser.add_argument(
        "--prompt-cookie-header",
        action="store_true",
        help=(
            "Prompt invisibly for the Cookie request-header value copied from "
            "the authenticated browser. The value is sent to curl over stdin "
            "and is not saved or placed in the process arguments."
        ),
    )
    parser.add_argument(
        "--prompt-user-agent",
        action="store_true",
        help=(
            "Prompt for the User-Agent request-header value from the same "
            "authenticated browser request. Use with --prompt-cookie-header "
            "when verification may bind cookies to browser identity."
        ),
    )
    parser.add_argument(
        "--download",
        action="store_true",
        help="Start transfers. Without this flag the script only prints the plan.",
    )
    parser.add_argument(
        "--accept-kerry-pr4184",
        action="store_true",
        help="Acknowledge that kerry-pr4184 is an unconfirmed 13.35 GB candidate.",
    )
    parser.add_argument(
        "--jobs",
        type=int,
        default=2,
        help="Concurrent transfers (default: 2, so fresh challenge cookies are used promptly).",
    )
    parser.add_argument(
        "--restart",
        action="store_true",
        help="Discard partial/header files for selected products and start again.",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="Show every known match, including unresolved/candidate Kerry entries.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.jobs < 1:
        raise SystemExit("--jobs must be at least 1")

    if args.list:
        for index, product in enumerate(PRODUCTS.values()):
            if index:
                print()
            show_product(product)
        if not args.download:
            return 0

    selected = [PRODUCTS[key] for key in dict.fromkeys(args.datasets)]
    if any(item.key == "kerry-pr4184" for item in selected) and not args.accept_kerry_pr4184:
        raise SystemExit(
            "Refusing the unconfirmed Kerry PR4184 candidate. Re-run with "
            "--accept-kerry-pr4184 only if you intentionally want that 13.35 GB product."
        )

    print("Selected download plan:")
    for product in selected:
        print(
            f"  {product.key:14s} {product.expected_gb:5.2f} GB  "
            f"{product.product}  [{product.confidence}]"
        )
    print(f"Destination: {args.output_dir.resolve()}")

    direct_urls = load_direct_urls(args.direct_url_file)
    if args.prompt_direct_urls:
        if not args.download:
            print("Fresh direct URLs will be requested when --download is used.")
        else:
            for product in selected:
                value = getpass.getpass(
                    f"Paste fresh {product.key} browser download URL (input hidden): "
                ).strip()
                parsed = urlparse(value)
                if parsed.scheme != "https" or not parsed.hostname:
                    raise SystemExit(
                        f"The direct URL supplied for {product.key} is not a valid https URL."
                    )
                direct_urls[product.key] = value
    unresolved = [p.key for p in selected if p.download_url is None and p.key not in direct_urls]
    if unresolved:
        raise SystemExit(
            "No current source URL is known for: "
            + ", ".join(unresolved)
            + ". Supply a verified URL with --direct-url-file."
        )

    cookie_header: str | None = None
    if args.prompt_cookie_header:
        if not args.download:
            print("Browser Cookie header will be requested when --download is used.")
        else:
            cookie_header = getpass.getpass(
                "Paste the browser Cookie request-header value (input hidden): "
            ).strip()
            if cookie_header.lower().startswith("cookie:"):
                cookie_header = cookie_header.split(":", 1)[1].strip()
            if not cookie_header or "\n" in cookie_header or "\r" in cookie_header:
                raise SystemExit("The Cookie header value is empty or invalid.")

    user_agent = "Mozilla/5.0 NZPAM-workspace-downloader/1.0"
    if args.prompt_user_agent:
        if not args.download:
            print("Browser User-Agent will be requested when --download is used.")
        else:
            user_agent = input(
                "Paste the User-Agent value from the same browser request: "
            ).strip()
            if user_agent.lower().startswith("user-agent:"):
                user_agent = user_agent.split(":", 1)[1].strip()
            if not user_agent or "\n" in user_agent or "\r" in user_agent:
                raise SystemExit("The User-Agent value is empty or invalid.")
            parsed_user_agent = urlparse(user_agent)
            if (
                parsed_user_agent.scheme in {"http", "https"}
                and parsed_user_agent.hostname
            ):
                raise SystemExit(
                    "A download/ticket URL was pasted as the User-Agent. "
                    "In browser DevTools, open the same request, then copy "
                    "Request Headers -> user-agent (normally starts with Mozilla/5.0)."
                )

    endpoint_keys = [p.key for p in selected if p.key not in direct_urls]
    if args.prompt_direct_urls and not args.download:
        endpoint_keys = []
    cookie_file: Path | None = None
    candidate_cookie_file = args.cookies.expanduser()
    if endpoint_keys and cookie_header is None:
        cookie_file = candidate_cookie_file
        if not args.download:
            print(f"Cookie file required for catalogue endpoints: {cookie_file}")
        elif not cookie_file.is_file():
            raise SystemExit(
                f"Cookie file not found: {cookie_file}\n"
                "Log in to NZP&M with RealMe in your browser, complete the human "
                "verification challenge, and export geodata.nzpam.govt.nz cookies "
                "in Netscape cookies.txt format. Keep the file private with chmod 600."
            )
        elif cookie_file.stat().st_mode & 0o077:
            raise SystemExit(
                f"Cookie file permissions are too open: {cookie_file}\n"
                f"Run: chmod 600 {cookie_file}"
            )
    elif cookie_header is None and candidate_cookie_file.is_file():
        # A copied browser URL may still point to an authenticated FPX ticket.
        # Send the cookie export when it is available, even though a direct URL
        # has replaced every catalogue endpoint.
        if candidate_cookie_file.stat().st_mode & 0o077:
            raise SystemExit(
                f"Cookie file permissions are too open: {candidate_cookie_file}\n"
                f"Run: chmod 600 {candidate_cookie_file}"
            )
        cookie_file = candidate_cookie_file

    if not args.download:
        print("Dry run only. Add --download after supplying fresh cookies or direct URLs.")
        return 0

    if shutil.which("curl") is None:
        raise SystemExit("curl is required but was not found in PATH")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    required = int(sum(p.expected_gb for p in selected) * 1_000_000_000 * 1.05)
    available = shutil.disk_usage(args.output_dir).free
    if available < required:
        raise SystemExit(
            f"Insufficient free space: need about {required / 1e9:.1f} GB, "
            f"have {available / 1e9:.1f} GB"
        )

    failures = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as executor:
        futures = [
            executor.submit(
                download_one,
                product,
                args.output_dir,
                cookie_file,
                cookie_header,
                user_agent,
                direct_urls.get(product.key),
                args.restart,
            )
            for product in selected
        ]
        for future in concurrent.futures.as_completed(futures):
            key, ok, message = future.result()
            print(f"[{key}] {'OK' if ok else 'FAILED'}: {message}", flush=True)
            failures += int(not ok)

    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
