import wx

from g6_component import build_slider_hbox


class SbxTab:

    @staticmethod
    def create(notebook: wx.Notebook) -> wx.Panel:
        panel = wx.Panel(notebook)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # controls = {}
        settings = ["Surround", "Crystalizer", "Bass", "Smart Volume", "Dialog Plus"]

        for setting in settings:
            hbox = build_slider_hbox(panel, setting)
            vbox.Add(hbox, flag=wx.EXPAND)

        panel.SetSizer(vbox)
        return panel
