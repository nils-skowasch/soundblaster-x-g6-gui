from collections.abc import Callable
import wx

from g6_cli import G6Api, AudioFeature, SmartVolumeSpecialHex


class SbxTab:
    class SliderComposite(wx.BoxSizer):
        def __init__(self, parent: wx.Panel, label: str):
            super().__init__(wx.HORIZONTAL)

            # create components
            self.__label = wx.StaticText(parent, label=label)
            self.__vbox_slider = wx.BoxSizer(wx.VERTICAL)
            self.__slider = wx.Slider(parent, minValue=0, maxValue=100, value=50, style=wx.SL_HORIZONTAL)
            self.__special_button_list = self.add_special_buttons(parent)
            self.__toggle = wx.ToggleButton(parent, label="Disabled")

            # label
            self.Add(self.__label, proportion=1, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=5)

            # slider and special buttons
            ## slider
            slider_proportion = 1
            if len(self.__special_button_list) > 0:
                self.__vbox_slider.AddStretchSpacer(3)
                slider_proportion = 2
            self.__vbox_slider.Add(self.__slider, proportion=slider_proportion, flag=wx.EXPAND, border=0)
            ## special buttons
            self.__hbox_special_buttons = wx.BoxSizer(wx.HORIZONTAL)
            self.__hbox_special_buttons.AddStretchSpacer(1)
            for special_button in self.__special_button_list:
                self.__hbox_special_buttons.Add(special_button, proportion=0, flag=wx.LEFT | wx.RIGHT, border=5)
            self.__hbox_special_buttons.AddStretchSpacer(1)
            self.__vbox_slider.Add(self.__hbox_special_buttons, proportion=0, flag=wx.EXPAND, border=0)
            ## add vbox containing slider and special buttons to self
            self.Add(self.__vbox_slider, proportion=2, flag=wx.ALL | wx.EXPAND, border=5)

            # add toggle button to hbox
            self.Add(self.__toggle, proportion=1, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=5)

            # define component states
            self.__slider.Enable(False)
            for special_button in self.__special_button_list:
                special_button.Enable(False)

        # noinspection PyMethodMayBeStatic
        def add_special_buttons(self, parent: wx.Panel) -> list[wx.Button]:
            """
            To be implemented by inheriting classes.
            :param parent: The parent panel to add the special buttons to.
            """
            return []

        def bind_toggle_event(self, handler: Callable[[wx.CommandEvent], None]) -> None:
            self.__toggle.Bind(wx.EVT_TOGGLEBUTTON, handler)

        def bind_slider_event(self, handler: Callable[[wx.CommandEvent], None]) -> None:
            self.__slider.Bind(wx.EVT_SCROLL, handler)

        def update_availability(self, g6_api: G6Api | None):
            toggle_enabled = self.is_toggle_enabled()

            slider_available = False
            toggle_available = False
            if g6_api is not None:
                slider_available = toggle_enabled and g6_api.sbx_slider_available()
                toggle_available = g6_api.sbx_toggle_available()

            self.__slider.Enable(slider_available)
            self.__toggle.Enable(toggle_available)

        def is_toggle_enabled(self) -> bool:
            return self.__toggle.GetValue()

        def set_toggle_value(self, value: bool):
            self.__toggle.SetValue(value)

        def set_slider_enabled(self, enabled: bool):
            self.__slider.Enable(enabled)

        def set_special_buttons_enabled(self, enabled: bool):
            for special_button in self.__special_button_list:
                special_button.Enable(enabled)

        def get_slider_value(self) -> int:
            return self.__slider.Value

    class SmartVolumeSpecialComposite(SliderComposite):
        def __init__(self, parent: wx.Panel, label: str):
            self.__night_button = None
            self.__loud_button = None
            super().__init__(parent, label)

        def add_special_buttons(self, parent: wx.Panel) -> list[wx.Button]:
            """
            Add special buttons for the Smart Volume preset.
            :param parent: The parent panel to add the special buttons to.
            """
            self.__night_button = wx.Button(parent, label="Night", size=wx.Size(60, 30))
            self.__loud_button = wx.Button(parent, label="Loud", size=wx.Size(60, 30))
            return [self.__night_button, self.__loud_button]

        def update_availability(self, g6_api: G6Api | None):
            super().update_availability(g6_api=g6_api)
            toggle_enabled = self.is_toggle_enabled()

            special_button_available = False
            if g6_api is not None:
                special_button_available = toggle_enabled and g6_api.sbx_smart_volume_special_available()

            self.__night_button.Enable(special_button_available)
            self.__loud_button.Enable(special_button_available)

        def bind_night_button_event(self, handler: Callable[[wx.CommandEvent], None]) -> None:
            self.__night_button.Bind(wx.EVT_BUTTON, handler)

        def bind_loud_button_event(self, handler: Callable[[wx.CommandEvent], None]) -> None:
            self.__loud_button.Bind(wx.EVT_BUTTON, handler)

    def __init__(self):
        self.__g6_api: None | G6Api = None
        self.__cmp_surround = None
        self.__cmp_crystalizer = None
        self.__cmp_bass = None
        self.__cmp_smart_volume = None
        self.__cmp_dialog_plus = None

    def create(self, notebook: wx.Notebook) -> wx.Panel:
        panel = wx.Panel(notebook)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # add components to vbox
        flags = wx.ALL | wx.EXPAND

        ## surround
        self.__cmp_surround = SbxTab.SliderComposite(panel, "Surround")
        self.__cmp_surround.bind_toggle_event(lambda event: self.on_toggle(slider_composite=self.__cmp_surround,
                                                                           audio_feature=AudioFeature.SURROUND_TOGGLE,
                                                                           event=event))
        self.__cmp_surround.bind_slider_event(lambda event: self.on_slide(slider_composite=self.__cmp_surround,
                                                                          audio_feature=AudioFeature.SURROUND_SLIDER))
        vbox.Add(self.__cmp_surround, flag=flags, border=5)

        ## crystalizer
        self.__cmp_crystalizer = SbxTab.SliderComposite(panel, "Crystalizer")
        self.__cmp_crystalizer.bind_toggle_event(lambda event: self.on_toggle(slider_composite=self.__cmp_crystalizer,
                                                                              audio_feature=AudioFeature.CRYSTALIZER_TOGGLE,
                                                                              event=event))
        self.__cmp_crystalizer.bind_slider_event(lambda event: self.on_slide(slider_composite=self.__cmp_crystalizer,
                                                                             audio_feature=AudioFeature.CRYSTALIZER_SLIDER))
        vbox.Add(self.__cmp_crystalizer, flag=flags, border=5)

        ## bass
        self.__cmp_bass = SbxTab.SliderComposite(panel, "Bass")
        self.__cmp_bass.bind_toggle_event(lambda event: self.on_toggle(slider_composite=self.__cmp_bass,
                                                                       audio_feature=AudioFeature.BASS_TOGGLE,
                                                                       event=event))
        self.__cmp_bass.bind_slider_event(lambda event: self.on_slide(slider_composite=self.__cmp_bass,
                                                                      audio_feature=AudioFeature.BASS_SLIDER))
        vbox.Add(self.__cmp_bass, flag=flags, border=5)

        ## smart volume
        self.__cmp_smart_volume = SbxTab.SmartVolumeSpecialComposite(panel, "Smart Volume")
        self.__cmp_smart_volume.bind_toggle_event(lambda event: self.on_toggle(slider_composite=self.__cmp_smart_volume,
                                                                               audio_feature=AudioFeature.SMART_VOLUME_TOGGLE,
                                                                               event=event))
        self.__cmp_smart_volume.bind_slider_event(lambda event: self.on_slide(slider_composite=self.__cmp_smart_volume,
                                                                              audio_feature=AudioFeature.SMART_VOLUME_SLIDER))
        self.__cmp_smart_volume.bind_night_button_event(lambda event: self.on_smart_volume_special(
            smart_volume_special_hex=SmartVolumeSpecialHex.SMART_VOLUME_NIGHT))
        self.__cmp_smart_volume.bind_loud_button_event(lambda event: self.on_smart_volume_special(
            smart_volume_special_hex=SmartVolumeSpecialHex.SMART_VOLUME_LOUD))
        vbox.Add(self.__cmp_smart_volume, flag=flags, border=5)

        ## dialog plus
        self.__cmp_dialog_plus = SbxTab.SliderComposite(panel, "Dialog Plus")
        self.__cmp_dialog_plus.bind_toggle_event(lambda event: self.on_toggle(slider_composite=self.__cmp_dialog_plus,
                                                                              audio_feature=AudioFeature.DIALOG_PLUS_TOGGLE,
                                                                              event=event))
        self.__cmp_dialog_plus.bind_slider_event(lambda event: self.on_slide(slider_composite=self.__cmp_dialog_plus,
                                                                             audio_feature=AudioFeature.DIALOG_PLUS_SLIDER))
        vbox.Add(self.__cmp_dialog_plus, flag=flags, border=5)

        panel.SetSizer(vbox)
        return panel

    def update_availability(self, g6_api: G6Api | None):
        self.__g6_api = g6_api
        self.__cmp_surround.update_availability(g6_api=g6_api)
        self.__cmp_crystalizer.update_availability(g6_api=g6_api)
        self.__cmp_bass.update_availability(g6_api=g6_api)
        self.__cmp_smart_volume.update_availability(g6_api=g6_api)
        self.__cmp_dialog_plus.update_availability(g6_api=g6_api)

    def on_toggle(self, slider_composite: SliderComposite, audio_feature: AudioFeature, event):
        # get the toggle button and the button's state
        toggle = event.GetEventObject()
        toggle_value = toggle.GetValue()

        # enable or disable slider
        slider_composite.set_slider_enabled(toggle_value)

        # enable or disable special buttons
        slider_composite.set_special_buttons_enabled(toggle_value)

        # update toggle button label
        toggle.SetLabel("Enabled" if toggle_value else "Disabled")

        if self.__g6_api is not None:
            self.__g6_api.sbx_toggle(audio_feature=audio_feature, activate=toggle_value)
            self.on_slide(slider_composite=slider_composite, audio_feature=audio_feature)

    def on_slide(self, slider_composite: SliderComposite, audio_feature: AudioFeature):
        if self.__g6_api is not None:
            slider_value = slider_composite.get_slider_value()
            self.__g6_api.sbx_slider(audio_feature=audio_feature, value=slider_value)

    def on_smart_volume_special(self, smart_volume_special_hex: SmartVolumeSpecialHex):
        if self.__g6_api is not None:
            self.__g6_api.sbx_smart_volume_special(smart_volume_special_hex=smart_volume_special_hex)
