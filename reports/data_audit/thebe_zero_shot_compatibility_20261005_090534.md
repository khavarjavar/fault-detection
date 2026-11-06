# Thebe Zero-Shot Compatibility Audit

- Project: `/home/khavarj/projects/fault_detection`
- Source log: `reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.log`
- Generated: 2026-10-05T09:10:27+04:00

## Complete audit output

    === PROJECT ===
    /home/khavarj/projects/fault_detection
    Mon Oct  5 09:05:34 AM +04 2026
    
    === BASELINE A CHECKPOINT ===
    -rw-rw-r-- 1 khavarj khavarj 17M Sep 30 18:59 runs/baseline_A_synthetic_bce_seed42/best.pt
    
    === BASELINE A FINAL METRICS ===
    -rw-rw-r-- 1 khavarj khavarj 6.9K Sep 30 19:00 runs/baseline_A_synthetic_bce_seed42/final_metrics.json
    
    === THEBE DIRECTORY SIZES ===
    21G	data/thebe
    17G	data/processed/thebe_h5
    32K	data/manifests
    136K	reports/data_audit
    
    === THEBE FILE INVENTORY ===
    
    ROOT: data/thebe
      total files: 37
      extensions:
        .json: 1
        .npz: 36
      files by directory:
        data/thebe: 1
          metadata.json
        data/thebe/fault: 18
          faulttest1.npz
          faulttest2.npz
          faultval1.npz
          faultval2.npz
        data/thebe/seis: 18
          seistest1.npz
          seistest2.npz
          seisval1.npz
          seisval2.npz
    
    ROOT: data/processed/thebe_h5
      total files: 18
      extensions:
        .h5: 18
      files by directory:
        data/processed/thebe_h5: 18
          test1.h5
          test2.h5
          val1.h5
          val2.h5
    
    TOTAL THEBE FILES FOUND: 55
    
    === EXISTING THEBE AUDIT REPORTS ===
    
    --- reports/data_audit/thebe_h5_statistics.csv ---
    split,shape,source_seismic_dtype,source_fault_dtype,output_seismic_dtype,output_fault_dtype,seismic_min,seismic_max,seismic_mean,seismic_std,fault_positive_count,total_voxels,fault_positive_pct,source_seismic_sha256,source_fault_sha256,source_seismic_path,source_fault_path,output_path,output_bytes
    train,100x3174x1537,float64,bool,float32,uint8,-2.789945602416992,3.0317649841308594,-1.4305969246317352e-05,0.09593104272920336,5477591,487843800,1.1228165654662414,43e21d81dd46fe4cf398fb6b22f4fde8acf963ff247dcf5e5583fc11538a89af,de7cb1337c12fb2fdcd35aeb1a064f073e43e71ad5a4c588a509e7ec85cb6fc3,data/thebe/seis/seistrain1.npz,data/thebe/fault/faulttrain1.npz,data/processed/thebe_h5/train1.h5,717073164
    train,100x3174x1537,float64,bool,float32,uint8,-2.3829421997070312,2.607198715209961,-1.0810308912158474e-05,0.0975952528214434,5664598,487843800,1.1611499418461402,026eb129231902f0208d1d23bd7e2c0edcca74ae042c69c5091464cdf4e9297d,798f470159dc878acad8eabf2ee3caf73e27ad9cbd61947c6e6db30751ad7778,data/thebe/seis/seistrain2.npz,data/thebe/fault/faulttrain2.npz,data/processed/thebe_h5/train2.h5,748153745
    train,100x3174x1537,float64,bool,float32,uint8,-8.393916130065918,7.38558292388916,-7.093819185128362e-06,0.10218002205944188,5068071,487843800,1.0388716634299748,2e8599638fc6912a0e935b827ab62481a6b49863943bed49dd0e3a799b050d42,283322439cfdbc306c21a5b8f304282cb5aae69dbc6ca9ccfec9bd4f4a576469,data/thebe/seis/seistrain3.npz,data/thebe/fault/faulttrain3.npz,data/processed/thebe_h5/train3.h5,780327606
    train,100x3174x1537,float64,bool,float32,uint8,-2.807478904724121,3.005870819091797,-4.016161870267805e-06,0.10568906220763231,3575397,487843800,0.7328979070759944,207742571324b7631cca8b497140dd7ac1f46e84bce4aa5549b21370db84b18e,753ebc026f3874ee359859ce13d505f66ef344406c94c6dfef329fdc182b342c,data/thebe/seis/seistrain4.npz,data/thebe/fault/faulttrain4.npz,data/processed/thebe_h5/train4.h5,812145386
    train,100x3174x1537,float64,bool,float32,uint8,-2.6587982177734375,2.834458351135254,-2.925060121001068e-06,0.11106203265206424,3570872,487843800,0.7319703560852879,66027b1f4df037aa0c3dae4a08ff42d11872068d6a9ddc479fd820d62c39ee3e,94d8fe88e7e8ead7d6399cfa2c9bfd256b75f1851a8c242a0180247969d9b7ac,data/thebe/seis/seistrain5.npz,data/thebe/fault/faulttrain5.npz,data/processed/thebe_h5/train5.h5,844142314
    train,100x3174x1537,float64,bool,float32,uint8,-2.676699638366699,9.433253288269043,5.592769920060861e-06,0.11655410640016116,3909866,487843800,0.8014585816197726,7580b1a3ba71b9abc1f63f54acf1d2b6c407a9b003d0180886446aa01560529f,71b418f08d9ed0d0a346496e07e82cae9967f5e588f2c825e05eb88bd17a8631,data/thebe/seis/seistrain6.npz,data/thebe/fault/faulttrain6.npz,data/processed/thebe_h5/train6.h5,877969475
    train,100x3174x1537,float64,bool,float32,uint8,-2.7207870483398438,2.8281021118164062,1.1942063768727192e-05,0.12574849960104517,6197892,487843800,1.2704664894788045,a8e2deff21c5a1e2fb45a758b466bfb46f30762153d96fd340055a6c37f816d6,1621e3db04c5ea33dc96a87e3f54cf1d5031341f7080fa85c7353d52eab21cc9,data/thebe/seis/seistrain7.npz,data/thebe/fault/faulttrain7.npz,data/processed/thebe_h5/train7.h5,1032693045
    train,100x3174x1537,float64,bool,float32,uint8,-2.84981632232666,2.660374641418457,9.623303973857554e-06,0.12655295620612175,5903062,487843800,1.2100311616136148,74205588023112fb56ef47b81908c370cae3b89bb1a10fdc9a6dc416c9ca6be5,8dc688183ad340ee95a42ff321d9f285c2719d7fcb7f5ca623a0da4353a92282,data/thebe/seis/seistrain8.npz,data/thebe/fault/faulttrain8.npz,data/processed/thebe_h5/train8.h5,1046692870
    train,100x3174x1537,float64,bool,float32,uint8,-3.216402053833008,3.139723777770996,2.7340818943474607e-07,0.12788971853180867,6739751,487843800,1.3815387220253696,2c13da092fdb4ed6cdb7aa947b0318268ead5f644bbfff8e6d75e6f77ffb6b07,a2e0459c72b56ce0bb3c0ccde438eef6f416ad1e63322566932fc98f77e116d0,data/thebe/seis/seistrain9.npz,data/thebe/fault/faulttrain9.npz,data/processed/thebe_h5/train9.h5,1054637087
    val,100x3174x1537,float64,bool,float32,uint8,-3.718324661254883,3.5749521255493164,-8.142081609447118e-06,0.13305340028663978,7906942,487843800,1.620793786863746,f6cca2e72c86d89e2c05feb92a1604a96d22a3557c25249f1cb2244e95205437,88341218e0d5e63b9092985d6c31612d6d64144d676babf8db194342d59c2bfb,data/thebe/seis/seisval1.npz,data/thebe/fault/faultval1.npz,data/processed/thebe_h5/val1.h5,1116731622
    val,100x3174x1537,float64,bool,float32,uint8,-3.8605175018310547,3.8904953002929688,-7.648144044332711e-06,0.1357798178216228,9245068,487843800,1.8950877309499474,dd57128664c2fe6e2fe78964e1a057ab23f918fab86fe73f82acbb68d19d0afb,5e1bd1d04cdfc8e875a4036d322cddb27433503e15462d1a56be262a3c47bdbd,data/thebe/seis/seisval2.npz,data/thebe/fault/faultval2.npz,data/processed/thebe_h5/val2.h5,1179747245
    
    --- reports/data_audit/thebe_train_val.log ---
    nohup: ignoring input
    train1.h5: 10/100 sections
    train1.h5: 20/100 sections
    train1.h5: 30/100 sections
    train1.h5: 40/100 sections
    train1.h5: 50/100 sections
    train1.h5: 60/100 sections
    train1.h5: 70/100 sections
    train1.h5: 80/100 sections
    train1.h5: 90/100 sections
    train1.h5: 100/100 sections
    RECORDED: data/processed/thebe_h5/train1.h5 and updated reports/data_audit/thebe_h5_statistics.csv
    train2.h5: 10/100 sections
    train2.h5: 20/100 sections
    train2.h5: 30/100 sections
    train2.h5: 40/100 sections
    train2.h5: 50/100 sections
    train2.h5: 60/100 sections
    train2.h5: 70/100 sections
    train2.h5: 80/100 sections
    train2.h5: 90/100 sections
    train2.h5: 100/100 sections
    RECORDED: data/processed/thebe_h5/train2.h5 and updated reports/data_audit/thebe_h5_statistics.csv
    train3.h5: 10/100 sections
    train3.h5: 20/100 sections
    train3.h5: 30/100 sections
    train3.h5: 40/100 sections
    train3.h5: 50/100 sections
    train3.h5: 60/100 sections
    train3.h5: 70/100 sections
    train3.h5: 80/100 sections
    train3.h5: 90/100 sections
    train3.h5: 100/100 sections
    RECORDED: data/processed/thebe_h5/train3.h5 and updated reports/data_audit/thebe_h5_statistics.csv
    train4.h5: 10/100 sections
    train4.h5: 20/100 sections
    train4.h5: 30/100 sections
    train4.h5: 40/100 sections
    train4.h5: 50/100 sections
    train4.h5: 60/100 sections
    train4.h5: 70/100 sections
    train4.h5: 80/100 sections
    train4.h5: 90/100 sections
    train4.h5: 100/100 sections
    RECORDED: data/processed/thebe_h5/train4.h5 and updated reports/data_audit/thebe_h5_statistics.csv
    train5.h5: 10/100 sections
    train5.h5: 20/100 sections
    train5.h5: 30/100 sections
    train5.h5: 40/100 sections
    train5.h5: 50/100 sections
    train5.h5: 60/100 sections
    train5.h5: 70/100 sections
    train5.h5: 80/100 sections
    train5.h5: 90/100 sections
    train5.h5: 100/100 sections
    RECORDED: data/processed/thebe_h5/train5.h5 and updated reports/data_audit/thebe_h5_statistics.csv
    train6.h5: 10/100 sections
    train6.h5: 20/100 sections
    train6.h5: 30/100 sections
    train6.h5: 40/100 sections
    train6.h5: 50/100 sections
    train6.h5: 60/100 sections
    train6.h5: 70/100 sections
    train6.h5: 80/100 sections
    train6.h5: 90/100 sections
    train6.h5: 100/100 sections
    RECORDED: data/processed/thebe_h5/train6.h5 and updated reports/data_audit/thebe_h5_statistics.csv
    train7.h5: 10/100 sections
    train7.h5: 20/100 sections
    train7.h5: 30/100 sections
    train7.h5: 40/100 sections
    train7.h5: 50/100 sections
    train7.h5: 60/100 sections
    train7.h5: 70/100 sections
    train7.h5: 80/100 sections
    train7.h5: 90/100 sections
    train7.h5: 100/100 sections
    RECORDED: data/processed/thebe_h5/train7.h5 and updated reports/data_audit/thebe_h5_statistics.csv
    train8.h5: 10/100 sections
    train8.h5: 20/100 sections
    train8.h5: 30/100 sections
    train8.h5: 40/100 sections
    train8.h5: 50/100 sections
    train8.h5: 60/100 sections
    train8.h5: 70/100 sections
    train8.h5: 80/100 sections
    train8.h5: 90/100 sections
    train8.h5: 100/100 sections
    RECORDED: data/processed/thebe_h5/train8.h5 and updated reports/data_audit/thebe_h5_statistics.csv
    train9.h5: 10/100 sections
    train9.h5: 20/100 sections
    train9.h5: 30/100 sections
    train9.h5: 40/100 sections
    train9.h5: 50/100 sections
    train9.h5: 60/100 sections
    train9.h5: 70/100 sections
    train9.h5: 80/100 sections
    train9.h5: 90/100 sections
    train9.h5: 100/100 sections
    RECORDED: data/processed/thebe_h5/train9.h5 and updated reports/data_audit/thebe_h5_statistics.csv
    val1.h5: 10/100 sections
    val1.h5: 20/100 sections
    val1.h5: 30/100 sections
    val1.h5: 40/100 sections
    val1.h5: 50/100 sections
    val1.h5: 60/100 sections
    val1.h5: 70/100 sections
    val1.h5: 80/100 sections
    val1.h5: 90/100 sections
    val1.h5: 100/100 sections
    RECORDED: data/processed/thebe_h5/val1.h5 and updated reports/data_audit/thebe_h5_statistics.csv
    val2.h5: 10/100 sections
    val2.h5: 20/100 sections
    val2.h5: 30/100 sections
    val2.h5: 40/100 sections
    val2.h5: 50/100 sections
    val2.h5: 60/100 sections
    val2.h5: 70/100 sections
    val2.h5: 80/100 sections
    val2.h5: 90/100 sections
    val2.h5: 100/100 sections
    RECORDED: data/processed/thebe_h5/val2.h5 and updated reports/data_audit/thebe_h5_statistics.csv
    PASS: converted 11 new Thebe blocks; updated reports/data_audit/thebe_h5_statistics.csv
    
    --- reports/data_audit/thebe_preprocessing_candidates.txt ---
    ./reports/data_audit/thebe_train_val.log
    ./reports/data_audit/thebe_h5_statistics.csv
    ./download_thebe.log
    ./scripts/prepare_seismic_datasets.py
    
    === H5/NUMPY ARRAY STRUCTURE ===
    Supported array files found: 54
    
    Directory: data/processed/thebe_h5
    Count: 18
    
    Directory: data/thebe/fault
    Count: 18
    
    Directory: data/thebe/seis
    Count: 18
    
    --- INSPECTING: data/processed/thebe_h5/test1.h5 ---
    File attributes:
      fault_positive_count: np.int64(8401766)
      seismic_max: np.float64(3.6155223846435547)
      seismic_mean: np.float64(7.045719784800201e-06)
      seismic_min: np.float64(-4.100235939025879)
      seismic_std: np.float64(0.13845259212179462)
      source_fault: 'data/thebe/fault/faulttest1.npz'
      source_fault_dtype: 'bool'
      source_seismic: 'data/thebe/seis/seistest1.npz'
      source_seismic_dtype: 'float64'
    Dataset fault: shape=(100, 3174, 1537), dtype=uint8, chunks=(1, 256, 256), compression=gzip
    Dataset seismic: shape=(100, 3174, 1537), dtype=float32, chunks=(1, 256, 256), compression=gzip
    
    --- INSPECTING: data/processed/thebe_h5/test2.h5 ---
    File attributes:
      fault_positive_count: np.int64(8253759)
      seismic_max: np.float64(3.876628875732422)
      seismic_mean: np.float64(8.401971943081868e-06)
      seismic_min: np.float64(-3.4763288497924805)
      seismic_std: np.float64(0.13612245757742752)
      source_fault: 'data/thebe/fault/faulttest2.npz'
      source_fault_dtype: 'bool'
      source_seismic: 'data/thebe/seis/seistest2.npz'
      source_seismic_dtype: 'float64'
    Dataset fault: shape=(100, 3174, 1537), dtype=uint8, chunks=(1, 256, 256), compression=gzip
    Dataset seismic: shape=(100, 3174, 1537), dtype=float32, chunks=(1, 256, 256), compression=gzip
    
    --- INSPECTING: data/processed/thebe_h5/val1.h5 ---
    File attributes:
      fault_positive_count: np.int64(7906942)
      seismic_max: np.float64(3.5749521255493164)
      seismic_mean: np.float64(-8.142081609447118e-06)
      seismic_min: np.float64(-3.718324661254883)
      seismic_std: np.float64(0.13305340028663978)
      source_fault: 'data/thebe/fault/faultval1.npz'
      source_fault_dtype: 'bool'
      source_seismic: 'data/thebe/seis/seisval1.npz'
      source_seismic_dtype: 'float64'
    Dataset fault: shape=(100, 3174, 1537), dtype=uint8, chunks=(1, 256, 256), compression=gzip
    Dataset seismic: shape=(100, 3174, 1537), dtype=float32, chunks=(1, 256, 256), compression=lzf
    
    --- INSPECTING: data/processed/thebe_h5/val2.h5 ---
    File attributes:
      fault_positive_count: np.int64(9245068)
      seismic_max: np.float64(3.8904953002929688)
      seismic_mean: np.float64(-7.648144044332711e-06)
      seismic_min: np.float64(-3.8605175018310547)
      seismic_std: np.float64(0.1357798178216228)
      source_fault: 'data/thebe/fault/faultval2.npz'
      source_fault_dtype: 'bool'
      source_seismic: 'data/thebe/seis/seisval2.npz'
      source_seismic_dtype: 'float64'
    Dataset fault: shape=(100, 3174, 1537), dtype=uint8, chunks=(1, 256, 256), compression=gzip
    Dataset seismic: shape=(100, 3174, 1537), dtype=float32, chunks=(1, 256, 256), compression=lzf
    
    --- INSPECTING: data/thebe/fault/faulttest1.npz ---
    keys=['arr_0']
      arr_0: shape=(100, 3174, 1537), dtype=bool
    
    --- INSPECTING: data/thebe/fault/faulttest2.npz ---
    keys=['arr_0']
      arr_0: shape=(100, 3174, 1537), dtype=bool
    
    --- INSPECTING: data/thebe/fault/faultval1.npz ---
    keys=['arr_0']
      arr_0: shape=(100, 3174, 1537), dtype=bool
    
    --- INSPECTING: data/thebe/fault/faultval2.npz ---
    keys=['arr_0']
      arr_0: shape=(100, 3174, 1537), dtype=bool
    
    --- INSPECTING: data/thebe/seis/seistest1.npz ---
    keys=['arr_0']
      arr_0: shape=(100, 3174, 1537), dtype=float64
    
    --- INSPECTING: data/thebe/seis/seistest2.npz ---
    keys=['arr_0']
      arr_0: shape=(100, 3174, 1537), dtype=float64
    
    --- INSPECTING: data/thebe/seis/seisval1.npz ---
    keys=['arr_0']
      arr_0: shape=(100, 3174, 1537), dtype=float64
    
    --- INSPECTING: data/thebe/seis/seisval2.npz ---
    keys=['arr_0']
      arr_0: shape=(100, 3174, 1537), dtype=float64
    
    === POSSIBLE THEBE MANIFESTS ===
    
    
    === ALL CURRENT MANIFEST FILES ===
    130 bytes  data/manifests/faultseg3d_test.txt
    1346 bytes  data/manifests/faultseg3d_train.txt
    144 bytes  data/manifests/faultseg3d_val.txt
    16 bytes  data/manifests/cracks_masks_without_images.txt
    6336 bytes  data/manifests/cracks_available_images.txt
    640 bytes  data/manifests/cracks_expert_sections.txt
    
    === BASELINE DATA LOADER ===
    def read_manifest(path: Path) -> list[str]:
        if not path.is_file():
            raise FileNotFoundError(f"Missing manifest: {path}")
        names = [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
        if not names:
            raise RuntimeError(f"Empty manifest: {path}")
        if len(names) != len(set(names)):
            raise RuntimeError(f"Duplicate IDs in manifest: {path}")
        return names
    
    
    class FaultSegDataset(Dataset[tuple[Tensor, Tensor, str]]):
        def __init__(
            self,
            split_root: Path,
            manifest: Path,
            include_fixed_flip: bool,
        ) -> None:
            self.split_root = split_root
            self.names = read_manifest(manifest)
            self.samples: list[tuple[str, bool]] = []
            for name in self.names:
                self.samples.append((name, False))
                if include_fixed_flip:
                    self.samples.append((name, True))
    
            expected_values = math.prod(VOLUME_SHAPE)
            expected_bytes = expected_values * np.dtype(np.float32).itemsize
            for name in self.names:
                for kind in ("seis", "fault"):
                    path = self.split_root / kind / name
                    if not path.is_file():
                        raise FileNotFoundError(path)
                    if path.stat().st_size != expected_bytes:
                        raise RuntimeError(
                            f"Unexpected size for {path}: {path.stat().st_size}; "
                            f"expected {expected_bytes}"
                        )
    
        def __len__(self) -> int:
            return len(self.samples)
    
        def __getitem__(self, index: int) -> tuple[Tensor, Tensor, str]:
            name, flipped = self.samples[index]
            seismic_path = self.split_root / "seis" / name
            fault_path = self.split_root / "fault" / name
    
            seismic = np.fromfile(seismic_path, dtype=np.float32).reshape(VOLUME_SHAPE)
            fault = np.fromfile(fault_path, dtype=np.float32).reshape(VOLUME_SHAPE)
            if not np.isfinite(seismic).all() or not np.isfinite(fault).all():
                raise RuntimeError(f"NaN/Inf in pair {name}")
            if not np.isin(np.unique(fault), (0.0, 1.0)).all():
                raise RuntimeError(f"Non-binary label in {fault_path}")
    
            # Match the public FaultSeg3D loader: standardize each seismic volume
            # independently, then reverse the axis order for seismic conventions.
            mean = float(seismic.mean(dtype=np.float64))
            std = float(seismic.std(dtype=np.float64))
            if not std > 0.0:
                raise RuntimeError(f"Zero standard deviation in {seismic_path}")
            seismic = (seismic - mean) / std
            seismic = np.transpose(seismic)
            fault = np.transpose(fault)
            if flipped:
                seismic = np.flip(seismic, axis=0)
                fault = np.flip(fault, axis=0)
    
            seismic = np.ascontiguousarray(seismic[None], dtype=np.float32)
            fault = np.ascontiguousarray(fault[None], dtype=np.float32)
            sample_id = f"{Path(name).stem}{'_flip' if flipped else ''}"
            return torch.from_numpy(seismic), torch.from_numpy(fault), sample_id
    
    
    def soft_dice_loss(logits: Tensor, target: Tensor, smooth: float = 1.0) -> Tensor:
    
    === THEBE PREPARATION IMPLEMENTATION ===
        encoding = "utf-8" if major == 3 else "latin1"
        header = ast.literal_eval(read_exact(stream, header_length).decode(encoding).strip())
        return tuple(header["shape"]), bool(header["fortran_order"]), np.dtype(header["descr"])
    
    
    def only_npy_member(archive: zipfile.ZipFile) -> str:
        members = [name for name in archive.namelist() if name.endswith(".npy")]
        if len(members) != 1:
            raise RuntimeError(f"Expected one NPY member, found {members}")
        return members[0]
    
    
    def thebe_h5(data_root: Path, splits: list[str]) -> None:
        try:
            import h5py
        except ImportError as exc:
            raise RuntimeError("h5py is required: python -m pip install h5py") from exc
    
        source_root = data_root / "thebe"
        output_root = data_root / "processed" / "thebe_h5"
        output_root.mkdir(parents=True, exist_ok=True)
        report_path = REPORT_DIR / "thebe_h5_statistics.csv"
        records: dict[str, dict] = {}
        if report_path.exists():
            with report_path.open(newline="", encoding="utf-8") as stream:
                records = {
                    row["output_path"]: row
                    for row in csv.DictReader(stream)
                    if row.get("output_path")
                }
        converted = 0
        patterns = {"train": "seistrain*.npz", "val": "seisval*.npz", "test": "seistest*.npz"}
        reserve_bytes = 15 * 1024**3
    
        for split in splits:
            seismic_files = sorted((source_root / "seis").glob(patterns[split]), key=natural_key)
            if not seismic_files:
                raise RuntimeError(f"No Thebe files found for split {split}")
            for seismic_npz in seismic_files:
                suffix = seismic_npz.name[len("seis"):]
                fault_npz = source_root / "fault" / f"fault{suffix}"
                if not fault_npz.exists():
                    raise RuntimeError(f"Missing pair for {seismic_npz}: {fault_npz}")
                output_path = output_root / seismic_npz.name.replace("seis", "", 1).replace(".npz", ".h5")
                if output_path.exists():
                    output_key = str(output_path)
                    if output_key not in records:
                        with h5py.File(output_path, "r") as h5:
                            shape = tuple(h5["seismic"].shape)
                            voxel_count = int(np.prod(shape))
                            positive_count = int(h5.attrs["fault_positive_count"])
                            records[output_key] = {
                                "split": split,
                                "shape": "x".join(str(x) for x in shape),
                                "source_seismic_dtype": str(h5.attrs["source_seismic_dtype"]),
                                "source_fault_dtype": str(h5.attrs["source_fault_dtype"]),
                                "output_seismic_dtype": "float32",
                                "output_fault_dtype": "uint8",
                                "seismic_min": float(h5.attrs["seismic_min"]),
                                "seismic_max": float(h5.attrs["seismic_max"]),
                                "seismic_mean": float(h5.attrs["seismic_mean"]),
                                "seismic_std": float(h5.attrs["seismic_std"]),
                                "fault_positive_count": positive_count,
                                "total_voxels": voxel_count,
                                "fault_positive_pct": 100.0 * positive_count / voxel_count,
                                "source_seismic_sha256": sha256_file(seismic_npz),
                                "source_fault_sha256": sha256_file(fault_npz),
                                "source_seismic_path": str(seismic_npz),
                                "source_fault_path": str(fault_npz),
                                "output_path": output_key,
                                "output_bytes": output_path.stat().st_size,
                            }
                        write_csv(report_path, list(records.values()))
                        print(f"RECOVERED CSV row for existing {output_path}", flush=True)
                    else:
                        print(f"SKIP: already exists: {output_path}", flush=True)
                    continue
    
                with zipfile.ZipFile(seismic_npz) as szip, zipfile.ZipFile(fault_npz) as fzip:
                    smember = only_npy_member(szip)
                    fmember = only_npy_member(fzip)
                    with szip.open(smember) as sstream, fzip.open(fmember) as fstream:
                        sshape, sfortran, sdtype = read_npy_header(sstream)
                        fshape, ffortran, fdtype = read_npy_header(fstream)
                        if sshape != fshape or len(sshape) != 3:
                            raise RuntimeError(f"Shape mismatch: {sshape} vs {fshape}")
                        if sfortran or ffortran:
                            raise RuntimeError("Fortran-order Thebe arrays are not supported")
    
                        voxel_count = int(np.prod(sshape))
                        worst_output = voxel_count * 5  # float32 seismic + uint8 mask
                        free = shutil.disk_usage(output_root).free
                        if free < worst_output + reserve_bytes:
                            raise RuntimeError(
                                f"Insufficient free disk for {output_path}. "
                                f"Free={free / 1024**3:.1f} GiB, worst output="
                                f"{worst_output / 1024**3:.1f} GiB, reserve=15 GiB"
                            )
    
                        section_shape = sshape[1:]
                        section_values = int(np.prod(section_shape))
                        sbytes = section_values * sdtype.itemsize
                        fbytes = section_values * fdtype.itemsize
                        chunk_shape = (1, min(256, sshape[1]), min(256, sshape[2]))
                        part_path = output_path.with_suffix(".h5.part")
    
    
    === THEBE SPLIT/COORDINATE REFERENCES ===
    1-termina#!/usr/bin/env python3
    2:"""Audit and prepare FaultSeg3D, CRACKS, and Thebe without altering raw data."""
    3-
    4-from __future__ import annotations
    5-
    --
    18-from PIL import Image
    19-
    20-
    21:FAULTSEG_SHAPE = (128, 128, 128)
    22-REPORT_DIR = Path("reports/data_audit")
    23-
    24-
    25:def sha256_file(path: Path, block_size: int = 8 * 1024 * 1024) -> str:
    26-    digest = hashlib.sha256()
    27-    with path.open("rb") as stream:
    28:        while block := stream.read(block_size):
    29:            digest.update(block)
    30-    return digest.hexdigest()
    31-
    32-
    33-def natural_key(path: Path):
    34-    return [int(piece) if piece.isdigit() else piece.lower()
    35:            for piece in re.split(r"(\d+)", path.name)]
    36-
    37-
    38-def write_csv(path: Path, rows: list[dict]) -> None:
    --
    47-
    48-def faultseg_csv(data_root: Path) -> None:
    49-    rows: list[dict] = []
    50:    expected_bytes = int(np.prod(FAULTSEG_SHAPE)) * np.dtype(np.float32).itemsize
    51-
    52:    for split in ("train", "validation"):
    53:        seis_dir = data_root / "faultseg3d" / split / "seis"
    54:        fault_dir = data_root / "faultseg3d" / split / "fault"
    55-        seis_files = {p.name: p for p in seis_dir.glob("*.dat")}
    56-        fault_files = {p.name: p for p in fault_dir.glob("*.dat")}
    57-        if seis_files.keys() != fault_files.keys():
    58-            missing_fault = sorted(seis_files.keys() - fault_files.keys())
    59-            missing_seis = sorted(fault_files.keys() - seis_files.keys())
    60-            raise RuntimeError(
    61:                f"{split}: unmatched pairs; missing fault={missing_fault}, "
    62-                f"missing seismic={missing_seis}"
    63-            )
    64-
    --
    71-            if fault_path.stat().st_size != expected_bytes:
    72-                raise RuntimeError(f"Wrong size: {fault_path}")
    73-
    74:            seis = np.fromfile(seis_path, dtype=np.float32).reshape(FAULTSEG_SHAPE)
    75:            fault = np.fromfile(fault_path, dtype=np.float32).reshape(FAULTSEG_SHAPE)
    76-            labels = np.unique(fault)
    77-            if not np.isfinite(seis).all() or not np.isfinite(fault).all():
    78-                raise RuntimeError(f"NaN/Inf found in pair {name}")
    --
    82-            positives = int(np.count_nonzero(fault))
    83-            voxels = int(fault.size)
    84-            rows.append({
    85:                "split": split,
    86-                "volume_id": Path(name).stem,
    87:                "shape": "128x128x128",
    88-                "seismic_dtype": str(seis.dtype),
    89-                "fault_dtype": str(fault.dtype),
    90-                "seismic_bytes": seis_path.stat().st_size,
    91-                "fault_bytes": fault_path.stat().st_size,
    92-                "seismic_min": float(seis.min()),
    93-                "seismic_max": float(seis.max()),
    94:                "seismic_mean": float(seis.mean(dtype=np.float64)),
    95:                "seismic_std": float(seis.std(dtype=np.float64)),
    96-                "fault_positive_voxels": positives,
    97-                "total_voxels": voxels,
    98-                "fault_positive_pct": 100.0 * positives / voxels,
    --
    104-                "fault_path": str(fault_path),
    105-            })
    106-            if index % 25 == 0 or index == len(names):
    107:                print(f"{split}: audited {index}/{len(names)} pairs", flush=True)
    108-
    109-    output = REPORT_DIR / "faultseg3d_volume_statistics.csv"
    110-    write_csv(output, rows)
    --
    116-    mask_root = data_root / "cracks" / "Fault segmentations"
    117-    output_root = data_root / "processed" / "cracks"
    118-    target_root = output_root / "target"
    119:    valid_root = output_root / "valid"
    120-    rows: list[dict] = []
    121-
    122-    image_names = {p.name for p in image_dir.glob("section_*.png")}
    --
    139-            "raw_1_certain_nonfault": "",
    140-            "raw_2_uncertain_fault": "",
    141-            "raw_3_certain_fault": "",
    142:            "valid_pixels": "",
    143-            "positive_pixels": "",
    144:            "positive_pct_of_valid": "",
    145-            "source_sha256": sha256_file(mask_path),
    146-            "source_path": str(mask_path),
    147-            "target_path": "",
    148:            "valid_path": "",
    149-        }
    150-        if not image_exists:
    151-            skipped += 1
    --
    154-
    155-        mask = np.asarray(Image.open(mask_path))
    156-        if mask.ndim != 2:
    157:            raise RuntimeError(f"Expected indexed 2D mask, got {mask.shape}: {mask_path}")
    158-        labels, counts = np.unique(mask, return_counts=True)
    159-        if not np.isin(labels, [0, 1, 2, 3]).all():
    160:            raise RuntimeError(f"Unexpected mask values {labels.tolist()}: {mask_path}")
    161-        count_map = {int(label): int(count) for label, count in zip(labels, counts)}
    162-
    163-        target = np.isin(mask, [2, 3]).astype(np.uint8) * 255
    164:        valid = (mask != 0).astype(np.uint8) * 255
    165-        target_path = target_root / annotator / mask_path.name
    166:        valid_path = valid_root / annotator / mask_path.name
    167-        target_path.parent.mkdir(parents=True, exist_ok=True)
    168:        valid_path.parent.mkdir(parents=True, exist_ok=True)
    169-        Image.fromarray(target).save(target_path)
    170:        Image.fromarray(valid).save(valid_path)
    171-
    172:        valid_pixels = int(np.count_nonzero(valid))
    173-        positive_pixels = int(np.count_nonzero(target))
    174-        row.update({
    175:            "height": mask.shape[0],
    176:            "width": mask.shape[1],
    177-            "raw_0_unknown": count_map.get(0, 0),
    178-            "raw_1_certain_nonfault": count_map.get(1, 0),
    179-            "raw_2_uncertain_fault": count_map.get(2, 0),
    180-            "raw_3_certain_fault": count_map.get(3, 0),
    181:            "valid_pixels": valid_pixels,
    182-            "positive_pixels": positive_pixels,
    183:            "positive_pct_of_valid": (
    184:                100.0 * positive_pixels / valid_pixels if valid_pixels else 0.0
    185-            ),
    186-            "target_path": str(target_path),
    187:            "valid_path": str(valid_path),
    188-        })
    189-        rows.append(row)
    190-        processed += 1
    --
    197-    semantics.parent.mkdir(parents=True, exist_ok=True)
    198-    semantics.write_text(
    199-        "Raw 0 = unknown/unannotated (ignore in loss)\n"
    200:        "Raw 1 = certain non-fault (valid target 0)\n"
    201:        "Raw 2 = uncertain fault (valid target 1)\n"
    202:        "Raw 3 = certain fault (valid target 1)\n"
    203-        "Derived target PNG: 0=non-fault/ignored, 255=fault\n"
    204:        "Derived valid PNG: 0=ignore, 255=include in loss\n",
    205-        encoding="utf-8",
    206-    )
    207-    print(
    --
    224-
    225-def read_npy_header(stream):
    226-    if read_exact(stream, 6) != b"\x93NUMPY":
    227:        raise ValueError("Invalid NPY magic value")
    228-    major, minor = read_exact(stream, 2)
    229-    if major == 1:
    230-        header_length = struct.unpack("<H", read_exact(stream, 2))[0]
    231-    elif major in (2, 3):
    232-        header_length = struct.unpack("<I", read_exact(stream, 4))[0]
    233-    else:
    234:        raise ValueError(f"Unsupported NPY version {(major, minor)}")
    235-    encoding = "utf-8" if major == 3 else "latin1"
    236:    header = ast.literal_eval(read_exact(stream, header_length).decode(encoding).strip())
    237:    return tuple(header["shape"]), bool(header["fortran_order"]), np.dtype(header["descr"])
    238-
    239-
    240-def only_npy_member(archive: zipfile.ZipFile) -> str:
    --
    244-    return members[0]
    245-
    246-
    247:def thebe_h5(data_root: Path, splits: list[str]) -> None:
    248-    try:
    249-        import h5py
    250-    except ImportError as exc:
    251-        raise RuntimeError("h5py is required: python -m pip install h5py") from exc
    252-
    253:    source_root = data_root / "thebe"
    254:    output_root = data_root / "processed" / "thebe_h5"
    255-    output_root.mkdir(parents=True, exist_ok=True)
    256:    report_path = REPORT_DIR / "thebe_h5_statistics.csv"
    257-    records: dict[str, dict] = {}
    258-    if report_path.exists():
    259-        with report_path.open(newline="", encoding="utf-8") as stream:
    --
    263-                if row.get("output_path")
    264-            }
    265-    converted = 0
    266:    patterns = {"train": "seistrain*.npz", "val": "seisval*.npz", "test": "seistest*.npz"}
    267-    reserve_bytes = 15 * 1024**3
    268-
    269:    for split in splits:
    270:        seismic_files = sorted((source_root / "seis").glob(patterns[split]), key=natural_key)
    271-        if not seismic_files:
    272:            raise RuntimeError(f"No Thebe files found for split {split}")
    273-        for seismic_npz in seismic_files:
    274-            suffix = seismic_npz.name[len("seis"):]
    275-            fault_npz = source_root / "fault" / f"fault{suffix}"
    --
    280-                output_key = str(output_path)
    281-                if output_key not in records:
    282-                    with h5py.File(output_path, "r") as h5:
    283:                        shape = tuple(h5["seismic"].shape)
    284:                        voxel_count = int(np.prod(shape))
    285-                        positive_count = int(h5.attrs["fault_positive_count"])
    286-                        records[output_key] = {
    287:                            "split": split,
    288:                            "shape": "x".join(str(x) for x in shape),
    289-                            "source_seismic_dtype": str(h5.attrs["source_seismic_dtype"]),
    290-                            "source_fault_dtype": str(h5.attrs["source_fault_dtype"]),
    291-                            "output_seismic_dtype": "float32",
    292-                            "output_fault_dtype": "uint8",
    293-                            "seismic_min": float(h5.attrs["seismic_min"]),
    294-                            "seismic_max": float(h5.attrs["seismic_max"]),
    295:                            "seismic_mean": float(h5.attrs["seismic_mean"]),
    296:                            "seismic_std": float(h5.attrs["seismic_std"]),
    297-                            "fault_positive_count": positive_count,
    298-                            "total_voxels": voxel_count,
    299-                            "fault_positive_pct": 100.0 * positive_count / voxel_count,
    --
    304-                            "output_path": output_key,
    305-                            "output_bytes": output_path.stat().st_size,
    306-                        }
    307:                    write_csv(report_path, list(records.values()))
    308-                    print(f"RECOVERED CSV row for existing {output_path}", flush=True)
    309-                else:
    310-                    print(f"SKIP: already exists: {output_path}", flush=True)
    --
    314-                smember = only_npy_member(szip)
    315-                fmember = only_npy_member(fzip)
    316-                with szip.open(smember) as sstream, fzip.open(fmember) as fstream:
    317:                    sshape, sfortran, sdtype = read_npy_header(sstream)
    318:                    fshape, ffortran, fdtype = read_npy_header(fstream)
    319:                    if sshape != fshape or len(sshape) != 3:
    320:                        raise RuntimeError(f"Shape mismatch: {sshape} vs {fshape}")
    321-                    if sfortran or ffortran:
    322:                        raise RuntimeError("Fortran-order Thebe arrays are not supported")
    323-
    324:                    voxel_count = int(np.prod(sshape))
    325-                    worst_output = voxel_count * 5  # float32 seismic + uint8 mask
    326-                    free = shutil.disk_usage(output_root).free
    327-                    if free < worst_output + reserve_bytes:
    --
    331-                            f"{worst_output / 1024**3:.1f} GiB, reserve=15 GiB"
    332-                        )
    333-
    334:                    section_shape = sshape[1:]
    335:                    section_values = int(np.prod(section_shape))
    336:                    sbytes = section_values * sdtype.itemsize
    337:                    fbytes = section_values * fdtype.itemsize
    338:                    chunk_shape = (1, min(256, sshape[1]), min(256, sshape[2]))
    339-                    part_path = output_path.with_suffix(".h5.part")
    340-
    341-                    total_sum = 0.0
    --
    346-
    347-                    with h5py.File(part_path, "w") as h5:
    348-                        seis_ds = h5.create_dataset(
    349:                            "seismic", shape=sshape, dtype="f4", chunks=chunk_shape,
    350-                            compression="lzf", shuffle=True
    351-                        )
    352-                        fault_ds = h5.create_dataset(
    353:                            "fault", shape=fshape, dtype="u1", chunks=chunk_shape,
    354-                            compression="gzip", compression_opts=1, shuffle=True
    355-                        )
    356:                        for section_index in range(sshape[0]):
    357-                            seismic = np.frombuffer(
    358-                                read_exact(sstream, sbytes), dtype=sdtype
    359:                            ).reshape(section_shape)
    360-                            fault = np.frombuffer(
    361-                                read_exact(fstream, fbytes), dtype=fdtype
    362:                            ).reshape(section_shape)
    363-                            if not np.isfinite(seismic).all():
    364-                                raise RuntimeError(
    365-                                    f"NaN/Inf in {seismic_npz}, section {section_index}"
    --
    382-                            seis_ds[section_index] = seismic.astype(np.float32)
    383-                            fault_ds[section_index] = fault.astype(np.uint8)
    384-
    385:                            if (section_index + 1) % 10 == 0 or section_index + 1 == sshape[0]:
    386-                                print(
    387:                                    f"{output_path.name}: {section_index + 1}/{sshape[0]} sections",
    388-                                    flush=True,
    389-                                )
    390-
    391-                        if sstream.read(1) or fstream.read(1):
    392-                            raise RuntimeError("Unexpected trailing bytes in NPY data")
    393-
    394:                        mean = total_sum / voxel_count
    395:                        variance = max(0.0, total_sumsq / voxel_count - mean * mean)
    396:                        std = variance ** 0.5
    397-                        h5.attrs["source_seismic"] = str(seismic_npz)
    398-                        h5.attrs["source_fault"] = str(fault_npz)
    399-                        h5.attrs["source_seismic_dtype"] = str(sdtype)
    400-                        h5.attrs["source_fault_dtype"] = str(fdtype)
    401-                        h5.attrs["seismic_min"] = global_min
    402-                        h5.attrs["seismic_max"] = global_max
    403:                        h5.attrs["seismic_mean"] = mean
    404:                        h5.attrs["seismic_std"] = std
    405-                        h5.attrs["fault_positive_count"] = positive_count
    406-
    407-                    os.replace(part_path, output_path)
    408-                    row = {
    409:                        "split": split,
    410:                        "shape": "x".join(str(x) for x in sshape),
    411-                        "source_seismic_dtype": str(sdtype),
    412-                        "source_fault_dtype": str(fdtype),
    413-                        "output_seismic_dtype": "float32",
    414-                        "output_fault_dtype": "uint8",
    415-                        "seismic_min": global_min,
    416-                        "seismic_max": global_max,
    417:                        "seismic_mean": mean,
    418:                        "seismic_std": std,
    419-                        "fault_positive_count": positive_count,
    420-                        "total_voxels": voxel_count,
    421-                        "fault_positive_pct": 100.0 * positive_count / voxel_count,
    --
    427-                        "output_bytes": output_path.stat().st_size,
    428-                    }
    429-                    records[str(output_path)] = row
    430:                    write_csv(report_path, list(records.values()))
    431-                    converted += 1
    432-                    print(f"RECORDED: {output_path} and updated {report_path}", flush=True)
    433-
    434-    if converted:
    435:        print(f"PASS: converted {converted} new Thebe blocks; updated {report_path}")
    436-    else:
    437:        print("PASS: no new Thebe files required conversion; existing files were verified.")
    438-
    439-
    440-def main() -> None:
    --
    443-    commands = parser.add_subparsers(dest="command", required=True)
    444-    commands.add_parser("faultseg-csv")
    445-    commands.add_parser("cracks-masks")
    446:    thebe_parser = commands.add_parser("thebe-h5")
    447:    thebe_parser.add_argument(
    448:        "--splits", nargs="+", choices=("train", "val", "test"),
    449:        default=("train", "val")
    450-    )
    451-    args = parser.parse_args()
    452-
    --
    454-        faultseg_csv(args.data_root)
    455-    elif args.command == "cracks-masks":
    456-        cracks_masks(args.data_root)
    457:    elif args.command == "thebe-h5":
    458:        thebe_h5(args.data_root, args.splits)
    459-
    460-
    461-if __name__ == "__main__":
    
    === EXISTING EVALUATION ENTRY POINTS ===
    scripts/prepare_seismic_datasets.py-439-
    scripts/prepare_seismic_datasets.py-440-def main() -> None:
    scripts/prepare_seismic_datasets.py-441-    parser = argparse.ArgumentParser(description=__doc__)
    scripts/prepare_seismic_datasets.py:442:    parser.add_argument("--data-root", type=Path, default=Path("data"))
    scripts/prepare_seismic_datasets.py-443-    commands = parser.add_subparsers(dest="command", required=True)
    scripts/prepare_seismic_datasets.py-444-    commands.add_parser("faultseg-csv")
    scripts/prepare_seismic_datasets.py-445-    commands.add_parser("cracks-masks")
    --
    scripts/faultseg3d_baseline.py-415-
    scripts/faultseg3d_baseline.py-416-
    scripts/faultseg3d_baseline.py-417-@torch.no_grad()
    scripts/faultseg3d_baseline.py:418:def evaluate(
    scripts/faultseg3d_baseline.py-419-    model: nn.Module,
    scripts/faultseg3d_baseline.py-420-    loader: DataLoader,
    scripts/faultseg3d_baseline.py-421-    device: torch.device,
    --
    scripts/faultseg3d_baseline.py-424-    histogram_bins: int,
    scripts/faultseg3d_baseline.py-425-    save_per_volume: Path | None = None,
    scripts/faultseg3d_baseline.py-426-    compute_structural: bool = False,
    scripts/faultseg3d_baseline.py:427:    measure_inference: bool = False,
    scripts/faultseg3d_baseline.py-428-) -> tuple[Metrics, ProbabilityHistogram, list[dict[str, object]]]:
    scripts/faultseg3d_baseline.py-429-    model.eval()
    scripts/faultseg3d_baseline.py-430-    aggregate = ProbabilityHistogram(histogram_bins)
    --
    scripts/faultseg3d_baseline.py-432-    for seismic, fault, sample_ids in loader:
    scripts/faultseg3d_baseline.py-433-        seismic = seismic.to(device, non_blocking=True)
    scripts/faultseg3d_baseline.py-434-        fault = fault.to(device, non_blocking=True)
    scripts/faultseg3d_baseline.py:435:        if measure_inference and device.type == "cuda":
    scripts/faultseg3d_baseline.py-436-            torch.cuda.synchronize()
    scripts/faultseg3d_baseline.py:437:        inference_started = time.perf_counter()
    scripts/faultseg3d_baseline.py-438-        with autocast_context(amp_enabled):
    scripts/faultseg3d_baseline.py-439-            logits = model(seismic)
    scripts/faultseg3d_baseline.py:440:        if measure_inference and device.type == "cuda":
    scripts/faultseg3d_baseline.py-441-            torch.cuda.synchronize()
    scripts/faultseg3d_baseline.py:442:        inference_seconds = time.perf_counter() - inference_started
    scripts/faultseg3d_baseline.py-443-        probability = torch.sigmoid(logits.float())
    scripts/faultseg3d_baseline.py-444-        aggregate.update_probabilities(probability, fault)
    scripts/faultseg3d_baseline.py-445-
    scripts/faultseg3d_baseline.py:446:        if save_per_volume is not None or compute_structural or measure_inference:
    scripts/faultseg3d_baseline.py-447-            for batch_index, sample_id in enumerate(sample_ids):
    scripts/faultseg3d_baseline.py-448-                individual = ProbabilityHistogram(histogram_bins)
    scripts/faultseg3d_baseline.py-449-                individual.update_probabilities(
    --
    scripts/faultseg3d_baseline.py-458-                    )
    scripts/faultseg3d_baseline.py-459-                    target_mask = fault[batch_index].detach().cpu().numpy() >= 0.5
    scripts/faultseg3d_baseline.py-460-                    row.update(structural_distances(predicted_mask, target_mask))
    scripts/faultseg3d_baseline.py:461:                if measure_inference:
    scripts/faultseg3d_baseline.py:462:                    row["inference_seconds"] = inference_seconds / len(sample_ids)
    scripts/faultseg3d_baseline.py-463-                per_volume_rows.append(row)
    scripts/faultseg3d_baseline.py-464-
    scripts/faultseg3d_baseline.py-465-    metrics = aggregate.metrics(threshold)
    --
    scripts/faultseg3d_baseline.py-472-    return metrics, aggregate, per_volume_rows
    scripts/faultseg3d_baseline.py-473-
    scripts/faultseg3d_baseline.py-474-
    scripts/faultseg3d_baseline.py:475:def save_checkpoint(
    scripts/faultseg3d_baseline.py-476-    path: Path,
    scripts/faultseg3d_baseline.py-477-    model: nn.Module,
    scripts/faultseg3d_baseline.py-478-    optimizer: torch.optim.Optimizer,
    --
    scripts/faultseg3d_baseline.py-544-    val_loader = make_loader(
    scripts/faultseg3d_baseline.py-545-        val_dataset, 1, False, args.workers, args.seed, use_cuda
    scripts/faultseg3d_baseline.py-546-    )
    scripts/faultseg3d_baseline.py:547:    test_loader = make_loader(
    scripts/faultseg3d_baseline.py-548-        test_dataset, 1, False, args.workers, args.seed, use_cuda
    scripts/faultseg3d_baseline.py-549-    )
    scripts/faultseg3d_baseline.py-550-
    --
    scripts/faultseg3d_baseline.py-616-                optimizer.zero_grad(set_to_none=True)
    scripts/faultseg3d_baseline.py-617-                optimizer_steps += 1
    scripts/faultseg3d_baseline.py-618-
    scripts/faultseg3d_baseline.py:619:        validation, _, _ = evaluate(
    scripts/faultseg3d_baseline.py-620-            model,
    scripts/faultseg3d_baseline.py-621-            val_loader,
    scripts/faultseg3d_baseline.py-622-            device,
    --
    scripts/faultseg3d_baseline.py-633-        }
    scripts/faultseg3d_baseline.py-634-        history.append(row)
    scripts/faultseg3d_baseline.py-635-        write_history(run_dir / "history.csv", history)
    scripts/faultseg3d_baseline.py:636:        save_checkpoint(run_dir / "last.pt", model, optimizer, epoch, args, validation)
    scripts/faultseg3d_baseline.py-637-        if validation.dice > best_dice:
    scripts/faultseg3d_baseline.py-638-            best_dice = validation.dice
    scripts/faultseg3d_baseline.py:639:            save_checkpoint(run_dir / "best.pt", model, optimizer, epoch, args, validation)
    scripts/faultseg3d_baseline.py-640-        print(
    scripts/faultseg3d_baseline.py-641-            f"epoch={epoch:03d} loss={row['train_loss']:.6f} "
    scripts/faultseg3d_baseline.py-642-            f"val_dice={validation.dice:.6f} val_iou={validation.iou:.6f} "
    --
    scripts/faultseg3d_baseline.py-646-        )
    scripts/faultseg3d_baseline.py-647-
    scripts/faultseg3d_baseline.py-648-    best = torch.load(run_dir / "best.pt", map_location=device, weights_only=False)
    scripts/faultseg3d_baseline.py:649:    model.load_state_dict(best["model"])
    scripts/faultseg3d_baseline.py:650:    _, validation_histogram, _ = evaluate(
    scripts/faultseg3d_baseline.py-651-        model,
    scripts/faultseg3d_baseline.py-652-        val_loader,
    scripts/faultseg3d_baseline.py-653-        device,
    --
    scripts/faultseg3d_baseline.py-656-        histogram_bins=args.histogram_bins,
    scripts/faultseg3d_baseline.py-657-    )
    scripts/faultseg3d_baseline.py-658-    selected_threshold = validation_histogram.best_dice_threshold()
    scripts/faultseg3d_baseline.py:659:    validation_final, _, validation_rows = evaluate(
    scripts/faultseg3d_baseline.py-660-        model,
    scripts/faultseg3d_baseline.py-661-        val_loader,
    scripts/faultseg3d_baseline.py-662-        device,
    --
    scripts/faultseg3d_baseline.py-665-        histogram_bins=args.histogram_bins,
    scripts/faultseg3d_baseline.py-666-        save_per_volume=run_dir / "validation_per_volume.csv",
    scripts/faultseg3d_baseline.py-667-        compute_structural=True,
    scripts/faultseg3d_baseline.py:668:        measure_inference=True,
    scripts/faultseg3d_baseline.py-669-    )
    scripts/faultseg3d_baseline.py:670:    test_final, _, test_rows = evaluate(
    scripts/faultseg3d_baseline.py-671-        model,
    scripts/faultseg3d_baseline.py:672:        test_loader,
    scripts/faultseg3d_baseline.py-673-        device,
    scripts/faultseg3d_baseline.py-674-        amp_enabled,
    scripts/faultseg3d_baseline.py-675-        threshold=selected_threshold,
    scripts/faultseg3d_baseline.py-676-        histogram_bins=args.histogram_bins,
    scripts/faultseg3d_baseline.py-677-        save_per_volume=run_dir / "test_per_volume.csv",
    scripts/faultseg3d_baseline.py-678-        compute_structural=True,
    scripts/faultseg3d_baseline.py:679:        measure_inference=True,
    scripts/faultseg3d_baseline.py-680-    )
    scripts/faultseg3d_baseline.py-681-    result = {
    scripts/faultseg3d_baseline.py-682-        "best_epoch": int(best["epoch"]),
    --
    scripts/faultseg3d_baseline.py-720-    parser.add_argument(
    scripts/faultseg3d_baseline.py-721-        "--loss", choices=("b0_bce", "b1_weighted_dice"), default="b0_bce"
    scripts/faultseg3d_baseline.py-722-    )
    scripts/faultseg3d_baseline.py:723:    parser.add_argument("--data-root", default="data/faultseg3d")
    scripts/faultseg3d_baseline.py:724:    parser.add_argument("--manifest-root", default="data/manifests")
    scripts/faultseg3d_baseline.py-725-    parser.add_argument("--run-dir", default="runs/faultseg3d_b0_seed42")
    scripts/faultseg3d_baseline.py-726-    parser.add_argument("--epochs", type=int, default=100)
    scripts/faultseg3d_baseline.py-727-    parser.add_argument("--batch-size", type=int, default=1)
    
    === ZERO-SHOT READINESS SUMMARY ===
    Baseline checkpoint exists: True
    Processed Thebe directory exists: True
    Processed Thebe array files: 18
    Existing Thebe-specific evaluator: False
    
    No training or inference was performed by this audit.
    
    === AUDIT LOG SAVED ===
    reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.log
    ]633;D;0]633;P;Cwd=/home/khavarj/projects/fault_detection[?2004h]633;A]0;khavarj@data-server: ~/projects/fault_detection[01;32mkhavarj@data-server[00m:[01;34m~/projects/fault_detection[00m$ ]633;B
    [?2004l]633;E;;e507cf66-16bb-4595-ab9c-61e579cc758d]633;C]633;D]633;P;Cwd=/home/khavarj/projects/fault_detection[?2004h]633;A]0;khavarj@data-server: ~/projects/fault_detection[01;32mkhavarj@data-server[00m:[01;34m~/projects/fault_detection[00m$ ]633;B[7mcd ~/projects/fault_detection || exit 1[27m
    [7mset -euo pipefail[27m
    
    [7mSOURCE_LOG="reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.log"[27m
    [7mOUTPUT_MD="reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.md"[27m
    
    [7mif [ ! -f "$SOURCE_LOG" ]; then[27m
    [7m    echo "ERROR: Missing audit log: $SOURCE_LOG"[27m
    [7m    exit 1[27m
    [7mfi[27m
    
    [7m{[27m
    [7m    echo "# Thebe Zero-Shot Compatibility Audit"[27m
    [7m    echo[27m
    [7m    echo "- Project: \`$(pwd)\`"[27m
    [7m    echo "- Source log: \`$SOURCE_LOG\`"[27m
    [7m    echo "- Generated: $(date --iso-8601=seconds)"[27m
    [7m    echo[27m
    [7m    echo "## Complete audit output"[27m
    [7m    echo[27m
    [7m    # Indenting every line creates a Markdown code block.[27m
    [7m    sed 's/^/    /' "$SOURCE_LOG"[27m
    [7m} > "$OUTPUT_MD"[27m
    
    [7mecho "=== MARKDOWN REPORT CREATED ==="[27m
    [7mls -lh "$OUTPUT_MD"[27m
    [7mwc -l "$OUTPUT_MD"[27m
    [7msha256sum "$OUTPUT_MD"[27m
    
    [7mecho[27m
    [7mecho "Attach this file:"[27m
    [7mecho "$OUTPUT_MD"[27m[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A[A]633;A]0;khavarj@data-server: ~/projects/fault_detection[01;32mkhavarj@data-server[00m:[01;34m~/projects/fault_detection[00m$ ]633;Bcd ~/projects/fault_detection || exit 1
    set -euo pipefail
    
    SOURCE_LOG="reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.log"
    OUTPUT_MD="reports/data_audit/thebe_zero_shot_compatibility_20261005_090534.md"
    
    if [ ! -f "$SOURCE_LOG" ]; then
        echo "ERROR: Missing audit log: $SOURCE_LOG"
        exit 1
    fi
    
    {
        echo "# Thebe Zero-Shot Compatibility Audit"
        echo
        echo "- Project: \`$(pwd)\`"
        echo "- Source log: \`$SOURCE_LOG\`"
        echo "- Generated: $(date --iso-8601=seconds)"
        echo
        echo "## Complete audit output"
        echo
        # Indenting every line creates a Markdown code block.
        sed 's/^/    /' "$SOURCE_LOG"
    } > "$OUTPUT_MD"
    
    echo "=== MARKDOWN REPORT CREATED ==="
    ls -lh "$OUTPUT_MD"
    wc -l "$OUTPUT_MD"
    sha256sum "$OUTPUT_MD"
    
    echo
    echo "Attach this file:"
    echo "$OUTPUT_MD"
    [?2004l]633;E;cd ~/projects/fault_detection;e507cf66-16bb-4595-ab9c-61e579cc758d]633;C