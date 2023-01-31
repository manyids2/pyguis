from argparse import Namespace
from dataclasses import dataclass

import dearpygui.dearpygui as dpg


@dataclass
class LayoutSettings:
    changed: bool = False
    width: int = 1000
    height: int = 1000
    show_sidebar: bool = True


class Layout:
    def __init__(self, settings: LayoutSettings):
        dpg.create_context()
        self.settings = settings
        self.children = ["layout__navbar", "layout__sidebar", "layout__content"]

    @property
    def state(self):
        return Namespace(
            width=self.settings.width,
            height=self.settings.height,
        )

    @staticmethod
    def key_press_handler(sender, app_data, user_data):
        del sender

        # q : quit
        if app_data == 81:
            dpg.stop_dearpygui()

        # b : sidebar
        if app_data == 66:
            user_data.settings.show_sidebar = not user_data.settings.show_sidebar
            user_data.settings.changed = True

    def setup_handlers(self):
        with dpg.handler_registry():
            dpg.add_key_press_handler(callback=self.key_press_handler, user_data=self)

    def setup_window(self):
        dpg.add_window(
            label="layout",
            width=self.settings.width,
            height=self.settings.height,
            pos=(0, 0),
            tag="primary_window",
        )

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
            pos=(self.settings.width * 3 // 4, 0),
            height=self.settings.height,
            width=self.settings.width // 4,
        ):
            dpg.add_text("sidebar")

    def render_content(self):
        with dpg.group(label="content", parent="primary_window", tag="layout__content"):
            dpg.add_text("content")

    def render(self):
        if not self.settings.changed:
            return

        # Remove existing
        for child in self.children:
            dpg.delete_item(child)

        # Reinitialize
        self.render_navbar()
        self.render_sidebar()
        self.render_content()

        # Do not redraw till next change
        self.settings.changed = False

    def run(self):
        self.setup_handlers()
        self.setup_window()
        self.settings.changed = True

        dpg.setup_dearpygui()
        width, height = self.settings.width, self.settings.height
        dpg.create_viewport(title="pyguis", width=width, height=height)
        dpg.show_viewport()
        dpg.set_primary_window("primary_window", True)

        while dpg.is_dearpygui_running():
            self.render()
            dpg.render_dearpygui_frame()


if __name__ == "__main__":
    ls = LayoutSettings()
    ll = Layout(ls)
    ll.run()
