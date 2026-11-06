import json, os, subprocess
ROOT = os.path.expanduser("~/projects/fault_detection/data/faultseg3d/validation")
API = "https://api.github.com/repos/xinwucwp/faultSeg/contents/data/validation/"
for sub in ("seis", "fault"):
    os.makedirs(ROOT + "/" + sub, exist_ok=True)
    out = subprocess.check_output(["curl", "-sS", "-m", "60", API + sub])
    for item in json.loads(out):
        dest = ROOT + "/" + sub + "/" + item["name"]
        if os.path.exists(dest) and os.path.getsize(dest) == item["size"]:
            print("SKIP", dest); continue
        rc = subprocess.call(["curl", "-fsS", "-m", "300", "--retry", "5", "-H", "Accept: application/vnd.github.raw", "-o", dest, item["url"]])
        ok = rc == 0 and os.path.getsize(dest) == item["size"]
        print("OK  " if ok else "FAIL", dest, flush=True)
