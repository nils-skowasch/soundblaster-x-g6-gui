import wx


class AudioSettingsFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Audio Settings", size=(400, 350))

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        self.controls = {}

        settings = ["Surround", "Crystalizer", "Bass", "Smart Volume", "Dialog Plus"]

        for setting in settings:
            hbox = wx.BoxSizer(wx.HORIZONTAL)
            label = wx.StaticText(panel, label=setting)
            slider = wx.Slider(panel, minValue=0, maxValue=100, value=50, style=wx.SL_HORIZONTAL)
            toggle = wx.ToggleButton(panel, label="Enable")

            slider.Enable(False)  # Initially disabled

            toggle.Bind(wx.EVT_TOGGLEBUTTON, lambda evt, s=slider: self.on_toggle(evt, s))

            hbox.Add(label, proportion=1, flag=wx.ALL | wx.EXPAND, border=5)
            hbox.Add(slider, proportion=2, flag=wx.ALL | wx.EXPAND, border=5)
            hbox.Add(toggle, proportion=1, flag=wx.ALL, border=5)

            self.controls[setting] = (slider, toggle)
            vbox.Add(hbox, flag=wx.EXPAND)

        panel.SetSizer(vbox)
        self.Centre()
        self.Show()

    def on_toggle(self, event, slider):
        button = event.GetEventObject()
        enabled = button.GetValue()
        slider.Enable(enabled)
        button.SetLabel("Disable" if enabled else "Enable")


if __name__ == "__main__":
    app = wx.App(False)
    frame = AudioSettingsFrame()
    app.MainLoop()
