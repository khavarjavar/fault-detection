import gdown
r = gdown.download_folder(url="https://drive.google.com/drive/folders/1FcykAxpqiy2NpLP1icdatrrSQgLRXLP8", skip_download=True, quiet=False)
print("FILES FOUND:", len(r))
for f in r[:8]:
    print(f.path)
