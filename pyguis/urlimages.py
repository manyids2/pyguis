from rich import print
from pathlib import Path

import numpy as np
import pandas as pd
import dearpygui.dearpygui as dpg

from pyguis.utils.images import image_from_url


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--csv_path", default="./data/images.csv", type=Path)
    parser.add_argument("--image_columns", default="image", type=str)
    args = parser.parse_args()

    image_columns = args.image_columns.split("+")
    df = pd.DataFrame(pd.read_csv(args.csv_path))
    columns = list(df.columns)

    show_images = True

    def key_press_handler(sender, app_data, user_data):
        del sender, user_data
        print(f"key pressed is: {app_data}")
        # q : quit
        if app_data == 81:
            dpg.stop_dearpygui()

    dpg.create_context()
    with dpg.handler_registry():
        dpg.add_key_press_handler(callback=key_press_handler)

    for _, row in df.iterrows():
        image = image_from_url(f"{row.base_url}/{row.image}")
        with dpg.texture_registry(show=False):
            dpg.add_raw_texture(
                width=image.size[0],
                height=image.size[1],
                default_value=(np.array(image).astype(float) / 255.0).flatten(),  # type: ignore
                format=dpg.mvFormat_Float_rgb,
                tag=row.image,
            )

    def render():
        with dpg.group(tag=f"{args.csv_path}", parent="primary_window"):
            with dpg.table(header_row=True, tag="main_table"):
                for column in visible:
                    dpg.add_table_column(label=column)

                # add_table_next_column will jump to the next row
                # once it reaches the end of the columns
                # table next column use slot 1
                for i in range(len(df)):
                    with dpg.table_row(tag=f"table__row-{i}"):
                        row = df.iloc[i, :]
                        for column in visible:
                            tag = f"table__cell-{i}-{column}"
                            if (column in image_columns) and show_images:
                                dpg.add_image(texture_tag=row.image, tag=tag)
                            else:
                                dpg.add_text(row[column], tag=tag)

    def show_hide(sender, app_data, user_data):
        del sender, user_data
        global show_images
        if app_data == "hide":
            dpg.delete_item(f"{args.csv_path}")
            show_images = False
            render()
        elif app_data == "show":
            dpg.delete_item(f"{args.csv_path}")
            show_images = True
            render()
        else:
            print(f"eh?")

    with dpg.window(
        label="urlimages",
        width=600,
        height=600,
        pos=(0, 0),
        tag="primary_window",
    ):
        # Show / hide images
        with dpg.group(label="settings"):
            dpg.add_radio_button(
                items=["show", "hide"],
                tag="settings__show_images",
                before="Show images",
                callback=show_hide,
            )

        visible = list(filter(lambda x: x != "base_url", columns))
        render()

    dpg.setup_dearpygui()

    dpg.create_viewport(title="pyguis", width=600, height=600)
    dpg.show_viewport()
    dpg.set_primary_window("primary_window", True)

    # below replaces, start_dearpygui()
    while dpg.is_dearpygui_running():
        dpg.render_dearpygui_frame()
