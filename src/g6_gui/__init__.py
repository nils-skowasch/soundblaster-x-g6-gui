import sys
import wx

from g6_cli import G6Api
from g6_gui.g6_console import RedirectText
from g6_gui.g6_tab_decoder import DecoderTab
from g6_gui.g6_tab_lighting import LightingTab
from g6_gui.g6_tab_mixer import MixerTab
from g6_gui.g6_tab_playback import PlaybackTab
from g6_gui.g6_tab_recording import RecordingTab
from g6_gui.g6_tab_sbx import SbxTab


class Model:
    def __init__(self):
        self.__view: View | None = None
        self.__g6_api: G6Api | None = None
        self.__g6_status: str = MainGuiFrame.TEXT_NOT_FOUND
        self.__hid_interface_status: str = MainGuiFrame.TEXT_UNAVAILABLE
        self.__audio_interface_status: str = MainGuiFrame.TEXT_UNAVAILABLE_NOT_CLAIMED

    def bind(self, view: "View"):
        self.__view = view

    def set_g6_api(self, g6_api: G6Api | None):
        self.__g6_api = g6_api

    def get_g6_api(self) -> G6Api | None:
        return self.__g6_api

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

        lbl_status = wx.StaticText(panel, label="G6 Status: ")
        self.__set_label_bold(lbl_status)
        hbox.Add(lbl_status, flag=wx.TOP | wx.BOTTOM | wx.LEFT | wx.ALIGN_CENTER_VERTICAL, border=5)

        self.__lbl_status_value = wx.StaticText(panel, label=MainGuiFrame.TEXT_NOT_FOUND, style=wx.ALIGN_CENTER)
        self.__apply_status_color(self.__lbl_status_value, self.__lbl_status_value.GetLabel())
        hbox.Add(self.__lbl_status_value, flag=wx.TOP | wx.BOTTOM | wx.ALIGN_CENTER_VERTICAL, border=5)

        hbox.Add(wx.StaticText(panel, label="|"), flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=5)

        lbl_hid_interface_status = wx.StaticText(panel, label="HID Interface: ")
        self.__set_label_bold(lbl_hid_interface_status)
        hbox.Add(lbl_hid_interface_status, flag=wx.TOP | wx.BOTTOM | wx.ALIGN_CENTER_VERTICAL, border=5)

        self.__lbl_hid_interface_status_value = wx.StaticText(panel, label=MainGuiFrame.TEXT_UNAVAILABLE,
                                                              style=wx.ALIGN_CENTER)
        self.__apply_status_color(
            self.__lbl_hid_interface_status_value,
            self.__lbl_hid_interface_status_value.GetLabel(),
        )
        hbox.Add(self.__lbl_hid_interface_status_value, flag=wx.TOP | wx.BOTTOM | wx.ALIGN_CENTER_VERTICAL, border=5)

        hbox.Add(wx.StaticText(panel, label="|"), flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=5)

        lbl_audio_interface_status = wx.StaticText(panel, label="Audio Interface: ")
        self.__set_label_bold(lbl_audio_interface_status)
        hbox.Add(lbl_audio_interface_status, flag=wx.TOP | wx.BOTTOM | wx.ALIGN_CENTER_VERTICAL, border=5)

        self.__lbl_audio_interface_status_value = wx.StaticText(
            panel,
            label=MainGuiFrame.TEXT_UNAVAILABLE_NOT_CLAIMED,
            style=wx.ALIGN_CENTER,
        )
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
        notebook = wx.Notebook(parent)

        self.__tab_sbx = SbxTab()
        notebook.AddPage(self.__tab_sbx.create(notebook), 'SBX-Profile')

        self.__tab_playback = PlaybackTab()
        notebook.AddPage(self.__tab_playback.create(notebook), "Playback")

        self.__tab_recording = RecordingTab()
        notebook.AddPage(self.__tab_recording.create(notebook), "Recording")

        self.__tab_decoder = DecoderTab()
        notebook.AddPage(self.__tab_decoder.create(notebook), "Decoder")

        self.__tab_mixer = MixerTab(self.__frame)
        notebook.AddPage(self.__tab_mixer.create(notebook), "Mixer")

        self.__tab_lighting = LightingTab()
        notebook.AddPage(self.__tab_lighting.create(notebook), "Lighting")

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

        btn_reload_alsa_and_pipewire = wx.Button(panel_footer, label="4. Reload ALSA and PipeWire")
        hbox_footer.Add(wx.StaticText(panel_footer, label=""), proportion=5)
        hbox_footer.Add(btn_reload_alsa_and_pipewire, flag=wx.ALL | wx.ALIGN_CENTER, border=5, proportion=1)
        hbox_footer.Add(wx.StaticText(panel_footer, label=""), proportion=5)
        btn_reload_alsa_and_pipewire.Bind(wx.EVT_BUTTON,
                                          lambda event: self.__controller.on_reload_alsa_and_pipewire(event))

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
        g6_api = G6Api(dry_run=True, debug=True)
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

    def on_reload_alsa_and_pipewire(self, event):
        g6_api = self.__model.get_g6_api()
        if g6_api:
            g6_api.reload_alsa_and_pipewire()

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

    def __init__(self):
        super().__init__(None, title="SoundBlaster X G6 - GUI", size=MainGuiFrame.FRAME_SIZE_INITIAL)
        self.SetMinSize(MainGuiFrame.FRAME_SIZE_INITIAL)

        self.panel_main = None
        self.__txt_console = None

        self.__model = Model()
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


def main():
    app = wx.App(False)
    frame = MainGuiFrame()
    frame.open()
    app.MainLoop()
