from typing import List, Optional
from rich import print
from pathlib import Path
from dataclasses import dataclass

import numpy as np
import pandas as pd
import dearpygui.dearpygui as dpg

from pyguis.utils.images import image_from_url


@dataclass
class Settings:
    height: int = 1000
    width: int = 1000

    show_images = True


settings = Settings()


class App:
    def __init__(
        self,
        csv_path: Path,
        image_columns: List[str],
        metadata_path: Optional[Path] = None,
    ) -> None:
        self.csv_path = csv_path
        self.metadata_path = metadata_path
        self.image_columns = image_columns

        self.load_csv()

        dpg.create_context()

    @classmethod
    def from_args(cls, args):
        image_columns = args.image_columns.split("+")
        return cls(args.csv_path, image_columns)

    def load_csv(self):
        self.df = pd.DataFrame(pd.read_csv(self.csv_path))
        self.columns = list(self.df.columns)

    def setup_window(self):
        width, height = settings.width, settings.height
        dpg.add_window(
            label="urlimages",
            width=width,
            height=height,
            pos=(0, 0),
            tag="primary_window",
        )

    @staticmethod
    def key_press_handler(sender, app_data, user_data):
        del sender, user_data
        print(f"key pressed is: {app_data}")
        # q : quit
        if app_data == 81:
            dpg.stop_dearpygui()

    @staticmethod
    def show_hide_handler(sender, app_data, user_data):
        del sender
        if app_data == "hide":
            settings.show_images = False
        elif app_data == "show":
            settings.show_images = True
        user_data.render()

    @staticmethod
    def csv_path_handler(sender, app_data, user_data):
        del sender
        user_data.csv_path = Path(app_data)

    def setup_handlers(self):
        with dpg.handler_registry():
            dpg.add_key_press_handler(callback=self.key_press_handler)

    def setup_textures(self):
        for _, row in self.df.iterrows():
            image = image_from_url(f"{row.base_url}/{row.image}")
            with dpg.texture_registry(show=False):
                dpg.add_raw_texture(
                    width=image.size[0],
                    height=image.size[1],
                    default_value=(np.array(image).astype(float) / 255.0).flatten(),  # type: ignore
                    format=dpg.mvFormat_Float_rgb,
                    tag=row.image,
                )

    def render_settings(self):
        with dpg.group(label="settings", parent="primary_window"):
            with dpg.table():
                dpg.add_table_column()  # Show/hide
                dpg.add_table_column()  # csv_file
                dpg.add_table_column()  # reload csv
                with dpg.table_row():
                    dpg.add_radio_button(
                        label="show_images",
                        items=["show", "hide"],
                        tag="settings__show_images",
                        user_data=self,
                        callback=self.show_hide_handler,
                    )
                    dpg.add_input_text(
                        label="csv_path",
                        default_value=f"{self.csv_path}",
                        callback=self.csv_path_handler,
                        user_data=self,
                    )
                    dpg.add_button(label="Reload csv", callback=self.reload)

    def reload(self):
        self.load_csv()
        self.render()

    def render(self):
        dpg.delete_item("table_group")
        with dpg.group(tag="table_group", parent="primary_window"):
            with dpg.table(header_row=True, tag="main_table"):
                for column in self.columns:
                    dpg.add_table_column(label=column)

                for i in range(len(self.df)):
                    with dpg.table_row(tag=f"table__row-{i}"):
                        row = self.df.iloc[i, :]
                        for column in self.columns:
                            tag = f"table__cell-{i}-{column}"
                            is_image = column in self.image_columns
                            if is_image and settings.show_images:
                                dpg.add_image(texture_tag=row.image, tag=tag)
                            else:
                                dpg.add_text(row[column], tag=tag)

    def run(self):
        self.setup_window()
        self.setup_handlers()
        self.setup_textures()
        self.render_settings()
        self.render()

        dpg.setup_dearpygui()

        width, height = settings.width, settings.height
        dpg.create_viewport(title="pyguis", width=width, height=height)
        dpg.show_viewport()
        dpg.set_primary_window("primary_window", True)

        while dpg.is_dearpygui_running():
            dpg.render_dearpygui_frame()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--csv_path", default="./data/images.csv", type=Path)
    parser.add_argument("--image_columns", default="image", type=str)
    args = parser.parse_args()

    app = App.from_args(args)
    app.run()
