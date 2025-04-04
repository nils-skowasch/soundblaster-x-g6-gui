import wx


class SbxTab:

    def create(self, notebook: wx.Notebook) -> wx.Panel:
        panel = wx.Panel(notebook)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # controls = {}
        settings = ["Surround", "Crystalizer", "Bass", "Smart Volume", "Dialog Plus"]

        for setting in settings:
            hbox = self.__build_slider_hbox(panel, setting)
            vbox.Add(hbox, flag=wx.EXPAND)

        panel.SetSizer(vbox)
        return panel

    # noinspection DuplicatedCode
    def __build_slider_hbox(self, panel: wx.Panel, label: str) -> wx.BoxSizer:
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        label = wx.StaticText(panel, label=label)
        slider = wx.Slider(panel, minValue=0, maxValue=100, value=50, style=wx.SL_HORIZONTAL)
        toggle = wx.ToggleButton(panel, label="Enable")

        slider.Enable(False)
        toggle.Bind(wx.EVT_TOGGLEBUTTON, lambda evt, s=slider: self.__on_toggle(evt, s))

        hbox.Add(label, proportion=1, flag=wx.ALL | wx.EXPAND, border=5)
        hbox.Add(slider, proportion=2, flag=wx.ALL | wx.EXPAND, border=5)
        hbox.Add(toggle, proportion=1, flag=wx.ALL, border=5)

        return hbox

    @staticmethod
    def __on_toggle(event, slider):
        button = event.GetEventObject()
        enabled = button.GetValue()
        slider.Enable(enabled)
        button.SetLabel("Disable" if enabled else "Enable")
