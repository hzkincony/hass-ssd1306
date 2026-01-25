---
name: bdf-to-pil
description: Convert BDF bitmap fonts to PIL bitmap font files (.pil + .pbm). Use when a user asks to convert BDF fonts for Pillow, or when Pillow cannot load a .bdf and requires .pil/.pbm.
---

# Convert BDF to PIL bitmap font

## Workflow

1. Confirm the BDF input path and desired output basename.
2. Run the conversion script to generate `.pil` and `.pbm` files.
3. Report the output paths and how to load the `.pil` file in code.

## Command

Use the bundled script:

```bash
python scripts/convert_bdf_to_pil.py /path/to/font.bdf
```

Optional output basename:

```bash
python scripts/convert_bdf_to_pil.py /path/to/font.bdf /path/to/output_basename
```

## Notes

- Output files are `<basename>.pil` and `<basename>.pbm`.
- For Pillow, load the `.pil` file and keep the `.pbm` next to it.
