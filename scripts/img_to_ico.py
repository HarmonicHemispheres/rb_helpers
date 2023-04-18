"""
# ----------------- OVERVIEW ----------------- #
converts a image file like .png or .jpg to .ico

# ----------------- DETAILS ----------------- #
VERSION = 0.1.0

# ----------------- INSTALLS ----------------- #
> pip install rich Pillow typer

# ----------------- USAGE ----------------- #
# BASIC
> python img_to_ico.py <PATH>

# CUSTOM DIMENSIONS
> python img_to_ico.py <PATH> --px-dim 48
> python img_to_ico.py <PATH> --px-dim 256

# CUSTOM OUTFILE PATH
> python img_to_ico.py <PATH> --out <PATH>

"""

import rich
import typer
from pathlib import Path
from PIL import Image

def main(img: str, px_dim: int=32, out:Path = None):
    img_obj = Image.open(img)
    if out:
        new_path = Path(out)
    else:
        new_img = Path(img)
        new_path = new_img.parent / (new_img.name + '.ico')
    img_obj.save(new_path, format='ICO', sizes=[(px_dim, px_dim)])

    rich.print(f"\nSaved ico file @ {new_path}")


if __name__ == "__main__":
    typer.run(main)
