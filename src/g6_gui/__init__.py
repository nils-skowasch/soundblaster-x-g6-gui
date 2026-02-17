import wx

from g6_cli import G6Api
from src.g6_gui.g6_tab_sbx import SbxTab
from src.g6_gui.g6_tab_playback import PlaybackTab
from src.g6_gui.g6_tab_recording import RecordingTab
from src.g6_gui.g6_tab_decoder import DecoderTab
from src.g6_gui.g6_tab_mixer import MixerTab
from src.g6_gui.g6_tab_lighting import LightingTab


class AudioSettingsFrame(wx.Frame):

    def __init__(self):
        super().__init__(None, title="Audio Settings", size=wx.Size(840, 630))

        # create panel with vertical box sizer
        self.panel_main = wx.Panel(self)

        # set vbox sizer as layout manager to panel_main
        self.vbox_main = wx.BoxSizer(wx.VERTICAL)
        self.panel_main.SetSizer(self.vbox_main)

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

        def handle_btn_release(event):
            self.__g6_api.release_audio_interface()

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
        btn_lookup = wx.Button(panel_footer, label="Lookup G6")
        hbox_footer.Add(wx.StaticText(panel_footer, label=""), proportion=5)
        hbox_footer.Add(btn_lookup, flag=wx.ALL | wx.ALIGN_CENTER, border=5, proportion=1)
        hbox_footer.Add(wx.StaticText(panel_footer, label=""), proportion=5)
        btn_lookup.Bind(wx.EVT_BUTTON, lambda event: handle_btn_lookup(event))

        btn_claim = wx.Button(panel_footer, label="Claim Audio Interface")
        hbox_footer.Add(wx.StaticText(panel_footer, label=""), proportion=5)
        hbox_footer.Add(btn_claim, flag=wx.ALL | wx.ALIGN_CENTER, border=5, proportion=1)
        hbox_footer.Add(wx.StaticText(panel_footer, label=""), proportion=5)
        btn_claim.Bind(wx.EVT_BUTTON, lambda event: handle_btn_claim(event))

        btn_apply = wx.Button(panel_footer, label="Apply")
        hbox_footer.Add(wx.StaticText(panel_footer, label=""), proportion=5)
        hbox_footer.Add(btn_apply, flag=wx.ALL | wx.ALIGN_CENTER, border=5, proportion=1)
        hbox_footer.Add(wx.StaticText(panel_footer, label=""), proportion=5)
        btn_apply.Bind(wx.EVT_BUTTON, lambda event: handle_btn_apply(event))

        btn_release = wx.Button(panel_footer, label="Release Audio Interface")
        hbox_footer.Add(wx.StaticText(panel_footer, label=""), proportion=5)
        hbox_footer.Add(btn_release, flag=wx.ALL | wx.ALIGN_CENTER, border=5, proportion=1)
        hbox_footer.Add(wx.StaticText(panel_footer, label=""), proportion=5)
        btn_release.Bind(wx.EVT_BUTTON, lambda event: handle_btn_release(event))

        btn_reload_alsa_and_pipewire = wx.Button(panel_footer, label="Reload ALSA and PipeWire")
        hbox_footer.Add(wx.StaticText(panel_footer, label=""), proportion=5)
        hbox_footer.Add(btn_reload_alsa_and_pipewire, flag=wx.ALL | wx.ALIGN_CENTER, border=5, proportion=1)
        hbox_footer.Add(wx.StaticText(panel_footer, label=""), proportion=5)
        btn_reload_alsa_and_pipewire.Bind(wx.EVT_BUTTON, lambda event: handle_btn_reload_alsa_and_pipewire(event))

        return panel_footer

    def __update_availability(self):
        self.__tab_sbx.update_availability(g6_api=self.__g6_api)


def main():
    app = wx.App(False)
    frame = AudioSettingsFrame()
    frame.open()
    app.MainLoop()
