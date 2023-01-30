from typing import List
from pathlib import Path
from dataclasses import dataclass, asdict
import pandas as pd

from pyguis.utils.images import image_from_url

@dataclass
class ImageFile:
    index: int
    name: str
    color: str
    filename: str
    base_url: str
    image: str = ""

    def __post_init__(self):
        self.image: str = f"{self.base_url}/{self.filename}"

    def get_image_columns(self) -> List[str]:
        return ["image"]


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--base_dir", default="./data", type=Path)
    parser.add_argument("--base_url", default="http://localhost:5555", type=str)
    args = parser.parse_args()

    rows = []
    for idx, image_file in enumerate(args.base_dir.glob("**/*.png")):
        imf = ImageFile(
            index=idx,
            name=image_file.name,
            color=image_file.stem,
            # relative_to is guaranteed due to way we are globbing
            filename=image_file.relative_to(args.base_dir),
            base_url=args.base_url,
        )
        image = image_from_url(imf.image)
        image.show()
        rows.append(asdict(imf))
    df = pd.DataFrame(rows)
    print(df)
