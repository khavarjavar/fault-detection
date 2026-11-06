# Attention3D NZP&M dataset match (2026-10-21)

## Decision

Download the processed **PSTM** products for Opunake PR3461 and Kahu PR3177. Do not download a Kerry catalogue product yet if exact reproduction is the goal.

The paper confirms that pretext training used three post-stack 3D surveys—Kerry-3D, Opunake-3D, and Kahu-3D—but it does not publish the SEG-Y filenames. The public GitHub repositories name the surveys but contain no download manifest, SEG-Y conversion code, crop bounds, or pretrained weights.

## Product mapping

| Survey | Historical public volume | Current NZP&M match | Size | Confidence | Action |
|---|---|---|---:|---|---|
| Opunake | `OPUNAKE3D-PR3461-FS.3D.Final_Stack.sgy` | `OPUNAKE-3D-PR3461-T-PSTM`, resource `8ecd25f5-522f-59da-bcef-6c4f9d6d03c3` | 9.67 GB | High | Download |
| Kahu | `KAHU-3D-PR3177-FM.3D.Final_Migration.sgy` | `KAHU-3D-PR3177-T-PSTM-FULL`, resource `f2366d42-a04e-5aca-bcf0-9d07f6f0d27a` | 5.78 GiB | High | Downloaded and structurally verified |
| Kerry | `Kerry3D.segy` | No proven identical current resource | about 1 GB | Target identified; source unresolved | Wait for exact source or author confirmation |
| Kerry candidate | unknown | `KERRY-3D-PR4184-FS`, resource `e3f8885f-a7e1-5666-958b-8355bec72d97` | 13.35 GB | Candidate only | Do not download by default |

Official records:

- Opunake PR3461: <https://geodata.nzpam.govt.nz/survey/78683ccd-4fb8-5eff-98fe-e5b04358450d>
- Kahu PR3177: <https://geodata.nzpam.govt.nz/survey/80d2c7f4-ae54-57ed-bfc7-5a08ae48099e>
- Kerry original acquisition PR1556: <https://geodata.nzpam.govt.nz/survey/54a5a5ab-b437-5d3e-b960-fe1415f73383>
- Kerry reprocessing PR4184: <https://geodata.nzpam.govt.nz/survey/fcb71940-67a7-5b98-876d-75d05d82a3b3>

## Why these files

Opunake's historical file is called `Final_Stack`; the current catalogue offers a processed PSTM and a Raw PSTM of almost the same size. A post-stack pretraining volume maps to the processed PSTM, not the raw product.

Kahu's historical file is called `Final_Migration`; the current catalogue offers `PSTM-FULL`, Raw PSTM, angle stacks, PSDM products, and velocity data. The full processed PSTM is the direct match to a post-stack time-migrated volume.

Kerry is not resolved by choosing the largest or newest entry. The canonical ML/open-geoscience cube `Kerry3D.segy` is described by SEG as an approximately 1 GB time-migrated volume and is reported elsewhere as `287 x 735 x 1252`. The current PR4184 Final Stack is 13.35 GB. PR1556 exposes a 14.35 GB Raw Migration rather than a final post-stack volume. Neither has been demonstrated to be the authors' approximately 1 GB cube. The historical S3 object currently returns HTTP 403.

## Downloader

Use `scripts/download_nzpam_pretraining.py`. It defaults to Opunake and Kahu, resumes partial transfers, downloads directly into the workspace, rejects or quarantines short error/challenge responses, and gives an NZP&M-packaged payload a `.zip` suffix instead of mislabelling it as SEG-Y.

RealMe is an interactive SAML flow and NZP&M applies human verification, so a username/password file is not supported. Log in in a browser and export a short-lived Netscape-format cookie file to `~/.config/nzpam/cookies.txt`, then protect it with `chmod 600`.

An easier alternative is to use the browser only to create the authorized links:

1. Sign in to NZP&M with RealMe.
2. Open each exact record and click the exact product named in the table.
3. Complete human verification. Once the browser download begins, cancel it.
4. In the browser's Downloads page or Developer Tools Network panel, copy the fresh final download URL.
5. Copy `configs/nzpam_download_urls.example.json` to a private file and paste the two URLs there. Run the workspace downloader immediately because ticket/signed URLs can expire.

The private JSON file has this form:

```json
{
  "opunake": "https://...",
  "kahu": "https://..."
}
```

```bash
mkdir -p ~/.config/nzpam
cp configs/nzpam_download_urls.example.json ~/.config/nzpam/download_urls.json
chmod 600 ~/.config/nzpam/download_urls.json
# Edit the two empty strings, then:
python scripts/download_nzpam_pretraining.py \
  --direct-url-file ~/.config/nzpam/download_urls.json \
  --download
```

Plan only:

```bash
cd /shared/home/khavarj/projects/fault_detection
python scripts/download_nzpam_pretraining.py --list
```

Download the two high-confidence matches:

```bash
cd /shared/home/khavarj/projects/fault_detection
chmod 600 ~/.config/nzpam/cookies.txt
python scripts/download_nzpam_pretraining.py --download
```

The 355 KB file previously named `data/raw/nz_pretraining/ACTUAL_FILENAME.sgy` was a catalogue HTML page, not SEG-Y data. It has been renamed to `data/raw/nz_pretraining/FAILED_DOWNLOAD_PAGE.html`.

## Retrieval status (2026-10-21)

### Kahu completion update (2026-10-26)

Kahu `KAHU-3D-PR3177-T-PSTM-FULL` was downloaded through the browser and moved
to `data/raw/nz_pretraining/kahu/KAHU-3D-PR3177-T-PSTM-FULL.sgy`. The file is
6,203,998,800 bytes and its local SHA-256 integrity baseline is
`079826f39ea6e29b34accd4342e1d2e7fb5fea079a7dc06a74b1d3a4d525b225`.

The SEG-Y audit resolves exactly to 994,230 fixed-length traces with 1,500 IBM
float samples per trace, a 4 ms interval, and zero trailing bytes. Its textual
header identifies `KAHU 3D` and `ZERO PHASE FILTERED AND SCALED MIGRATION (FULL
ANGLE)`. Geometry comprises 599 inlines (996–1594) and 1,697 crosslines
(1008–4400 at step 2), with 994,230 unique pairs and no duplicate coordinates.
The footprint contains 22,273 unoccupied cells inside its rectangular envelope,
so readers must permit irregular/unstructured geometry and use the vendor fields
at inline byte 181 and crossline byte 185. The machine-readable audit is stored
beside the volume as `KAHU-3D-PR3177-T-PSTM-FULL.sgy.audit.json`.

The failed 1.7 GB `.part` and its HTML verification response were deleted after
the completed volume passed this audit.

The private direct-URL file contains correctly formed `/fpx/ticket/<uuid>/download` URLs for Opunake and Kahu and has mode `0600`. A header-only request from the workspace returned HTTP 404 for both tickets. A second fresh Opunake ticket also returned the same 36-byte JSON 404 when sent with the visible load-balancer session cookie. No large transfer was started. The evidence indicates that `/fpx/ticket/.../download` is a one-use handoff: the browser consumes it while following the redirect, so copying that ticket afterward is too late.

Generate a fresh ticket with Developer Tools Network recording, then copy the `Location` response header from the successful ticket response or the subsequent final storage-object request URL. It should be a long signed URL rather than another `/fpx/ticket/.../download` URL. Cancel the browser transfer only after the final object request appears, and paste that final URL into the downloader immediately. Keep Kerry disabled.

If the fresh ticket works only in the logged-in browser, open Developer Tools, select the ticket request, and copy the value of its `Cookie` request header. Then run:

```bash
cd /shared/home/khavarj/projects/fault_detection
python3 scripts/download_nzpam_pretraining.py \
  --prompt-direct-urls \
  --prompt-cookie-header \
  --download
```

Paste the fresh Opunake URL, fresh Kahu URL, and Cookie value at the three hidden prompts. The downloader sends the Cookie value to `curl` over standard input; none of these session values is written to disk, shell history, or process arguments.

An email was sent to both corresponding authors, Matin Mahzad and Majid Bagheri, asking them to confirm the exact filenames, stable NZP&M product/resource IDs or source URLs, byte sizes, checksums, loaded dimensions, and any preprocessing for all three surveys. The message specifically documents the ambiguity between the roughly 1 GB historical `Kerry3D.segy`, the PR1556 selection reported by the portal as 46.97 GB, and the PR4184 selection reported as 158 GB.
