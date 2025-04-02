import wx

class AudioSettingsFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Audio Settings", size=(600, 600))

        notebook = wx.Notebook(self)

        self.create_sbx_profile_tab(notebook)
        self.create_playback_tab(notebook)
        self.create_recording_tab(notebook)
        self.create_decoder_tab(notebook)
        self.create_mixer_tab(notebook)  # New Mixer tab

        self.Centre()
        self.Show()

    def create_sbx_profile_tab(self, notebook):
        panel = wx.Panel(notebook)
        vbox = wx.BoxSizer(wx.VERTICAL)

        self.controls = {}
        settings = ["Surround", "Crystalizer", "Bass", "Smart Volume", "Dialog Plus"]

        for setting in settings:
            hbox = wx.BoxSizer(wx.HORIZONTAL)
            label = wx.StaticText(panel, label=setting)
            slider = wx.Slider(panel, minValue=0, maxValue=100, value=50, style=wx.SL_HORIZONTAL)
            toggle = wx.ToggleButton(panel, label="Enable")

            slider.Enable(False)
            toggle.Bind(wx.EVT_TOGGLEBUTTON, lambda evt, s=slider: self.on_toggle(evt, s))

            hbox.Add(label, proportion=1, flag=wx.ALL | wx.EXPAND, border=5)
            hbox.Add(slider, proportion=2, flag=wx.ALL | wx.EXPAND, border=5)
            hbox.Add(toggle, proportion=1, flag=wx.ALL, border=5)

            self.controls[setting] = (slider, toggle)
            vbox.Add(hbox, flag=wx.EXPAND)

        panel.SetSizer(vbox)
        notebook.AddPage(panel, "SBX-Profile")

    def create_playback_tab(self, notebook):
        panel = wx.Panel(notebook)
        vbox = wx.BoxSizer(wx.VERTICAL)

        choices = ["Stereo", "Virtual Surround 5.1", "Virtual Surround 7.1"]

        # Speakers section
        speakers_box = wx.BoxSizer(wx.HORIZONTAL)
        speakers_radio = wx.RadioButton(panel, label="Speakers", style=wx.RB_GROUP)
        speakers_combo = wx.ComboBox(panel, choices=choices, style=wx.CB_READONLY)
        speakers_combo.SetSelection(0)
        speakers_box.Add(speakers_radio, proportion=1, flag=wx.ALL | wx.EXPAND, border=5)
        speakers_box.Add(speakers_combo, proportion=2, flag=wx.ALL | wx.EXPAND, border=5)

        # Headphones section
        headphones_box = wx.BoxSizer(wx.HORIZONTAL)
        headphones_radio = wx.RadioButton(panel, label="Headphones")
        headphones_combo = wx.ComboBox(panel, choices=choices, style=wx.CB_READONLY)
        headphones_combo.SetSelection(0)
        headphones_box.Add(headphones_radio, proportion=1, flag=wx.ALL | wx.EXPAND, border=5)
        headphones_box.Add(headphones_combo, proportion=2, flag=wx.ALL | wx.EXPAND, border=5)

        # Directmode toggle buttons
        directmode_toggle = wx.ToggleButton(panel, label="Directmode")
        spdif_toggle = wx.ToggleButton(panel, label="SPDIF-Out Directmode")

        # Filter ComboBox
        filter_choices = [
            "Schneller Abrollvorgang - Minimale Phase",
            "Langsames Abrollen - Minimale Phase",
            "Schneller Abrollvorgang - Lineare Phase",
            "Langsames Abrollen - Lineare Phase"
        ]
        filter_combo = wx.ComboBox(panel, choices=filter_choices, style=wx.CB_READONLY)
        filter_combo.SetSelection(0)

        # Audio Quality ComboBox
        bit_depths = ["16 Bit", "24 Bit", "32 Bit"]
        sample_rates = ["44 kHz", "48 kHz", "88 kHz", "96 kHz"]
        audio_quality_choices = [f"{bit} {rate}" for bit in bit_depths for rate in sample_rates]
        audio_quality_combo = wx.ComboBox(panel, choices=audio_quality_choices, style=wx.CB_READONLY)
        audio_quality_combo.SetSelection(0)

        # Test button
        test_button = wx.Button(panel, label="Test")

        vbox.Add(speakers_box, flag=wx.EXPAND)
        vbox.Add(headphones_box, flag=wx.EXPAND)
        vbox.Add(directmode_toggle, flag=wx.ALL | wx.EXPAND, border=5)
        vbox.Add(spdif_toggle, flag=wx.ALL | wx.EXPAND, border=5)
        vbox.Add(filter_combo, flag=wx.ALL | wx.EXPAND, border=5)
        vbox.Add(audio_quality_combo, flag=wx.ALL | wx.EXPAND, border=5)
        vbox.Add(test_button, flag=wx.ALL | wx.EXPAND, border=5)

        panel.SetSizer(vbox)
        notebook.AddPage(panel, "Playback")

    def create_recording_tab(self, notebook):
        panel = wx.Panel(notebook)
        tabbook = wx.Notebook(panel)

        mic_panel = self.create_microphone_tab(tabbook)
        other_input_panel = self.create_other_input_tab(tabbook)

        tabbook.AddPage(mic_panel, "Microphone")
        tabbook.AddPage(other_input_panel, "Other Input")

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(tabbook, 1, wx.EXPAND | wx.ALL, 5)
        panel.SetSizer(sizer)
        notebook.AddPage(panel, "Recording")

    def create_decoder_tab(self, notebook):
        panel = wx.Panel(notebook)
        vbox = wx.BoxSizer(wx.VERTICAL)

        normal_radio = wx.RadioButton(panel, label="Normal", style=wx.RB_GROUP)
        full_radio = wx.RadioButton(panel, label="Full")
        night_radio = wx.RadioButton(panel, label="Night")

        vbox.Add(normal_radio, 0, wx.ALL, 5)
        vbox.Add(full_radio, 0, wx.ALL, 5)
        vbox.Add(night_radio, 0, wx.ALL, 5)

        panel.SetSizer(vbox)
        notebook.AddPage(panel, "Decoder")

    def create_mixer_tab(self, notebook):
        panel = wx.Panel(notebook)
        vbox = wx.BoxSizer(wx.VERTICAL)

        panel.SetSizer(vbox)

        # Define groups and george components
        self.create_mixer_slider_group(panel, "Playback", ["Speakers"])
        self.create_mixer_slider_group(panel, "Monitoring", ["Line-In", "External Microphone", "SPDIF-In"])
        self.create_mixer_slider_group(panel, "Recording", ["External Mic", "Line In", "SPDIF-In", "Why U Hear"])

        notebook.AddPage(panel, "Mixer")

    def create_mixer_slider_group(self, panel, group_name, george_labels):
        group_box = wx.StaticBox(panel, label=group_name)
        group_sizer = wx.StaticBoxSizer(group_box, wx.VERTICAL)

        for label in george_labels:
            mixer_slider_component = self.create_mixer_slider_component(panel, label)
            group_sizer.Add(mixer_slider_component, flag=wx.ALL | wx.EXPAND, border=5)

        panel.GetSizer().Add(group_sizer, flag=wx.EXPAND)

    def create_mixer_slider_component(self, panel, label):
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        component_label = wx.StaticText(panel, label=label)
        checkbox = wx.CheckBox(panel, label="Active / Muted")
        slider = wx.Slider(panel, minValue=0, maxValue=100, value=50, style=wx.SL_HORIZONTAL)
        gears_button = wx.Button(panel, label="⚙")

        gears_button.Bind(wx.EVT_BUTTON, self.on_gears_button)

        hbox.Add(component_label, proportion=1, flag=wx.ALL | wx.EXPAND, border=5)
        hbox.Add(checkbox, proportion=1, flag=wx.ALL | wx.EXPAND, border=5)
        hbox.Add(slider, proportion=2, flag=wx.ALL | wx.EXPAND, border=5)
        hbox.Add(gears_button, proportion=1, flag=wx.ALL, border=5)

        return hbox

    def on_gears_button(self, event):
        dialog = wx.Dialog(self, title="Gears Settings", size=(300, 200))
        vbox = wx.BoxSizer(wx.VERTICAL)

        l_slider = wx.Slider(dialog, minValue=0, maxValue=100, value=50, style=wx.SL_HORIZONTAL)
        r_slider = wx.Slider(dialog, minValue=0, maxValue=100, value=50, style=wx.SL_HORIZONTAL)

        vbox.Add(wx.StaticText(dialog, label="Left"), flag=wx.ALL, border=5)
        vbox.Add(l_slider, flag=wx.ALL | wx.EXPAND, border=5)
        vbox.Add(wx.StaticText(dialog, label="Right"), flag=wx.ALL, border=5)
        vbox.Add(r_slider, flag=wx.ALL | wx.EXPAND, border=5)

        dialog.SetSizer(vbox)
        dialog.ShowModal()

    def create_microphone_tab(self, parent):
        panel = wx.Panel(parent)
        vbox = wx.BoxSizer(wx.VERTICAL)

        mic_volume = wx.Slider(panel, minValue=0, maxValue=100, value=50, style=wx.SL_HORIZONTAL)
        mic_boost = wx.Slider(panel, minValue=0, maxValue=30, value=10, style=wx.SL_HORIZONTAL)
        playback_checkbox = wx.CheckBox(panel, label="Use this device as Playback source")

        voice_clarity_toggle = wx.ToggleButton(panel, label="Voice clarity")
        voice_clarity_box = wx.StaticBoxSizer(wx.VERTICAL, panel, "Voice clarity options")
        noise_reduction_cb = wx.CheckBox(panel, label="Noise reduction")
        noise_slider = wx.Slider(panel, minValue=0, maxValue=100, value=50, style=wx.SL_HORIZONTAL)
        echo_cb = wx.CheckBox(panel, label="Acoustic Echo Cancelation")
        smart_volume_cb = wx.CheckBox(panel, label="Smart Volume")
        mic_eq_cb = wx.CheckBox(panel, label="Mic-EQ")

        for widget in [noise_reduction_cb, noise_slider, echo_cb, smart_volume_cb, mic_eq_cb]:
            widget.Enable(False)
            voice_clarity_box.Add(widget, 0, wx.ALL | wx.EXPAND, 5)

        voice_clarity_toggle.Bind(wx.EVT_TOGGLEBUTTON, lambda evt: self.toggle_group(evt, [noise_reduction_cb, noise_slider, echo_cb, smart_volume_cb, mic_eq_cb]))

        voice_morph_toggle = wx.ToggleButton(panel, label="Voice morph")
        morph_box = wx.StaticBoxSizer(wx.VERTICAL, panel, "Voice morph type")
        morph_choices = [
            "Neutral", "Male", "Female", "Child", "Grandma", "Dark voice", "Northern Light", "Unstable", "Emo",
            "Elf", "Dwarf", "Intruder", "Ur", "Orc", "Marine", "Hamster", "Roboter"
        ]
        morph_combo = wx.ComboBox(panel, choices=morph_choices, style=wx.CB_READONLY)
        morph_combo.Enable(False)
        morph_box.Add(morph_combo, 0, wx.ALL | wx.EXPAND, 5)

        voice_morph_toggle.Bind(wx.EVT_TOGGLEBUTTON, lambda evt: morph_combo.Enable(voice_morph_toggle.GetValue()))

        vbox.Add(wx.StaticText(panel, label="Mic-Recording volume"), 0, wx.ALL, 5)
        vbox.Add(mic_volume, 0, wx.ALL | wx.EXPAND, 5)
        vbox.Add(wx.StaticText(panel, label="Microphone boost"), 0, wx.ALL, 5)
        vbox.Add(mic_boost, 0, wx.ALL | wx.EXPAND, 5)
        vbox.Add(playback_checkbox, 0, wx.ALL, 5)
        vbox.Add(voice_clarity_toggle, 0, wx.ALL, 5)
        vbox.Add(voice_clarity_box, 0, wx.ALL | wx.EXPAND, 5)
        vbox.Add(voice_morph_toggle, 0, wx.ALL, 5)
        vbox.Add(morph_box, 0, wx.ALL | wx.EXPAND, 5)

        panel.SetSizer(vbox)
        return panel

    def create_other_input_tab(self, parent):
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

    def toggle_group(self, event, widgets):
        state = event.GetEventObject().GetValue()
        for widget in widgets:
            widget.Enable(state)

    def on_toggle(self, event, slider):
        button = event.GetEventObject()
        enabled = button.GetValue()
        slider.Enable(enabled)
        button.SetLabel("Disable" if enabled else "Enable")

if __name__ == "__main__":
    app = wx.App(False)
    frame = AudioSettingsFrame()
    app.MainLoop()
