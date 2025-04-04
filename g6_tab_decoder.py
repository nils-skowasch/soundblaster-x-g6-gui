import wx


class DecoderTab:
    @staticmethod
    def create(notebook: wx.Notebook) -> wx.Panel:
        panel = wx.Panel(notebook)
        vbox = wx.BoxSizer(wx.VERTICAL)

        rad_normal = wx.RadioButton(panel, label="Normal", style=wx.RB_GROUP)
        rad_full = wx.RadioButton(panel, label="Full")
        rad_night = wx.RadioButton(panel, label="Night")

        vbox.Add(rad_normal, 0, wx.ALL, 5)
        vbox.Add(rad_full, 0, wx.ALL, 5)
        vbox.Add(rad_night, 0, wx.ALL, 5)

        panel.SetSizer(vbox)
        return panel
