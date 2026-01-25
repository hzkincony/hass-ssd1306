from __future__ import annotations

import sys
from pathlib import Path

from PIL import BdfFontFile


def main() -> int:
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python convert_bdf_to_pil.py <font.bdf> [output_basename]")
        return 2

    src = Path(sys.argv[1])
    if not src.exists():
        print(f"BDF file not found: {src}")
        return 1

    if len(sys.argv) == 3:
        dst = Path(sys.argv[2])
    else:
        dst = src.with_suffix("")

    with src.open("rb") as fp:
        font = BdfFontFile.BdfFontFile(fp)
    font.save(str(dst))

    print(f"Wrote: {dst.with_suffix('.pil')}")
    print(f"Wrote: {dst.with_suffix('.pbm')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
