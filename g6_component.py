import wx


# noinspection DuplicatedCode
def build_slider_hbox(panel: wx.Panel, label: str) -> wx.BoxSizer:
    hbox = wx.BoxSizer(wx.HORIZONTAL)

    label = wx.StaticText(panel, label=label)
    slider = wx.Slider(panel, minValue=0, maxValue=100, value=50, style=wx.SL_HORIZONTAL)
    toggle = wx.ToggleButton(panel, label="Enable")

    slider.Enable(False)
    toggle.Bind(wx.EVT_TOGGLEBUTTON, lambda evt, s=slider: __on_toggle(evt, s))

    hbox.Add(label, proportion=1, flag=wx.ALL | wx.EXPAND, border=5)
    hbox.Add(slider, proportion=2, flag=wx.ALL | wx.EXPAND, border=5)
    hbox.Add(toggle, proportion=1, flag=wx.ALL, border=5)

    return hbox


def __on_toggle(event, slider):
    button = event.GetEventObject()
    enabled = button.GetValue()
    slider.Enable(enabled)
    button.SetLabel("Disable" if enabled else "Enable")
