# Thebe reference thickness and provenance audit

Date: 2026-11-02

## Question audited

For the first row of
`reports/evaluation/faultedgeformer_thebe_full_seed42_20261026/validation_casebook.png`:

- Is the pink overlay the stored Thebe validation reference?
- Did our conversion, patch reader, axis handling, or plotting thicken or shift it?
- Does the pink band's width represent the physical width of a geological fault?

## Result

The pink overlay is the official processed Thebe reference mask at the displayed
coordinate. It is expert-derived, but it is a rasterized reference annotation and
should not be interpreted as a precise physical fault-zone width or as
uncertainty-free geological truth.

The local audit found no conversion or plotting error:

- Case origin: `(x, y, z) = (0, 1920, 896)`
- Displayed survey section: `x = 127`
- Direct source in the processed validation HDF5: `val2.h5`, local section 27
- Plotted mask equals the direct HDF5 slice: **true, pixel for pixel**
- All plotted reference pixels are in valid seismic: **true**
- Positive reference pixels in the displayed section: **1,555**
- Rows containing a reference fault: **100**
- Contiguous horizontal run widths: **5 minimum, 12 median, 13 90th percentile,
  13 maximum pixels**

Horizontal run width is not exactly the surface-normal width for a dipping band,
but it confirms that this reference is a multi-pixel band rather than a one-pixel
surface.

## Why the official label is thick

The dataset authors report that fault experts from University College Dublin's
Fault Analysis Group interpreted faults as polylines on discrete 2D Petrel
cross-sections. The points could then be connected into 3D surfaces. For the
released machine-learning labels, Petrel produced fault-annotation screenshots.
Those screenshots were converted to binary grayscale, cropped to the seismic
boundary, scaled to the seismic cross-section dimensions, flipped for direction
consistency, and concatenated into a 3D NumPy volume.

That screenshot-rendering and scaling path preserves the drawn stroke as a band.
Consequently, a positive voxel means the processed annotation says a fault passes
through it; the band thickness is not a measured fault-zone aperture.

The authors also state that the annotations cover only faults with vertical
displacement greater than 20 m in a selected area and depth range of about 2–4 km.
Unlabelled pixels therefore cannot always be interpreted as proof that no smaller
or out-of-scope fault exists.

Primary source:

- Yu An et al., *A gigabyte interpreted seismic dataset for automatic fault
  recognition*: https://pmc.ncbi.nlm.nih.gov/articles/PMC8220338/

## Local pipeline evidence

`scripts/prepare_seismic_datasets.py` reads each official binary fault section and
writes `fault.astype(np.uint8)` directly to HDF5. It performs no resize,
morphological dilation, erosion, smoothing, or label interpolation.

`scripts/r100_full_run.py` reads seismic and fault arrays from the same coordinates,
pads both to the same shape, and applies the same axis reversal. The visualization
then reverses that transform and uses the same `x` cut for seismic, reference, and
prediction. The direct-HDF5 equality check above independently verifies this for
the questioned case.

## Consequence for training and evaluation

Voxel BCE/Dice training against this target rewards reproduction of its band. The
frozen validation threshold of 0.2456 can make the binary prediction wider than a
0.5 threshold, but it did not cause the reference thickness.

If the intended product is a thin fault surface, preserve the published-mask
result for comparable Thebe benchmarking and add a separate thin-surface task:

1. Prefer the original Petrel/IESX fault sticks or surfaces when available.
2. Otherwise derive a 3D centre surface from the official mask and record the
   derivation explicitly. Avoid independent 2D thinning because it can introduce
   jagged or disconnected surfaces between sections.
3. Train with centre-surface, boundary, or distance-transform supervision.
4. Evaluate with a spatial tolerance or surface-distance metric as well as the
   published exact-mask Dice.

A topology loss can help connectivity, but by itself it does not define the
desired line thickness.
