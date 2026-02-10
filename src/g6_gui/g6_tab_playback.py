import wx


class PlaybackTab:

    def create(self, notebook: wx.Notebook) -> wx.Panel:
        panel = wx.Panel(notebook)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # constants
        audio_choices = ["Stereo", "Virtual Surround 5.1", "Virtual Surround 7.1"]

        # Speakers section
        hbox_speakers = self.__build_radio_combo_hbox(panel, 'Speakers', audio_choices, True)

        # Headphones section
        hbox_headphones = self.__build_radio_combo_hbox(panel, 'Headphones', audio_choices, False)

        # Directmode toggle buttons
        tgl_directmode = wx.ToggleButton(panel, label="Directmode")
        tgl_spdif = wx.ToggleButton(panel, label="SPDIF-Out Directmode")

        # Filter ComboBox
        filter_choices = [
            "Fast Roll-Off - Minimum Phase",
            "Slow Roll-Off - Minimum Phase",
            "Fast Roll-Off - Linear Phase",
            "Slow Roll-Off - Linear Phase"
        ]
        cmb_filter = wx.ComboBox(panel, choices=filter_choices, style=wx.CB_READONLY)
        cmb_filter.SetSelection(0)

        # Test button
        btn_test = wx.Button(panel, label="Test")

        # Add components to vbox
        vbox.Add(hbox_speakers, flag=wx.EXPAND)
        vbox.Add(hbox_headphones, flag=wx.EXPAND)
        vbox.Add(tgl_directmode, flag=wx.ALL | wx.EXPAND, border=5)
        vbox.Add(tgl_spdif, flag=wx.ALL | wx.EXPAND, border=5)
        vbox.Add(cmb_filter, flag=wx.ALL | wx.EXPAND, border=5)
        vbox.Add(btn_test, flag=wx.ALL | wx.EXPAND, border=5)

        panel.SetSizer(vbox)
        return panel

    @staticmethod
    def __build_radio_combo_hbox(panel: wx.Panel, label: str, choices: list, radio_selected: bool) -> wx.BoxSizer:
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        radio_style = wx.RB_GROUP if radio_selected else 0
        rad = wx.RadioButton(panel, label=label, style=radio_style)
        cmb = wx.ComboBox(panel, choices=choices, style=wx.CB_READONLY)
        cmb.SetSelection(0)
        hbox.Add(rad, proportion=1, flag=wx.ALL | wx.EXPAND, border=5)
        hbox.Add(cmb, proportion=2, flag=wx.ALL | wx.EXPAND, border=5)
        return hbox
