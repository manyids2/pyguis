import tempfile
from pathlib import Path

from PIL import Image
import urllib.request as request


def image_from_url(url: str) -> Image.Image:
    with tempfile.TemporaryFile() as tfile:
        request.urlretrieve(url, str(tfile))
        image = Image.open(str(tfile))
    return image


def gen_images(base_dir: Path) -> None:
    colors = ["red", "green", "blue"]
    for color in colors:
        image = Image.new("RGB", (64, 64), color=color)
        image.save(base_dir / f"{color}.png")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--base_dir", default="./data", type=Path)
    args = parser.parse_args()

    gen_images(args.base_dir)
