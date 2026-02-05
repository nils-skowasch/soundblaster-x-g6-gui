import wx


class RecordingTab:

    def __init__(self):
        self.__sld_mic_volume = None
        self.__sld_mic_boost = None
        self.__chk_playback = None
        self.__sld_mic_monitoring = None
        self.__tgl_voice_clarity = None
        self.__chk_noise_reduction = None
        self.__sld_noise_reduction = None
        self.__chk_echo_cancellation = None
        self.__chk_smart_volume = None
        self.__chk_mic_eq = None
        self.__cmb_mic_eq_preset = None

    def create(self, notebook: wx.Notebook) -> wx.Panel:
        panel = wx.Panel(notebook)
        vbox = wx.BoxSizer(wx.VERTICAL)
        panel.SetSizer(vbox)

        # microphone volume
        vbox.Add(wx.StaticText(panel, label="Mic-Recording volume"), 0, wx.ALL, 5)
        self.__sld_mic_volume = wx.Slider(panel, minValue=0, maxValue=100, value=50, style=wx.SL_HORIZONTAL)
        vbox.Add(self.__sld_mic_volume, 0, wx.ALL | wx.EXPAND, 5)

        # microphone boost
        vbox.Add(wx.StaticText(panel, label="Microphone boost"), 0, wx.ALL, 5)
        self.__sld_mic_boost = wx.Slider(panel, minValue=0, maxValue=30, value=10, style=wx.SL_HORIZONTAL)
        vbox.Add(self.__sld_mic_boost, 0, wx.ALL | wx.EXPAND, 5)

        # playback
        self.__chk_playback = wx.CheckBox(panel, label="Use this device as Playback source (Monitoring)")
        self.__chk_playback.Bind(wx.EVT_CHECKBOX, lambda evt: self.__handle_mic_monitoring_enabled())
        vbox.Add(self.__chk_playback, 0, wx.ALL, 5)
        vbox.Add(wx.StaticText(panel, label="Mic-Monitoring volume"), 0, wx.ALL, 5)
        self.__sld_mic_monitoring = wx.Slider(panel, minValue=0, maxValue=100, value=50, style=wx.SL_HORIZONTAL)
        vbox.Add(self.__sld_mic_monitoring, 0, wx.ALL | wx.EXPAND, 5)

        # playback: handle enable state
        self.__handle_mic_monitoring_enabled()

        # voice clarity
        self.__tgl_voice_clarity = wx.ToggleButton(panel, label="Voice clarity")
        self.__tgl_voice_clarity.Bind(wx.EVT_TOGGLEBUTTON, lambda evt: self.__handle_voice_clarity_enabled())
        vbox.Add(self.__tgl_voice_clarity, 0, wx.ALL, 5)

        self.__chk_noise_reduction = wx.CheckBox(panel, label="Noise reduction")
        self.__chk_noise_reduction.Bind(wx.EVT_CHECKBOX,
                                        lambda evt: self.__handle_voice_clarity_sld_noise_reduction_enabled())
        self.__sld_noise_reduction = wx.Slider(panel, minValue=0, maxValue=100, value=50, style=wx.SL_HORIZONTAL)
        self.__chk_echo_cancellation = wx.CheckBox(panel, label="Acoustic Echo Cancellation")
        self.__chk_smart_volume = wx.CheckBox(panel, label="Smart Volume")
        self.__chk_mic_eq = wx.CheckBox(panel, label="Mic-EQ")
        self.__chk_mic_eq.Bind(wx.EVT_CHECKBOX,
                                      lambda evt: self.__handle_voice_clarity_cmb_mic_eq_preset_enabled())
        preset_choices = [
            "Preset 1 - Reduce bass, harshness, improve clarity",
            "Preset 2 - Reduce bass, improve vocal clarity",
            "Preset 3 - Reduce harshness, improve vocal",
            "Preset 4 - Reduce bass, improve vocal",
            "Preset 5 - Improve vocal, reduce harshness",
            "Preset 6 - Reduce bass, improve clarity",
            "Preset 7 - Reduce vocal, improve bass/clarity",
            "Preset 8 - Reduce harshness, improve vocal/clarity",
            "Preset 9 - Reduce harshness, imrpove clarity",
            "Preset 10 - Improve clarity",
            "Preset DM-1 - Improve vocal clarity"
        ]
        self.__cmb_mic_eq_preset = wx.ComboBox(panel, choices=preset_choices, style=wx.CB_READONLY)
        self.__cmb_mic_eq_preset.SetSelection(0)

        # voice clarity > group
        vbox_voice_clarity = wx.StaticBoxSizer(wx.VERTICAL, panel, "Voice clarity options")
        for widget in [self.__chk_noise_reduction, self.__sld_noise_reduction, self.__chk_echo_cancellation,
                       self.__chk_smart_volume, self.__chk_mic_eq, self.__cmb_mic_eq_preset]:
            vbox_voice_clarity.Add(widget, 0, wx.ALL | wx.EXPAND, 5)
        vbox.Add(vbox_voice_clarity, 0, wx.ALL | wx.EXPAND, 5)

        # voice clarity: handle enable state
        self.__handle_voice_clarity_enabled()

        panel.SetSizer(vbox)
        return panel

    @staticmethod
    def __toggle_group(event, widgets):
        state = event.GetEventObject().GetValue()
        for widget in widgets:
            widget.Enable(state)

    def __handle_mic_monitoring_enabled(self):
        self.__sld_mic_monitoring.Enable(self.__chk_playback.GetValue())

    def __handle_voice_clarity_enabled(self):
        voice_clarity_enabled = self.__tgl_voice_clarity.GetValue()
        self.__chk_noise_reduction.Enable(voice_clarity_enabled)
        self.__handle_voice_clarity_sld_noise_reduction_enabled()
        self.__chk_echo_cancellation.Enable(voice_clarity_enabled)
        self.__chk_smart_volume.Enable(voice_clarity_enabled)
        self.__chk_mic_eq.Enable(voice_clarity_enabled)
        self.__cmb_mic_eq_preset.Enable(voice_clarity_enabled and self.__chk_mic_eq.GetValue())
        self.__handle_voice_clarity_cmb_mic_eq_preset_enabled()

    def __handle_voice_clarity_sld_noise_reduction_enabled(self):
        self.__sld_noise_reduction.Enable(self.__tgl_voice_clarity.GetValue() and self.__chk_noise_reduction.GetValue())

    def __handle_voice_clarity_cmb_mic_eq_preset_enabled(self):
        self.__cmb_mic_eq_preset.Enable(self.__tgl_voice_clarity.GetValue() and self.__chk_mic_eq.GetValue())
