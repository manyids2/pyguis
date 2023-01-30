from rich import print
from pathlib import Path

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--csv_path", default="./data/images.csv", type=Path)
    parser.add_argument("--image_columns", default="image", type=str)
    args = parser.parse_args()

    image_columns = args.image_columns.split("+")
    print(image_columns)
