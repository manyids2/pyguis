from dataclasses import dataclass
import dearpygui.dearpygui as dpg
from pyguis.widgets.layout import Layout, LayoutSettings


@dataclass
class AppState:
    show_images: bool = True
    base_url: str = "http://localhost:5555"
    csv_file: str = "./data/images.csv"


class App(Layout):
    settings = LayoutSettings()
    appstate = AppState()

    def __init__(self):
        super().__init__(self.settings)

    def reload_csv(self):
        print(self.appstate.__dict__)
        print(f"Reloaded csv")

    @staticmethod
    def handle_reload_csv(sender, app_data, user_data):
        del sender, app_data
        user_data.appstate.csv_file = dpg.get_value("sidebar__csv_file")
        user_data.reload_csv()

    @staticmethod
    def handle_show_images(sender, app_data, user_data):
        del sender
        user_data.appstate.show_images = app_data
        user_data.settings.changed = True

    @staticmethod
    def handle_base_url(sender, app_data, user_data):
        del sender, app_data
        user_data.appstate.base_url = dpg.get_value("sidebar__base_url")
        user_data.settings.changed = True

    def render_navbar(self):
        with dpg.group(label="navbar", parent="primary_window", tag="layout__navbar"):
            dpg.add_text("navbar")
            dpg.add_separator()

    def render_sidebar(self):
        if not self.settings.show_sidebar:
            return

        with dpg.window(
            label="sidebar",
            tag="layout__sidebar",
            no_title_bar=True,
            pos=(self.settings.width * 2 // 3, 0),
            height=self.settings.height,
            width=self.settings.width // 3,
        ):
            dpg.add_text("sidebar")
            dpg.add_separator()

            # CSV file
            dpg.add_text("CSV file")
            dpg.add_input_text(
                default_value=self.appstate.csv_file,
                tag="sidebar__csv_file",
            )
            dpg.add_button(
                label="Reload CSV",
                callback=self.handle_reload_csv,
                user_data=self,
            )
            dpg.add_separator()

            # Show images
            dpg.add_checkbox(
                label="Show images",
                user_data=self,
                callback=self.handle_show_images,
                default_value=self.appstate.show_images,
            )
            dpg.add_separator()

            # Base url
            dpg.add_input_text(
                label="Base url",
                user_data=self,
                default_value=self.appstate.base_url,
                tag="sidebar__base_url",
            )
            dpg.add_button(
                label="Reload images",
                callback=self.handle_base_url,
                user_data=self,
            )
            dpg.add_separator()


if __name__ == "__main__":
    app = App()
    app.run()
