import argparse

import sys
import wx

from g6_cli import G6Api
from g6_cli.g6_api import DEFAULT_MODEL_PATH
from g6_gui.g6_console import RedirectText
from g6_gui.g6_tab_decoder import DecoderTab
from g6_gui.g6_tab_lighting import LightingTab
from g6_gui.g6_tab_mixer import MixerTab
from g6_gui.g6_tab_playback import PlaybackTab
from g6_gui.g6_tab_recording import RecordingTab
from g6_gui.g6_tab_sbx import SbxTab
from g6_gui.g6_util import read_png_from_file

VERSION = '1.1.0a4'


class Model:
    def __init__(self, dry_run: bool, debug: bool, persist_model: bool):
        self.__view: View | None = None
        self.__g6_api: G6Api | None = None
        self.__g6_status: str = MainGuiFrame.TEXT_NOT_FOUND
        self.__hid_interface_status: str = MainGuiFrame.TEXT_UNAVAILABLE
        self.__audio_interface_status: str = MainGuiFrame.TEXT_UNAVAILABLE_NOT_CLAIMED
        self.__dry_run = dry_run
        self.__debug = debug
        self.__persist_model = persist_model

    def bind(self, view: "View"):
        self.__view = view

    def set_g6_api(self, g6_api: G6Api | None):
        self.__g6_api = g6_api

    def get_g6_api(self) -> G6Api | None:
        return self.__g6_api

    def is_dry_run(self) -> bool:
        return self.__dry_run

    def is_debug(self) -> bool:
        return self.__debug

    def is_persist_model(self) -> bool:
        return self.__persist_model

    def set_g6_status(self, status: str):
        self.__g6_status = status
        self.__view.set_g6_status_label(status)

    def set_hid_interface_status(self, status: str):
        self.__hid_interface_status = status
        self.__view.set_hid_interface_status_label(status)

    def set_audio_interface_status(self, status: str):
        self.__audio_interface_status = status
        self.__view.set_audio_interface_status_label(status)


class View:
    def __init__(self):
        self.__controller: Controller | None = None
        self.__frame: MainGuiFrame | None = None

        self.__lbl_status_value = None
        self.__lbl_hid_interface_status_value = None
        self.__lbl_audio_interface_status_value = None

        self.__notebook = None
        self.__tab_sbx = None
        self.__tab_playback = None
        self.__tab_recording = None
        self.__tab_decoder = None
        self.__tab_mixer = None
        self.__tab_lighting = None

        self.__txt_console = None
        self.__placeholder = None
        self.__btn_toggle_console = None

    def bind(self, controller: "Controller"):
        self.__controller = controller

    def create(self, frame: "MainGuiFrame") -> None:
        self.__frame = frame

        panel_main = wx.Panel(frame)
        vbox_main = wx.BoxSizer(wx.VERTICAL)
        panel_main.SetSizer(vbox_main)

        # G6 status composite
        cmp_status = self.__create_status_composite(panel_main)
        vbox_main.Add(cmp_status, flag=wx.ALL, proportion=0, border=5)

        # create notebook
        self.__notebook = self.__create_notebook(panel_main)
        vbox_main.Add(self.__notebook, flag=wx.EXPAND | wx.ALL, proportion=1, border=5)

        # create console panel
        panel_console = self.__create_console_panel(panel_main)
        vbox_main.Add(panel_console, flag=wx.EXPAND | wx.ALL, proportion=10, border=5)

        # create footer
        panel_footer = self.__create_footer(panel_main)
        vbox_main.Add(panel_footer, flag=wx.ALL, proportion=0, border=5)

        frame.set_panel_main(panel_main)
        frame.set_txt_console(self.__txt_console)

    def __create_status_composite(self, parent: wx.Panel) -> wx.Panel:
        panel = wx.Panel(parent)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        panel.SetSizer(hbox)

        # G6 status
        lbl_status = wx.StaticText(panel, label="G6 Status: ")
        self.__set_label_bold(lbl_status)
        hbox.Add(lbl_status, flag=wx.TOP | wx.BOTTOM | wx.LEFT | wx.ALIGN_CENTER_VERTICAL, border=5)

        self.__lbl_status_value = wx.StaticText(panel, label=MainGuiFrame.TEXT_NOT_FOUND, style=wx.ALIGN_LEFT)
        self.__lbl_status_value.SetMinSize(self.__lbl_status_value.GetBestSize())
        self.__apply_status_color(self.__lbl_status_value, self.__lbl_status_value.GetLabel())
        hbox.Add(self.__lbl_status_value, flag=wx.TOP | wx.BOTTOM | wx.ALIGN_CENTER_VERTICAL, border=5)

        # separator
        hbox.Add(wx.StaticText(panel, label="|"), flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=5)

        # HID interface
        lbl_hid_interface_status = wx.StaticText(panel, label="HID Interface: ")
        self.__set_label_bold(lbl_hid_interface_status)
        hbox.Add(lbl_hid_interface_status, flag=wx.TOP | wx.BOTTOM | wx.ALIGN_CENTER_VERTICAL, border=5)

        self.__lbl_hid_interface_status_value = wx.StaticText(panel, label=MainGuiFrame.TEXT_UNAVAILABLE,
                                                              style=wx.ALIGN_LEFT)
        self.__lbl_hid_interface_status_value.SetMinSize(self.__lbl_hid_interface_status_value.GetBestSize())
        self.__apply_status_color(
            self.__lbl_hid_interface_status_value,
            self.__lbl_hid_interface_status_value.GetLabel(),
        )
        hbox.Add(self.__lbl_hid_interface_status_value, flag=wx.TOP | wx.BOTTOM | wx.ALIGN_CENTER_VERTICAL, border=5)

        # separator
        hbox.Add(wx.StaticText(panel, label="|"), flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=5)

        # Audio interface
        lbl_audio_interface_status = wx.StaticText(panel, label="Audio Interface: ")
        self.__set_label_bold(lbl_audio_interface_status)
        hbox.Add(lbl_audio_interface_status, flag=wx.TOP | wx.BOTTOM | wx.ALIGN_CENTER_VERTICAL, border=5)

        self.__lbl_audio_interface_status_value = wx.StaticText(
            panel,
            label=MainGuiFrame.TEXT_UNAVAILABLE_NOT_CLAIMED,
            style=wx.ALIGN_LEFT,
        )
        self.__lbl_audio_interface_status_value.SetMinSize(self.__lbl_audio_interface_status_value.GetBestSize())
        self.__apply_status_color(
            self.__lbl_audio_interface_status_value,
            self.__lbl_audio_interface_status_value.GetLabel(),
        )
        hbox.Add(
            self.__lbl_audio_interface_status_value,
            flag=wx.TOP | wx.RIGHT | wx.BOTTOM | wx.ALIGN_CENTER_VERTICAL,
            border=5,
        )

        return panel

    def __create_notebook(self, parent: wx.Panel) -> wx.Notebook:

        icon_width = 24
        image_list = wx.ImageList(width=icon_width, height=icon_width, initialCount=6)
        sbx_image_id = image_list.Add(bitmap=read_png_from_file(
            file_name=f"notebook_sbx_{icon_width}.png", expected_width=icon_width))
        playback_image_id = image_list.Add(bitmap=read_png_from_file(
            file_name=f"notebook_playback_{icon_width}.png", expected_width=icon_width))
        recording_image_id = image_list.Add(bitmap=read_png_from_file(
            file_name=f"notebook_recording_{icon_width}.png", expected_width=icon_width))
        decoder_image_id = image_list.Add(bitmap=read_png_from_file(
            file_name=f"notebook_decoder_{icon_width}.png", expected_width=icon_width))
        mixer_image_id = image_list.Add(bitmap=read_png_from_file(
            file_name=f"notebook_mixer_{icon_width}.png", expected_width=icon_width))
        lighting_image_id = image_list.Add(bitmap=read_png_from_file(
            file_name=f"notebook_lighting_{icon_width}.png", expected_width=icon_width))

        notebook = wx.Notebook(parent)
        notebook.SetImageList(image_list)

        self.__tab_sbx = SbxTab()
        notebook.AddPage(page=self.__tab_sbx.create(notebook), text=' SBX-Profile', imageId=sbx_image_id)

        self.__tab_playback = PlaybackTab()
        notebook.AddPage(page=self.__tab_playback.create(notebook), text=" Playback", imageId=playback_image_id)

        self.__tab_recording = RecordingTab()
        notebook.AddPage(page=self.__tab_recording.create(notebook), text=" Recording", imageId=recording_image_id)

        self.__tab_decoder = DecoderTab()
        notebook.AddPage(page=self.__tab_decoder.create(notebook), text="Decoder", imageId=decoder_image_id)

        self.__tab_mixer = MixerTab(self.__frame)
        notebook.AddPage(page=self.__tab_mixer.create(notebook), text=" Mixer", imageId=mixer_image_id)

        self.__tab_lighting = LightingTab()
        notebook.AddPage(page=self.__tab_lighting.create(notebook), text=" Lighting", imageId=lighting_image_id)

        return notebook

    def __create_footer(self, parent: wx.Panel) -> wx.Panel:
        panel_footer = wx.Panel(parent)
        hbox_footer = wx.BoxSizer(wx.HORIZONTAL)
        panel_footer.SetSizer(hbox_footer)

        btn_lookup = wx.Button(panel_footer, label="1. Lookup G6")
        hbox_footer.Add(wx.StaticText(panel_footer, label=""), proportion=5)
        hbox_footer.Add(btn_lookup, flag=wx.ALL | wx.ALIGN_CENTER, border=5, proportion=1)
        hbox_footer.Add(wx.StaticText(panel_footer, label=""), proportion=5)
        btn_lookup.Bind(wx.EVT_BUTTON, lambda event: self.__controller.on_lookup(event))

        btn_claim = wx.Button(panel_footer, label="2. Claim Audio Interface")
        hbox_footer.Add(wx.StaticText(panel_footer, label=""), proportion=5)
        hbox_footer.Add(btn_claim, flag=wx.ALL | wx.ALIGN_CENTER, border=5, proportion=1)
        hbox_footer.Add(wx.StaticText(panel_footer, label=""), proportion=5)
        btn_claim.Bind(wx.EVT_BUTTON, lambda event: self.__controller.on_claim(event))

        btn_release = wx.Button(panel_footer, label="3. Release Audio Interface")
        hbox_footer.Add(wx.StaticText(panel_footer, label=""), proportion=5)
        hbox_footer.Add(btn_release, flag=wx.ALL | wx.ALIGN_CENTER, border=5, proportion=1)
        hbox_footer.Add(wx.StaticText(panel_footer, label=""), proportion=5)
        btn_release.Bind(wx.EVT_BUTTON, lambda event: self.__controller.on_release(event))

        btn_reload_audio_services = wx.Button(panel_footer, label="4. Reload Audio Services")
        hbox_footer.Add(wx.StaticText(panel_footer, label=""), proportion=5)
        hbox_footer.Add(btn_reload_audio_services, flag=wx.ALL | wx.ALIGN_CENTER, border=5, proportion=1)
        hbox_footer.Add(wx.StaticText(panel_footer, label=""), proportion=5)
        btn_reload_audio_services.Bind(wx.EVT_BUTTON,
                                       lambda event: self.__controller.on_reload_audio_services(event))

        return panel_footer

    def __create_console_panel(self, parent: wx.Panel) -> wx.Panel:
        panel = wx.Panel(parent)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        panel.SetSizer(hbox)

        self.__txt_console = wx.TextCtrl(
            panel,
            style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH2,
        )
        self.__txt_console.SetMinSize(wx.Size(-1, 150))
        self.__txt_console.Hide()

        self.__placeholder = wx.Panel(parent=panel)

        self.__btn_toggle_console = wx.Button(panel, label="", size=wx.Size(32, -1))
        self.__btn_toggle_console.SetToolTip("Show console")
        self.__btn_toggle_console.Bind(wx.EVT_BUTTON, lambda event: self.__controller.on_toggle_console(event))

        hbox.Add(self.__txt_console, flag=wx.EXPAND | wx.RIGHT, proportion=1, border=2)
        hbox.Add(self.__placeholder, flag=wx.EXPAND | wx.RIGHT, proportion=1, border=2)
        hbox.Add(self.__btn_toggle_console, flag=wx.ALIGN_BOTTOM | wx.LEFT, proportion=0, border=2)

        return panel

    def set_g6_status_label(self, label: str):
        self.__lbl_status_value.SetLabel(label)
        self.__apply_status_color(self.__lbl_status_value, label)

    def set_hid_interface_status_label(self, label: str):
        self.__lbl_hid_interface_status_value.SetLabel(label)
        self.__apply_status_color(self.__lbl_hid_interface_status_value, label)

    def set_audio_interface_status_label(self, label: str):
        self.__lbl_audio_interface_status_value.SetLabel(label)
        self.__apply_status_color(self.__lbl_audio_interface_status_value, label)

    def is_console_shown(self) -> bool:
        return self.__txt_console.IsShown()

    def show_console(self, show: bool):
        if show:
            self.__txt_console.Show()
            self.__placeholder.Hide()
            self.__btn_toggle_console.SetToolTip("Hide console")
        else:
            self.__txt_console.Hide()
            self.__placeholder.Show()
            self.__btn_toggle_console.SetToolTip("Show console")

    def update_tab_availability(self, g6_api: G6Api | None):
        self.__tab_sbx.update_availability(g6_api=g6_api)
        self.__tab_playback.update_availability(g6_api=g6_api)
        self.__tab_recording.update_availability(g6_api=g6_api)
        self.__tab_decoder.update_availability(g6_api=g6_api)
        self.__tab_mixer.update_availability(g6_api=g6_api)
        self.__tab_lighting.update_availability(g6_api=g6_api)

    @staticmethod
    def __set_label_bold(label: wx.StaticText) -> None:
        font = label.GetFont()
        if font.IsOk():
            label.SetFont(font.Bold())

    @staticmethod
    def __apply_status_color(value_label: wx.StaticText, value: str) -> None:
        normalized = value.strip().lower()

        good_values = {MainGuiFrame.TEXT_AVAILABLE, MainGuiFrame.TEXT_CLAIMED}
        bad_values = {MainGuiFrame.TEXT_NOT_FOUND, MainGuiFrame.TEXT_UNAVAILABLE,
                      MainGuiFrame.TEXT_UNAVAILABLE_NOT_CLAIMED}

        if normalized in good_values:
            value_label.SetForegroundColour(wx.Colour(0, 140, 0))  # green
        elif normalized in bad_values:
            value_label.SetForegroundColour(wx.Colour(200, 0, 0))  # red
        else:
            value_label.SetForegroundColour(wx.NullColour)  # default/theme color

        value_label.Refresh()


class Controller:
    def __init__(self):
        self.__model: Model | None = None
        self.__view: View | None = None
        self.__frame: MainGuiFrame | None = None

    def bind(self, model: Model, view: View, frame: "MainGuiFrame"):
        self.__model = model
        self.__view = view
        self.__frame = frame

    def on_lookup(self, event):
        g6_api = G6Api(dry_run=self.__model.is_dry_run(), debug=self.__model.is_debug(),
                       persist_model=self.__model.is_persist_model())
        self.__model.set_g6_api(g6_api)
        self.update_availability()

    def on_claim(self, event):
        g6_api = self.__model.get_g6_api()
        if g6_api:
            g6_api.claim_audio_interface()
            self.update_availability()

    def on_release(self, event):
        g6_api = self.__model.get_g6_api()
        if g6_api:
            g6_api.release_audio_interface()
            self.update_availability()

    def on_reload_audio_services(self, event):
        g6_api = self.__model.get_g6_api()
        if g6_api:
            g6_api.reload_audio()

    def on_toggle_console(self, event):
        if self.__view.is_console_shown():
            self.__frame.SetMinSize(MainGuiFrame.FRAME_SIZE_INITIAL)
            self.__frame.SetSize(MainGuiFrame.FRAME_SIZE_INITIAL)
            self.__view.show_console(False)
        else:
            self.__frame.SetMinSize(MainGuiFrame.FRAME_SIZE_WITH_CONSOLE)
            self.__frame.SetSize(MainGuiFrame.FRAME_SIZE_WITH_CONSOLE)
            self.__view.show_console(True)

        self.__frame.get_panel_main().Layout()

    def update_availability(self):
        g6_api = self.__model.get_g6_api()

        # update status labels
        g6_status = MainGuiFrame.TEXT_AVAILABLE if g6_api is not None else MainGuiFrame.TEXT_NOT_FOUND
        self.__model.set_g6_status(g6_status)

        hid_status = (
            MainGuiFrame.TEXT_AVAILABLE
            if g6_api is not None and g6_api.is_hid_interface_available()
            else MainGuiFrame.TEXT_UNAVAILABLE
        )
        self.__model.set_hid_interface_status(hid_status)

        audio_status = (
            MainGuiFrame.TEXT_CLAIMED
            if g6_api is not None and g6_api.is_audio_interface_available()
            else MainGuiFrame.TEXT_UNAVAILABLE_NOT_CLAIMED
        )
        self.__model.set_audio_interface_status(audio_status)

        # update tabs
        self.__view.update_tab_availability(g6_api=g6_api)


class MainGuiFrame(wx.Frame):
    TEXT_AVAILABLE = "available"
    TEXT_UNAVAILABLE = "unavailable"
    TEXT_CLAIMED = "claimed"
    TEXT_NOT_FOUND = "not found"
    TEXT_UNAVAILABLE_NOT_CLAIMED = "unavailable / not claimed"

    FRAME_SIZE_INITIAL = wx.Size(1024, 768)
    FRAME_SIZE_WITH_CONSOLE = wx.Size(FRAME_SIZE_INITIAL.width, FRAME_SIZE_INITIAL.height + 150)

    def __init__(self, dry_run: bool, debug: bool, persist_model: bool):
        super().__init__(None, title="SoundBlaster X G6 - GUI", size=MainGuiFrame.FRAME_SIZE_INITIAL)
        self.SetMinSize(MainGuiFrame.FRAME_SIZE_INITIAL)

        self.panel_main = None
        self.__txt_console = None

        self.__model = Model(dry_run=dry_run, debug=debug, persist_model=persist_model)
        self.__view = View()
        self.__controller = Controller()

        # create bindings
        self.__model.bind(self.__view)
        self.__view.bind(self.__controller)
        self.__controller.bind(self.__model, self.__view, self)

        # create view
        self.__view.create(self)

        # setup redirection
        self.__stdout_redirector = RedirectText(
            self.__txt_console,
            wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOWTEXT),
            sys.stdout
        )
        self.__stderr_redirector = RedirectText(
            self.__txt_console,
            wx.Colour(255, 69, 58) if wx.SystemSettings.GetAppearance().IsDark() else wx.Colour(200, 0, 0),
            sys.stderr
        )
        sys.stdout = self.__stdout_redirector
        sys.stderr = self.__stderr_redirector
        print("GUI: Console output redirection initialized.")

        # define component states
        self.__controller.update_availability()

    def set_panel_main(self, panel: wx.Panel):
        self.panel_main = panel

    def get_panel_main(self) -> wx.Panel:
        return self.panel_main

    def set_txt_console(self, txt_console: wx.TextCtrl):
        self.__txt_console = txt_console

    def open(self):
        self.Centre()
        self.Show()


def parse_cli_args() -> argparse.Namespace:
    """
    Parse the CLI arguments using argparse.
    :return: The parsed cli args object
    """
    parser = argparse.ArgumentParser(usage="soundblaster-x-g6-gui", description='SoundBlaster X G6 GUI')
    #
    # Device / services
    #
    general_options_group = parser.add_argument_group('General options')
    general_options_group.add_argument('--dry-run', required=False, action='store_true',
                                       help='Used to verify the available hex_line files, without making any calls against the G6 device.')
    general_options_group.add_argument('--debug', required=False, action='store_true',
                                       help='Print communication data with the G6 device to the console.')
    general_options_group.add_argument('--no-persist', required=False, action='store_true',
                                       help=f"Disables reading and writing of the current G6 state in file '{DEFAULT_MODEL_PATH}'.")
    general_options_group.add_argument('--version', action='version', version=f'soundblaster-x-g6-gui {VERSION}')

    # parse args
    args = parser.parse_args()
    return args


def main():
    # parse CLI arguments
    args = parse_cli_args()

    app = wx.App(False)
    frame = MainGuiFrame(dry_run=args.dry_run, debug=args.debug, persist_model=not args.no_persist)
    frame.open()
    app.MainLoop()
