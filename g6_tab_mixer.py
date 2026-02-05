import wx

FRIEND_SLIDER = 'slider'
FRIEND_GEARS = 'gears'


class MixerTab:

    def __init__(self, frame: wx.Frame):
        self.frame = frame

    def create(self, notebook: wx.Notebook) -> wx.Panel:
        panel = wx.Panel(notebook)

        vbox = wx.BoxSizer(wx.VERTICAL)
        panel.SetSizer(vbox)

        # Define groups and george components
        self.__create_mixer_slider_group(panel, "Playback", ["Speakers"])
        self.__create_mixer_slider_group(panel, "Monitoring", ["Line-In", "External Microphone", "SPDIF-In"])
        self.__create_mixer_slider_group(panel, "Recording", ["External Mic", "Line In", "SPDIF-In", "What U Hear"])

        return panel

    def __create_mixer_slider_group(self, panel, group_name, george_labels):
        grp = wx.StaticBox(panel, label=group_name)
        grp_sizer = wx.StaticBoxSizer(grp, wx.VERTICAL)

        for label in george_labels:
            cmp_mixer_slider = self.__create_mixer_slider_component(panel, label)
            grp_sizer.Add(cmp_mixer_slider, flag=wx.ALL | wx.EXPAND, border=5)

        panel.GetSizer().Add(grp_sizer, flag=wx.EXPAND)

    # noinspection DuplicatedCode
    def __create_mixer_slider_component(self, panel, label):
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        lbl_component = wx.StaticText(panel, label=label)
        chk_component = wx.CheckBox(panel, label="Active")
        chk_component.SetValue(True)
        chk_component.Bind(wx.EVT_CHECKBOX, self.__on_checkbox_button)
        sld_component = wx.Slider(panel, minValue=0, maxValue=100, value=50, style=wx.SL_HORIZONTAL)
        btn_gears = wx.Button(panel, label="⚙")
        btn_gears.Bind(wx.EVT_BUTTON, self.__on_gears_button)

        chk_component.friends = {FRIEND_SLIDER: sld_component, FRIEND_GEARS: btn_gears}

        hbox.Add(lbl_component, proportion=1, flag=wx.ALL | wx.EXPAND, border=5)
        hbox.Add(chk_component, proportion=1, flag=wx.ALL | wx.EXPAND, border=5)
        hbox.Add(sld_component, proportion=2, flag=wx.ALL | wx.EXPAND, border=5)
        hbox.Add(btn_gears, proportion=1, flag=wx.ALL, border=5)

        return hbox

    def __on_gears_button(self, event):
        dialog = wx.Dialog(self.frame, title="Gears Settings", size=wx.Size(300, 200))
        vbox = wx.BoxSizer(wx.VERTICAL)

        l_slider = wx.Slider(dialog, minValue=0, maxValue=100, value=50, style=wx.SL_HORIZONTAL)
        r_slider = wx.Slider(dialog, minValue=0, maxValue=100, value=50, style=wx.SL_HORIZONTAL)

        vbox.Add(wx.StaticText(dialog, label="Left"), flag=wx.ALL, border=5)
        vbox.Add(l_slider, flag=wx.ALL | wx.EXPAND, border=5)
        vbox.Add(wx.StaticText(dialog, label="Right"), flag=wx.ALL, border=5)
        vbox.Add(r_slider, flag=wx.ALL | wx.EXPAND, border=5)

        dialog.SetSizer(vbox)
        dialog.ShowModal()

    @staticmethod
    def __on_checkbox_button(event):
        checkbox = event.EventObject
        checkbox.Label = 'Active' if checkbox.Value else 'Muted'
        checkbox.friends[FRIEND_SLIDER].Enable(checkbox.Value)
        checkbox.friends[FRIEND_GEARS].Enable(checkbox.Value)
