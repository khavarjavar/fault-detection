import json, os, time, glob
R = os.path.expanduser("~/projects/fault_detection/data")
meta = json.load(open(R + "/_direct_downloads/thebe_metadata.json", encoding="utf-8"))["data"]["latestVersion"]["files"]
exp = []
for it in meta:
    last = (it.get("directoryLabel") or "").strip("/").split("/")[-1]
    if last in ("seis", "fault"):
        exp.append((R + "/thebe/" + last + "/" + it["dataFile"]["filename"], it["dataFile"]["filesize"], last))
def got():
    t = 0
    for p, s, g in exp:
        if os.path.exists(p): t += os.path.getsize(p)
        elif os.path.exists(p + ".part"): t += os.path.getsize(p + ".part")
    return t
tot = sum(s for p, s, g in exp)
b0 = got(); time.sleep(10); b1 = got()
GiB = 1024**3
print("=== THEBE ===")
for grp in ("seis", "fault"):
    items = [(p, s) for p, s, g in exp if g == grp]
    n = sum(1 for p, s in items if os.path.exists(p) and os.path.getsize(p) == s)
    print(grp + ": " + str(n) + "/" + str(len(items)) + " files complete")
print("downloaded: %.2f of %.2f GiB (%.1f%%)" % (b1 / GiB, tot / GiB, 100 * b1 / tot))
sp = (b1 - b0) / 10
print("speed now: %.2f MB/s" % (sp / 1e6))
print("time left: about %.1f hours" % ((tot - b1) / sp / 3600) if sp > 0 else "time left: no progress in 10s (check process)")
print("=== FAULTSEG3D ===")
F = R + "/faultseg3d"
print("validation seis/fault:", len(glob.glob(F + "/validation/seis/*.dat")), "/", len(glob.glob(F + "/validation/fault/*.dat")), "(want 20/20)")
print("train fault.zip present:", os.path.exists(F + "/train/fault.zip"))
print("train seis files found:", len(glob.glob(F + "/train/**/seis/*.dat", recursive=True)), "(want 200, after upload)")
print("=== CRACKS ===", sorted(os.listdir(R + "/cracks")))
