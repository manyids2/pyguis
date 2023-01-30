from pathlib import Path

from PIL import Image
import urllib.request as request

tmp_dir = Path("/tmp/pyguis/cache")
tmp_dir.mkdir(exist_ok=True, parents=True)


def clean_url(url):
    """Make it path friendly?"""
    return url.replace(":", "-").replace("/", "-").replace(".", "-")


def image_from_url(
    url: str, tmp_dir: Path = tmp_dir, force: bool = False
) -> Image.Image:
    """Caches images in tmp_dir."""
    fname = tmp_dir / clean_url(url)
    if not fname.exists() or force:
        request.urlretrieve(url, fname)
    image = Image.open(fname)
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
