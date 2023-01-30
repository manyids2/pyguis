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

    iheight: int = 200
    iwidth: int = 200

    show_images = True
    n_rows: int = 0

    current: int = 1
    n_pages: int = 1
    n_per_page: int = 5


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

        self.settings = Settings()
        self.load_csv()

        dpg.create_context()

    @classmethod
    def from_args(cls, args):
        image_columns = args.image_columns.split("+")
        return cls(args.csv_path, image_columns)

    def set_page(self):
        s = self.settings
        start = (s.current - 1) * s.n_per_page
        end = min(s.current * s.n_per_page, len(self.df))
        self.rows = self.df.iloc[start:end, :]

    def load_csv(self):
        self.df = pd.DataFrame(pd.read_csv(self.csv_path))
        self.columns = list(self.df.columns)
        s = self.settings
        s.n_rows = len(self.df)
        s.current = 1
        s.n_pages = int(np.ceil(len(self.df) / s.n_per_page))
        self.set_page()

    def setup_window(self):
        width, height = self.settings.width, self.settings.height
        dpg.add_window(
            label="urlimages",
            width=width,
            height=height,
            pos=(0, 0),
            tag="primary_window",
        )

    @staticmethod
    def key_press_handler(sender, app_data, user_data):
        del sender
        print(f"key pressed is: {app_data}")
        # q : quit
        if app_data == 81:
            dpg.stop_dearpygui()
        # r : reload
        if app_data == 82:
            user_data.reload()

    @staticmethod
    def show_hide_handler(sender, app_data, user_data):
        del sender
        if app_data == "hide":
            user_data.settings.show_images = False
        elif app_data == "show":
            user_data.settings.show_images = True
        user_data.render()

    @staticmethod
    def csv_path_handler(sender, app_data, user_data):
        del sender
        user_data.csv_path = Path(app_data)

    @staticmethod
    def handle_first(sender, app_data, user_data):
        del sender, app_data
        user_data.settings.current = 1
        user_data.render()

    @staticmethod
    def handle_prev(sender, app_data, user_data):
        del sender, app_data
        user_data.settings.current = max(1, user_data.settings.current - 1)
        user_data.render()

    @staticmethod
    def handle_next(sender, app_data, user_data):
        del sender, app_data
        user_data.settings.current = min(
            user_data.settings.n_pages, user_data.settings.current + 1
        )
        user_data.render()

    @staticmethod
    def handle_last(sender, app_data, user_data):
        del sender, app_data
        user_data.settings.current = user_data.settings.n_pages
        user_data.render()

    def setup_handlers(self):
        with dpg.handler_registry():
            dpg.add_key_press_handler(callback=self.key_press_handler, user_data=self)

    def setup_textures(self):
        # Set heights and widths to be constants
        width, height = self.settings.iwidth, self.settings.iheight
        self.textures = {}
        for idx in range(self.settings.n_per_page):
            self.textures[idx] = {}
            with dpg.texture_registry(show=False):
                for column in self.image_columns:
                    self.textures[idx][column] = np.zeros(
                        [height, width, 3], dtype=float
                    ).flatten()
                    dpg.add_raw_texture(
                        width=width,
                        height=height,
                        default_value=self.textures[idx][column],  # type: ignore
                        format=dpg.mvFormat_Float_rgb,
                        tag=f"image-{idx}-{column}",
                    )

    def reload_textures(self):
        # Set heights and widths to be constants
        width, height = self.settings.iwidth, self.settings.iheight
        for idx in range(self.settings.n_per_page):
            _idx = (self.settings.current - 1) * self.settings.n_per_page + idx
            if _idx >= self.settings.n_rows:
                break
            row = self.rows.iloc[idx, :]
            for column in self.image_columns:
                image = image_from_url(f"{row.base_url}/{row.image}")
                image = image.resize((width, height))
                np.copyto(
                    self.textures[idx][column],
                    (np.array(image).astype(float) / 255).flatten(),
                )
                print(f"Set: {idx}, {_idx}, {column}, {image}")

    def render_settings(self):
        with dpg.group(label="settings", parent="primary_window"):
            with dpg.table(header_row=False):
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

    def render_pages(self):
        with dpg.group(label="pages", parent="primary_window", tag="pages_group"):
            with dpg.table(header_row=False):
                dpg.add_table_column()  # First
                dpg.add_table_column()  # Prev
                dpg.add_table_column()  # Current
                dpg.add_table_column()  # Total
                dpg.add_table_column()  # Next
                dpg.add_table_column()  # Last
                with dpg.table_row():
                    dpg.add_button(
                        label="First",
                        user_data=self,
                        callback=self.handle_first,
                    )
                    dpg.add_button(
                        label="Prev",
                        user_data=self,
                        callback=self.handle_prev,
                    )
                    dpg.add_text(
                        f"{self.settings.current}",
                        # callback=self.handle_current,
                    )
                    dpg.add_text(
                        f" / {self.settings.n_pages}",
                    )
                    dpg.add_button(
                        label="Next",
                        user_data=self,
                        callback=self.handle_next,
                    )
                    dpg.add_button(
                        label="Last",
                        user_data=self,
                        callback=self.handle_last,
                    )

    def reload(self):
        self.load_csv()
        self.render()

    def render(self):
        dpg.delete_item("pages_group")
        dpg.delete_item("table_group")
        self.set_page()
        self.render_pages()
        self.reload_textures()
        with dpg.group(tag="table_group", parent="primary_window"):
            with dpg.table(header_row=True, tag="main_table"):
                for column in self.columns:
                    dpg.add_table_column(label=column)

                for idx in range(len(self.rows)):
                    with dpg.table_row(tag=f"table__row-{idx}"):
                        row = self.rows.iloc[idx, :]
                        for column in self.columns:
                            tag = f"table__cell-{idx}-{column}"
                            is_image = column in self.image_columns
                            if is_image and self.settings.show_images:
                                dpg.add_image(
                                    texture_tag=f"image-{idx}-{column}", tag=tag
                                )
                            else:
                                dpg.add_text(row[column], tag=tag)

    def run(self):
        self.setup_window()
        self.setup_handlers()
        self.setup_textures()
        self.render_settings()
        self.render()

        dpg.setup_dearpygui()

        width, height = self.settings.width, self.settings.height
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
