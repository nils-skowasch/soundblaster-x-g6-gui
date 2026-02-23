import wx

from g6_cli import G6Api
from src.g6_gui.g6_tab_sbx import SbxTab
from src.g6_gui.g6_tab_playback import PlaybackTab
from src.g6_gui.g6_tab_recording import RecordingTab
from src.g6_gui.g6_tab_decoder import DecoderTab
from src.g6_gui.g6_tab_mixer import MixerTab
from src.g6_gui.g6_tab_lighting import LightingTab


class AudioSettingsFrame(wx.Frame):
    TEXT_AVAILABLE = "available"
    TEXT_UNAVAILABLE = "unavailable"
    TEXT_CLAIMED = "claimed"
    TEXT_NOT_FOUND = "not found"
    TEXT_UNAVAILABLE_NOT_CLAIMED = "unavailable / not claimed"

    def __init__(self):
        super().__init__(None, title="SoundBlaster X G6 - GUI", size=wx.Size(840, 630))

        # create panel with vertical box sizer
        self.panel_main = wx.Panel(self)

        # set vbox sizer as layout manager to panel_main
        self.vbox_main = wx.BoxSizer(wx.VERTICAL)
        self.panel_main.SetSizer(self.vbox_main)

        # G6 status composite
        self.__cmp_status = self.__create_status_composite(self.panel_main)
        self.vbox_main.Add(self.__cmp_status, flag=wx.EXPAND, proportion=0, border=5)

        # create notebook
        self.__tab_sbx = None
        self.__tab_playback = None
        self.__tab_recording = None
        self.__tab_decoder = None
        self.__tab_mixer = None
        self.__tab_lighting = None
        self.notebook = self.__create_notebook(self.panel_main)
        self.vbox_main.Add(self.notebook, flag=wx.EXPAND, proportion=1, border=5)

        # create footer
        self.panel_footer = self.__create_footer(self.panel_main)
        self.vbox_main.Add(self.panel_footer, flag=wx.EXPAND, proportion=0, border=5)

        # initialize variables
        self.__g6_api: G6Api | None = None

        # define component states
        self.__update_availability()

    def open(self):
        self.Centre()
        self.Show()

    # --- Styling helpers -------------------------------------------------

    @staticmethod
    def __set_label_bold(label: wx.StaticText) -> None:
        font = label.GetFont()
        if font.IsOk():
            label.SetFont(font.Bold())

    def __apply_status_color(self, value_label: wx.StaticText, value: str) -> None:
        normalized = value.strip().lower()

        good_values = {self.TEXT_AVAILABLE, self.TEXT_CLAIMED}
        bad_values = {self.TEXT_NOT_FOUND, self.TEXT_UNAVAILABLE, self.TEXT_UNAVAILABLE_NOT_CLAIMED}

        if normalized in good_values:
            value_label.SetForegroundColour(wx.Colour(0, 140, 0))  # green
        elif normalized in bad_values:
            value_label.SetForegroundColour(wx.Colour(200, 0, 0))  # red
        else:
            value_label.SetForegroundColour(wx.NullColour)  # default/theme color

        value_label.Refresh()

    def __create_status_composite(self, parent: wx.Panel) -> wx.Panel:
        panel = wx.Panel(parent)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        panel.SetSizer(hbox)

        lbl_status = wx.StaticText(panel, label="G6 Status: ")
        self.__set_label_bold(lbl_status)
        hbox.Add(lbl_status, flag=wx.TOP | wx.BOTTOM | wx.LEFT | wx.ALIGN_CENTER_VERTICAL, border=5)

        self.__lbl_status_value = wx.StaticText(panel, label=self.TEXT_NOT_FOUND, style=wx.ALIGN_CENTER)
        self.__apply_status_color(self.__lbl_status_value, self.__lbl_status_value.GetLabel())
        hbox.Add(self.__lbl_status_value, flag=wx.TOP | wx.BOTTOM | wx.ALIGN_CENTER_VERTICAL, border=5)

        hbox.Add(wx.StaticText(panel, label="|"), flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=5)

        lbl_hid_interface_status = wx.StaticText(panel, label="HID Interface: ")
        self.__set_label_bold(lbl_hid_interface_status)
        hbox.Add(lbl_hid_interface_status, flag=wx.TOP | wx.BOTTOM | wx.ALIGN_CENTER_VERTICAL, border=5)

        self.__lbl_hid_interface_status_value = wx.StaticText(panel, label=self.TEXT_UNAVAILABLE, style=wx.ALIGN_CENTER)
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
            label=self.TEXT_UNAVAILABLE_NOT_CLAIMED,
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
        # create notebook (tab folder)
        notebook = wx.Notebook(parent)

        # create tabs
        self.__tab_sbx = SbxTab()
        notebook.AddPage(self.__tab_sbx.create(notebook), 'SBX-Profile')

        self.__tab_playback = PlaybackTab()
        notebook.AddPage(self.__tab_playback.create(notebook), "Playback")

        self.__tab_recording = RecordingTab()
        notebook.AddPage(self.__tab_recording.create(notebook), "Recording")

        self.__tab_decoder = DecoderTab()
        notebook.AddPage(self.__tab_decoder.create(notebook), "Decoder")

        self.__tab_mixer = MixerTab(self)
        notebook.AddPage(self.__tab_mixer.create(notebook), "Mixer")

        self.__tab_lighting = LightingTab()
        notebook.AddPage(self.__tab_lighting.create(notebook), "Lighting")

        return notebook

    def __create_footer(self, parent: wx.Panel) -> wx.Panel:
        def handle_btn_lookup(event):
            self.__g6_api = G6Api(dry_run=False)
            self.__update_availability()

        def handle_btn_claim(event):
            self.__g6_api.claim_audio_interface()
            self.__update_availability()

        def handle_btn_release(event):
            self.__g6_api.release_audio_interface()
            self.__update_availability()

        def handle_btn_apply(event):
            self.__g6_api.playback_mute(mute=True)

        def handle_btn_reload_alsa_and_pipewire(event):
            self.__g6_api.reload_alsa_and_pipewire()

        # create footer panel
        panel_footer = wx.Panel(parent)

        # define sizer as layout manager
        hbox_footer = wx.BoxSizer(wx.HORIZONTAL)
        panel_footer.SetSizer(hbox_footer)

        # add components to footer
        btn_lookup = wx.Button(panel_footer, label="1. Lookup G6")
        hbox_footer.Add(wx.StaticText(panel_footer, label=""), proportion=5)
        hbox_footer.Add(btn_lookup, flag=wx.ALL | wx.ALIGN_CENTER, border=5, proportion=1)
        hbox_footer.Add(wx.StaticText(panel_footer, label=""), proportion=5)
        btn_lookup.Bind(wx.EVT_BUTTON, lambda event: handle_btn_lookup(event))

        btn_claim = wx.Button(panel_footer, label="2. Claim Audio Interface")
        hbox_footer.Add(wx.StaticText(panel_footer, label=""), proportion=5)
        hbox_footer.Add(btn_claim, flag=wx.ALL | wx.ALIGN_CENTER, border=5, proportion=1)
        hbox_footer.Add(wx.StaticText(panel_footer, label=""), proportion=5)
        btn_claim.Bind(wx.EVT_BUTTON, lambda event: handle_btn_claim(event))

        btn_release = wx.Button(panel_footer, label="3. Release Audio Interface")
        hbox_footer.Add(wx.StaticText(panel_footer, label=""), proportion=5)
        hbox_footer.Add(btn_release, flag=wx.ALL | wx.ALIGN_CENTER, border=5, proportion=1)
        hbox_footer.Add(wx.StaticText(panel_footer, label=""), proportion=5)
        btn_release.Bind(wx.EVT_BUTTON, lambda event: handle_btn_release(event))

        btn_reload_alsa_and_pipewire = wx.Button(panel_footer, label="4. Reload ALSA and PipeWire")
        hbox_footer.Add(wx.StaticText(panel_footer, label=""), proportion=5)
        hbox_footer.Add(btn_reload_alsa_and_pipewire, flag=wx.ALL | wx.ALIGN_CENTER, border=5, proportion=1)
        hbox_footer.Add(wx.StaticText(panel_footer, label=""), proportion=5)
        btn_reload_alsa_and_pipewire.Bind(wx.EVT_BUTTON, lambda event: handle_btn_reload_alsa_and_pipewire(event))

        return panel_footer

    def __update_availability(self):
        # update status labels
        g6_status = self.TEXT_AVAILABLE if self.__g6_api is not None else self.TEXT_NOT_FOUND
        self.__lbl_status_value.SetLabel(g6_status)
        self.__apply_status_color(self.__lbl_status_value, g6_status)

        hid_status = (
            self.TEXT_AVAILABLE
            if self.__g6_api is not None and self.__g6_api.is_hid_interface_available()
            else self.TEXT_UNAVAILABLE
        )
        self.__lbl_hid_interface_status_value.SetLabel(hid_status)
        self.__apply_status_color(self.__lbl_hid_interface_status_value, hid_status)

        audio_status = (
            self.TEXT_CLAIMED
            if self.__g6_api is not None and self.__g6_api.is_audio_interface_available()
            else self.TEXT_UNAVAILABLE_NOT_CLAIMED
        )
        self.__lbl_audio_interface_status_value.SetLabel(audio_status)
        self.__apply_status_color(self.__lbl_audio_interface_status_value, audio_status)

        # update tabs
        self.__tab_sbx.update_availability(g6_api=self.__g6_api)
        self.__tab_playback.update_availability(g6_api=self.__g6_api)
        self.__tab_recording.update_availability(g6_api=self.__g6_api)
        self.__tab_decoder.update_availability(g6_api=self.__g6_api)
        self.__tab_mixer.update_availability(g6_api=self.__g6_api)
        self.__tab_lighting.update_availability(g6_api=self.__g6_api)


def main():
    app = wx.App(False)
    frame = AudioSettingsFrame()
    frame.open()
    app.MainLoop()
