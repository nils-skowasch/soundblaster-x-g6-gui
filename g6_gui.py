import wx
from g6_tab_sbx import SbxTab
from g6_tab_playback import PlaybackTab
from g6_tab_recording import RecordingTab
from g6_tab_decoder import DecoderTab
from g6_tab_mixer import MixerTab


class AudioSettingsFrame(wx.Frame):

    def __init__(self):
        super().__init__(None, title="Audio Settings", size=(1024, 768))

        self.notebook = wx.Notebook(self, size=(800, 600))

        self.notebook.AddPage(SbxTab().create(self.notebook), 'SBX-Profile')
        self.notebook.AddPage(PlaybackTab().create(self.notebook), "Playback")

        self.notebook.AddPage(RecordingTab().create(self.notebook), "Recording")
        self.notebook.AddPage(DecoderTab().create(self.notebook), "Decoder")
        self.notebook.AddPage(MixerTab(self).create(self.notebook), "Mixer")

    def open(self):
        self.Centre()
        self.Show()


if __name__ == "__main__":
    app = wx.App(False)
    frame = AudioSettingsFrame()
    frame.open()
    app.MainLoop()
