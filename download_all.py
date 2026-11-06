import json, os, subprocess, sys, urllib.request

ROOT = os.path.expanduser("~/projects/fault_detection/data")
os.makedirs(ROOT + "/_direct_downloads", exist_ok=True)
failed = []

def fetch(url, dest, expected=None):
    if expected and os.path.exists(dest) and os.path.getsize(dest) == expected:
        print("SKIP (done):", dest, flush=True)
        return True
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    part = dest + ".part"
    if expected and os.path.exists(part) and os.path.getsize(part) == expected:
        os.replace(part, dest)
        return True
    cmd = ["curl", "-fL", "-C", "-", "--retry", "10", "--retry-delay", "5",
           "--retry-all-errors", "-o", part, url]
    if "dataverse" in url:
        cmd[1:1] = ["-A", "Mozilla/5.0"]
    if subprocess.call(cmd) != 0:
        print("FAILED:", dest, flush=True)
        return False
    if expected and os.path.getsize(part) != expected:
        print("SIZE MISMATCH:", dest, flush=True)
        return False
    os.replace(part, dest)
    print("DONE:", dest, flush=True)
    return True

print("=== CRACKS ===", flush=True)
rec = json.load(urllib.request.urlopen("https://zenodo.org/api/records/11559387"))
for f in rec["files"]:
    if not fetch(f["links"]["self"], ROOT + "/cracks/" + f["key"], f["size"]):
        failed.append("cracks/" + f["key"])

print("=== FaultSeg3D ===", flush=True)
FS_URL = "https://drive.google.com/drive/folders/1FcykAxpqiy2NpLP1icdatrrSQgLRXLP8"
rc = subprocess.call([sys.executable, "-m", "gdown", "--folder", FS_URL, "-O", ROOT + "/faultseg3d"])
if rc != 0:
    failed.append("faultseg3d (gdown)")

print("=== Thebe ===", flush=True)
meta = ROOT + "/_direct_downloads/thebe_metadata.json"
if not os.path.exists(meta):
    fetch("https://dataverse.harvard.edu/api/datasets/:persistentId/?persistentId=doi:10.7910/DVN/YBYGBK", meta)
files = json.load(open(meta, encoding="utf-8"))["data"]["latestVersion"]["files"]
for item in files:
    last = (item.get("directoryLabel") or "").strip("/").split("/")[-1]
    if last not in ("seis", "fault"):
        continue
    df = item["dataFile"]
    url = "https://dataverse.harvard.edu/api/access/datafile/" + str(df["id"])
    if not fetch(url, ROOT + "/thebe/" + last + "/" + df["filename"], df["filesize"]):
        failed.append("thebe/" + last + "/" + df["filename"])

print("=== SUMMARY ===")
print("FAILED:", failed if failed else "none")
subprocess.call("du -sh " + ROOT + "/*/", shell=True)
print("ALL FINISHED", flush=True)
