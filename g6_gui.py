import wx
from g6_tab_sbx import SbxTab
from g6_tab_playback import PlaybackTab
from g6_tab_recording import RecordingTab
from g6_tab_decoder import DecoderTab
from g6_tab_mixer import MixerTab
from g6_tab_lighting import LightingTab


class AudioSettingsFrame(wx.Frame):

    def __init__(self):
        super().__init__(None, title="Audio Settings", size=wx.Size(840, 630))

        # create panel with vertical box sizer
        self.panel_main = wx.Panel(self)

        # set vbox sizer as layout manager to panel_main
        self.vbox_main = wx.BoxSizer(wx.VERTICAL)
        self.panel_main.SetSizer(self.vbox_main)

        # create notebook
        self.notebook = self.__create_notebook(self.panel_main)
        self.vbox_main.Add(self.notebook, flag=wx.EXPAND, proportion=1, border=5)

        # create footer
        self.panel_footer = self.__create_footer(self.panel_main)
        self.vbox_main.Add(self.panel_footer, flag=wx.EXPAND, proportion=0, border=5)

    def open(self):
        self.Centre()
        self.Show()

    def __create_notebook(self, parent: wx.Panel) -> wx.Notebook:
        # create notebook (tab folder)
        notebook = wx.Notebook(parent)

        # create tabs
        notebook.AddPage(SbxTab().create(notebook), 'SBX-Profile')
        notebook.AddPage(PlaybackTab().create(notebook), "Playback")

        notebook.AddPage(RecordingTab().create(notebook), "Recording")
        notebook.AddPage(DecoderTab().create(notebook), "Decoder")
        notebook.AddPage(MixerTab(self).create(notebook), "Mixer")

        notebook.AddPage(LightingTab().create(notebook), "Lighting")

        return notebook

    @staticmethod
    def __create_footer(parent: wx.Panel) -> wx.Panel:
        # create footer panel
        panel_footer = wx.Panel(parent)

        # define sizer as layout manager
        hbox_footer = wx.BoxSizer(wx.HORIZONTAL)
        panel_footer.SetSizer(hbox_footer)

        # add components to footer
        btn_apply = wx.Button(panel_footer, label="Apply")
        hbox_footer.Add(wx.StaticText(panel_footer, label=""), proportion=5)
        hbox_footer.Add(btn_apply, flag=wx.ALL | wx.ALIGN_CENTER, border=5, proportion=1)
        hbox_footer.Add(wx.StaticText(panel_footer, label=""), proportion=5)

        return panel_footer


if __name__ == "__main__":
    app = wx.App(False)
    frame = AudioSettingsFrame()
    frame.open()
    app.MainLoop()
