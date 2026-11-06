# Author email draft — not sent

To: Matin Mahzad <matinmahzad@yahoo.com>

Cc: Majid Bagheri <majidbagheri@ut.ac.ir>

Addresses verified from the [published corresponding-author section](https://www.nature.com/articles/s41598-026-54829-x#author-information).

Subject: Reproduction code, checkpoints, and protocol for your 3D global-attention fault-segmentation paper

Dear Dr. Mahzad and Dr. Bagheri,

I am working to reproduce your Scientific Reports paper, “Fault detection in seismic data using a true 3D global attention convolutional network with self-supervised denoising pretext training” (DOI: 10.1038/s41598-026-54829-x). I would like to match the published procedure before committing to a full training run.

Could you please help with these details?

1. Could you share the denoising-pretraining script and complete configuration, and the denoising and final segmentation checkpoints used for the reported results? The main repository refers to `pretrain_denoising.py` and `model_epoch_4.pt`, which I could not locate in its file tree. A matching code commit and checkpoint key/shape mapping would be helpful, since the separate denoising and segmentation releases appear to use different model layouts. Was the output head retained or reinitialized for segmentation?

2. Which exact Kerry-3D, Opunake-3D, and Kahu-3D processed files and sub-volumes were used? Could you provide download identifiers, crop bounds, the pretraining loss, training/validation sampling, epochs or update count, optimizer, and learning-rate schedule? An author copy of the referenced denoising paper would also help if available.

3. Could you provide the exact Thebe train/validation/test coordinates, axis ordering, label version, and normalization/no-data rules? The repository example uses a random 80/20 patch split, so I want to avoid substituting that for the published partition.

4. What was the actual global batch size, accumulation count, and optimizer-update schedule? Four devices, batch two per device, and four accumulation steps imply 32 samples per update, while the article states 16. How do the stated 11 batches per epoch relate to the patch count, and is the LR schedule advanced per batch or optimizer update?

5. Could you share the full-volume reconstruction/evaluation code, including Gaussian blending width, edge handling, and treatment of missing seismic? I understand that the published voxel metrics use probability greater than 0.5; I would like to match the scored region and avoid duplicate counting in overlaps.

An archived run configuration and the scripts that generated the reported validation and test tables would answer many of these questions directly.

Thank you for your time and for releasing your work.

Best regards,

[Your name]
