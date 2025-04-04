import wx


class RecordingTab:

    def create(self, notebook) -> wx.Panel:
        panel = wx.Panel(notebook)
        vbox = wx.BoxSizer(wx.VERTICAL)
        panel.SetSizer(vbox)

        tab_notebook = wx.Notebook(panel, size=(300, 200))

        mic_panel = self.__create_microphone_tab(tab_notebook)
        tab_notebook.AddPage(mic_panel, "Microphone")

        other_input_panel = self.__create_other_input_tab(tab_notebook)
        tab_notebook.AddPage(other_input_panel, "Other Input")

        vbox.Add(tab_notebook, 1, wx.EXPAND | wx.ALL, 5)
        return panel

    def __create_microphone_tab(self, tab_notebook):
        panel = wx.Panel(tab_notebook)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # microphone volume
        vbox.Add(wx.StaticText(panel, label="Mic-Recording volume"), 0, wx.ALL, 5)
        sld_mic_volume = wx.Slider(panel, minValue=0, maxValue=100, value=50, style=wx.SL_HORIZONTAL)
        vbox.Add(sld_mic_volume, 0, wx.ALL | wx.EXPAND, 5)

        # microphone boost
        vbox.Add(wx.StaticText(panel, label="Microphone boost"), 0, wx.ALL, 5)
        sld_mic_boost = wx.Slider(panel, minValue=0, maxValue=30, value=10, style=wx.SL_HORIZONTAL)
        vbox.Add(sld_mic_boost, 0, wx.ALL | wx.EXPAND, 5)

        # playback
        playback_checkbox = wx.CheckBox(panel, label="Use this device as Playback source")
        vbox.Add(playback_checkbox, 0, wx.ALL, 5)

        # voice clarity
        chk_noise_reduction = wx.CheckBox(panel, label="Noise reduction")
        sld_noise_reduction = wx.Slider(panel, minValue=0, maxValue=100, value=50, style=wx.SL_HORIZONTAL)
        chk_echo_cancellation = wx.CheckBox(panel, label="Acoustic Echo Cancellation")
        chk_smart_volume = wx.CheckBox(panel, label="Smart Volume")
        check_mic_eq = wx.CheckBox(panel, label="Mic-EQ")

        ## voice clarity > toggle
        tgl_voice_clarity = wx.ToggleButton(panel, label="Voice clarity")
        tgl_voice_clarity.Bind(wx.EVT_TOGGLEBUTTON, lambda evt: self.__toggle_group(evt, [chk_noise_reduction,
                                                                                          sld_noise_reduction,
                                                                                          chk_echo_cancellation,
                                                                                          chk_smart_volume,
                                                                                          check_mic_eq]))
        vbox.Add(tgl_voice_clarity, 0, wx.ALL, 5)

        ## voice clarity > vbox
        vbox_voice_clarity = wx.StaticBoxSizer(wx.VERTICAL, panel, "Voice clarity options")
        for widget in [chk_noise_reduction, sld_noise_reduction, chk_echo_cancellation, chk_smart_volume, check_mic_eq]:
            widget.Enable(False)
            vbox_voice_clarity.Add(widget, 0, wx.ALL | wx.EXPAND, 5)
        vbox.Add(vbox_voice_clarity, 0, wx.ALL | wx.EXPAND, 5)

        # voice morph
        morph_choices = [
            "Neutral", "Male", "Female", "Child", "Grandma", "Dark voice", "Northern Light", "Unstable", "Emo",
            "Elf", "Dwarf", "Intruder", "Ur", "Orc", "Marine", "Hamster", "Roboter"
        ]

        ## voice morph > toggle
        tlg_voice_morph = wx.ToggleButton(panel, label="Voice morph")
        tlg_voice_morph.Bind(wx.EVT_TOGGLEBUTTON, lambda evt: cmb_voice_morph.Enable(tlg_voice_morph.GetValue()))
        vbox.Add(tlg_voice_morph, 0, wx.ALL, 5)

        ## voice morph > combo
        vbox_voice_morph = wx.StaticBoxSizer(wx.VERTICAL, panel, "Voice morph type")
        cmb_voice_morph = wx.ComboBox(panel, choices=morph_choices, style=wx.CB_READONLY)
        cmb_voice_morph.Enable(False)
        vbox_voice_morph.Add(cmb_voice_morph, 0, wx.ALL | wx.EXPAND, 5)
        vbox.Add(vbox_voice_morph, 0, wx.ALL | wx.EXPAND, 5)

        panel.SetSizer(vbox)
        return panel

    @staticmethod
    def __create_other_input_tab(parent):
        panel = wx.Panel(parent)
        vbox = wx.BoxSizer(wx.VERTICAL)

        channels = ["2 channel"]
        bits = ["16 Bit", "32 Bit"]
        rates = ["44 kHz", "48 kHz", "88 kHz", "96 kHz", "176 kHz", "192 kHz"]
        quality = [f"{c} {b} {r}" for c in channels for b in bits for r in rates]

        for name in ["Line In", "SPDIF In", "What U Hear"]:
            box = wx.StaticBoxSizer(wx.VERTICAL, panel, name)
            combo = wx.ComboBox(panel, choices=quality, style=wx.CB_READONLY)
            combo.SetSelection(0)
            box.Add(combo, 0, wx.ALL | wx.EXPAND, 5)
            vbox.Add(box, 0, wx.ALL | wx.EXPAND, 5)

        panel.SetSizer(vbox)
        return panel

    @staticmethod
    def __toggle_group(event, widgets):
        state = event.GetEventObject().GetValue()
        for widget in widgets:
            widget.Enable(state)
