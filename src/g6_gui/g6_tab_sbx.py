from collections.abc import Callable

import wx

from g6_cli import G6Api, AudioFeature, SmartVolumeSpecialHex
from g6_gui.g6_models import AudioComponent, AudioComponentSmartVolume
from g6_cli.g6_model.sbx import Profile


class Model:
    def __init__(self):
        self.__view: View | None = None
        self.__surround = AudioComponent()
        self.__crystalizer = AudioComponent()
        self.__bass = AudioComponent()
        self.__smart_volume = AudioComponentSmartVolume()
        self.__dialog_plus = AudioComponent()
        self.__profile: Profile.Name | None = None
        self.__profile_available = False  # HID

    def bind(self, view: "View"):
        self.__view = view

    # --- selected profile ---

    def get_profile(self) -> Profile.Name | None:
        return self.__profile

    def set_profile(self, profile_name: Profile.Name):
        self.__profile = profile_name
        self.__view.set_profile_toggle_selection(self.__profile)

    def set_profiles_available(self, available: bool):
        self.__profile_available = available
        self.__view.set_profile_toggles_enabled(enabled=available)

    # --- surround ---

    def is_surround_available(self) -> bool:
        return self.__surround.is_available()

    def set_surround_available(self, available: bool):
        self.__surround.set_available(available)
        self.__handle_surround_enabled()

    def is_surround_active(self) -> bool:
        return self.__surround.is_active()

    def set_surround_active(self, active: bool):
        self.__surround.set_active(active)
        self.__handle_surround_enabled()

    def get_surround_value(self) -> int:
        return self.__surround.get_value()

    def set_surround_value(self, value: int):
        self.__surround.set_value(value)
        self.__view.set_surround_slider_value(value)

    def __handle_surround_enabled(self):
        available = self.__surround.is_available()
        active = self.__surround.is_active()
        active_and_available = available and active
        self.__view.set_surround_toggle_enabled(available)
        self.__view.set_surround_toggle_value(active)
        self.__view.set_surround_slider_enabled(active_and_available)
        self.__view.set_surround_special_buttons_enabled(active_and_available)

    # --- crystalizer ---

    def is_crystalizer_available(self) -> bool:
        return self.__crystalizer.is_available()

    def set_crystalizer_available(self, available: bool):
        self.__crystalizer.set_available(available)
        self.__handle_crystalizer_enabled()

    def is_crystalizer_active(self) -> bool:
        return self.__crystalizer.is_active()

    def set_crystalizer_active(self, active: bool):
        self.__crystalizer.set_active(active)
        self.__handle_crystalizer_enabled()

    def get_crystalizer_value(self) -> int:
        return self.__crystalizer.get_value()

    def set_crystalizer_value(self, value: int):
        self.__crystalizer.set_value(value)
        self.__view.set_crystalizer_slider_value(value)

    def __handle_crystalizer_enabled(self):
        available = self.__crystalizer.is_available()
        active = self.__crystalizer.is_active()
        active_and_available = available and active
        self.__view.set_crystalizer_toggle_enabled(available)
        self.__view.set_crystalizer_toggle_value(active)
        self.__view.set_crystalizer_slider_enabled(active_and_available)
        self.__view.set_crystalizer_special_buttons_enabled(active_and_available)

    # --- bass ---

    def is_bass_available(self) -> bool:
        return self.__bass.is_available()

    def set_bass_available(self, available: bool):
        self.__bass.set_available(available)
        self.__handle_bass_enabled()

    def is_bass_active(self) -> bool:
        return self.__bass.is_active()

    def set_bass_active(self, active: bool):
        self.__bass.set_active(active)
        self.__handle_bass_enabled()

    def get_bass_value(self) -> int:
        return self.__bass.get_value()

    def set_bass_value(self, value: int):
        self.__bass.set_value(value)
        self.__view.set_bass_slider_value(value)

    def __handle_bass_enabled(self):
        available = self.__bass.is_available()
        active = self.__bass.is_active()
        active_and_available = available and active
        self.__view.set_bass_toggle_enabled(available)
        self.__view.set_bass_toggle_value(active)
        self.__view.set_bass_slider_enabled(active_and_available)
        self.__view.set_bass_special_buttons_enabled(active_and_available)

    # --- smart volume ---
    def is_smart_volume_available(self) -> bool:
        return self.__smart_volume.is_available()

    def set_smart_volume_available(self, available: bool):
        self.__smart_volume.set_available(available)
        self.__handle_smart_volume_enabled()

    def is_smart_volume_active(self) -> bool:
        return self.__smart_volume.is_active()

    def set_smart_volume_active(self, active: bool):
        self.__smart_volume.set_active(active)
        self.__handle_smart_volume_enabled()

    def get_smart_volume_value(self) -> int:
        return self.__smart_volume.get_value()

    def set_smart_volume_value(self, value: int):
        self.__smart_volume.set_value(value)
        self.__view.set_smart_volume_slider_value(value)

    def set_smart_volume_night_mode(self):
        self.__smart_volume.set_night_mode()

    def set_smart_volume_loud_mode(self):
        self.__smart_volume.set_loud_mode()

    def __handle_smart_volume_enabled(self):
        available = self.__smart_volume.is_available()
        active = self.__smart_volume.is_active()
        active_and_available = available and active
        self.__view.set_smart_volume_toggle_enabled(available)
        self.__view.set_smart_volume_toggle_value(active)
        self.__view.set_smart_volume_slider_enabled(active_and_available)
        self.__view.set_smart_volume_special_buttons_enabled(active_and_available)

    # --- dialog plus ---

    def is_dialog_plus_available(self) -> bool:
        return self.__dialog_plus.is_available()

    def set_dialog_plus_available(self, available: bool):
        self.__dialog_plus.set_available(available)
        self.__handle_dialog_plus_enabled()

    def is_dialog_plus_active(self) -> bool:
        return self.__dialog_plus.is_active()

    def set_dialog_plus_active(self, active: bool):
        self.__dialog_plus.set_active(active)
        self.__handle_dialog_plus_enabled()

    def get_dialog_plus_value(self) -> int:
        return self.__dialog_plus.get_value()

    def set_dialog_plus_value(self, value: int):
        self.__dialog_plus.set_value(value)
        self.__view.set_dialog_plus_slider_value(value)

    def __handle_dialog_plus_enabled(self):
        available = self.__dialog_plus.is_available()
        active = self.__dialog_plus.is_active()
        active_and_available = available and active
        self.__view.set_dialog_plus_toggle_enabled(available)
        self.__view.set_dialog_plus_toggle_value(active)
        self.__view.set_dialog_plus_slider_enabled(active_and_available)
        self.__view.set_dialog_plus_special_buttons_enabled(active_and_available)


class View:
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
            self.__slider.Bind(wx.EVT_SCROLL_CHANGED, handler)

        def update_availability(self, g6_api: G6Api | None):
            toggle_value = self.get_toggle_value()

            slider_available = False
            toggle_available = False
            if g6_api is not None:
                slider_available = toggle_value and g6_api.sbx_slider_available()
                toggle_available = g6_api.sbx_toggle_available()

            self.__slider.Enable(slider_available)
            self.__toggle.Enable(toggle_available)

        def get_toggle_value(self) -> bool:
            return self.__toggle.GetValue()

        def set_toggle_value(self, value: bool):
            self.__toggle.SetValue(value)
            self.__toggle.SetLabel("Enabled" if value else "Disabled")

        def is_toggle_enabled(self) -> bool:
            return self.__toggle.IsEnabled()

        def set_toggle_enabled(self, enabled: bool):
            self.__toggle.Enable(enabled)

        def is_slider_enabled(self) -> bool:
            return self.__slider.IsEnabled()

        def set_slider_enabled(self, enabled: bool):
            self.__slider.Enable(enabled)

        def set_special_buttons_enabled(self, enabled: bool):
            for special_button in self.__special_button_list:
                special_button.Enable(enabled)

        def get_slider_value(self) -> int:
            return self.__slider.Value

        def set_slider_value(self, value: int):
            self.__slider.SetValue(value)

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
            toggle_value = self.get_toggle_value()

            special_button_available = False
            if g6_api is not None:
                special_button_available = toggle_value and g6_api.sbx_smart_volume_special_available()

            self.__night_button.Enable(special_button_available)
            self.__loud_button.Enable(special_button_available)

        def bind_night_button_event(self, handler: Callable[[wx.CommandEvent], None]) -> None:
            self.__night_button.Bind(wx.EVT_BUTTON, handler)

        def bind_loud_button_event(self, handler: Callable[[wx.CommandEvent], None]) -> None:
            self.__loud_button.Bind(wx.EVT_BUTTON, handler)

    def __init__(self):
        self.__controller: Controller | None = None
        self.__g6_api: None | G6Api = None
        self.__cmp_surround = None
        self.__cmp_crystalizer = None
        self.__cmp_bass = None
        self.__cmp_smart_volume = None
        self.__cmp_dialog_plus = None
        self.__profile_button_dict: dict[Profile.Name, wx.ToggleButton] = {}

    def bind(self, controller: "Controller"):
        self.__controller = controller

    def create(self, notebook: wx.Notebook) -> wx.Panel:
        panel = wx.Panel(notebook)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # add components to vbox
        flags = wx.ALL | wx.EXPAND

        ## surround
        self.__cmp_surround = View.SliderComposite(panel, "Surround")
        self.__cmp_surround.bind_toggle_event(
            lambda event: self.__controller.on_toggle(audio_feature=AudioFeature.SURROUND_TOGGLE,
                                                      event=event))
        self.__cmp_surround.bind_slider_event(
            lambda event: self.__controller.on_slide(audio_feature=AudioFeature.SURROUND_SLIDER, event=event))
        vbox.Add(self.__cmp_surround, flag=flags, border=5)

        ## crystalizer
        self.__cmp_crystalizer = View.SliderComposite(panel, "Crystalizer")
        self.__cmp_crystalizer.bind_toggle_event(
            lambda event: self.__controller.on_toggle(audio_feature=AudioFeature.CRYSTALIZER_TOGGLE, event=event))
        self.__cmp_crystalizer.bind_slider_event(
            lambda event: self.__controller.on_slide(audio_feature=AudioFeature.CRYSTALIZER_SLIDER, event=event))
        vbox.Add(self.__cmp_crystalizer, flag=flags, border=5)

        ## bass
        self.__cmp_bass = View.SliderComposite(panel, "Bass")
        self.__cmp_bass.bind_toggle_event(
            lambda event: self.__controller.on_toggle(audio_feature=AudioFeature.BASS_TOGGLE, event=event))
        self.__cmp_bass.bind_slider_event(lambda event: self.__controller.on_slide(
            audio_feature=AudioFeature.BASS_SLIDER, event=event))
        vbox.Add(self.__cmp_bass, flag=flags, border=5)

        ## smart volume
        self.__cmp_smart_volume = View.SmartVolumeSpecialComposite(panel, "Smart Volume")
        self.__cmp_smart_volume.bind_toggle_event(
            lambda event: self.__controller.on_toggle(audio_feature=AudioFeature.SMART_VOLUME_TOGGLE,
                                                      event=event))
        self.__cmp_smart_volume.bind_slider_event(
            lambda event: self.__controller.on_slide(audio_feature=AudioFeature.SMART_VOLUME_SLIDER, event=event))
        self.__cmp_smart_volume.bind_night_button_event(lambda event: self.__controller.on_smart_volume_special(
            smart_volume_special_hex=SmartVolumeSpecialHex.SMART_VOLUME_NIGHT))
        self.__cmp_smart_volume.bind_loud_button_event(lambda event: self.__controller.on_smart_volume_special(
            smart_volume_special_hex=SmartVolumeSpecialHex.SMART_VOLUME_LOUD))
        vbox.Add(self.__cmp_smart_volume, flag=flags, border=5)

        ## dialog plus
        self.__cmp_dialog_plus = View.SliderComposite(panel, "Dialog Plus")
        self.__cmp_dialog_plus.bind_toggle_event(
            lambda event: self.__controller.on_toggle(audio_feature=AudioFeature.DIALOG_PLUS_TOGGLE, event=event))
        self.__cmp_dialog_plus.bind_slider_event(
            lambda event: self.__controller.on_slide(audio_feature=AudioFeature.DIALOG_PLUS_SLIDER, event=event))
        vbox.Add(self.__cmp_dialog_plus, flag=flags, border=5)

        ## SBX profiles
        hbox_profiles = wx.BoxSizer(wx.HORIZONTAL)

        # build __profile_button_dict
        for profile_name in Profile.Name:
            # Toggle buttons sized larger (like the original SoundBlaster Command Windows app)
            # Images can be added here (uncomment/adjust paths when icon assets are available):
            #   icon_path = f"icons/{profile_name.value.lower()}.png"
            #   if os.path.exists(icon_path):
            #       bmp = wx.Bitmap(icon_path)
            #       btn.SetBitmap(bmp)          # wx.ToggleButton supports bitmap in wxPython 4+
            btn = wx.ToggleButton(panel, label=profile_name.value, size=wx.Size(130, 65))
            self.__profile_button_dict[profile_name] = btn

            # Bind directly (lambda captures the profile enum)
            btn.Bind(wx.EVT_TOGGLEBUTTON,
                     lambda event, pn=profile_name: self.__controller.on_profile_selected(pn))

            # Add button to hbox_profiles
            hbox_profiles.Add(btn, proportion=1, flag=wx.ALL | wx.EXPAND, border=5)

        # Add hbox_profiles to vbox
        vbox.Add(hbox_profiles, flag=flags, border=5)

        panel.SetSizer(vbox)
        return panel

    def update_availability(self, g6_api: G6Api | None):
        self.__g6_api = g6_api
        self.__cmp_surround.update_availability(g6_api=g6_api)
        self.__cmp_crystalizer.update_availability(g6_api=g6_api)
        self.__cmp_bass.update_availability(g6_api=g6_api)
        self.__cmp_smart_volume.update_availability(g6_api=g6_api)
        self.__cmp_dialog_plus.update_availability(g6_api=g6_api)

    def set_profile_toggle_selection(self, profile_name: Profile.Name):
        """Visually select only the chosen profile button (mutually exclusive)."""
        for button_profile_name, toggle_button in self.__profile_button_dict.items():
            toggle_button.SetValue(button_profile_name == profile_name)

    def set_profile_toggles_enabled(self, enabled: bool):
        """Enable or disable the profile toggle buttons."""
        for button_profile_name, toggle_button in self.__profile_button_dict.items():
            toggle_button.Enable(enable=enabled)

    def get_surround_toggle_value(self) -> bool:
        return self.__cmp_surround.get_toggle_value()

    def set_surround_toggle_value(self, enabled: bool):
        self.__cmp_surround.set_toggle_value(enabled)

    def get_surround_toggle_enabled(self) -> bool:
        return self.__cmp_surround.is_toggle_enabled()

    def set_surround_toggle_enabled(self, enabled: bool):
        self.__cmp_surround.set_toggle_enabled(enabled)

    def get_surround_slider_value(self) -> int:
        return self.__cmp_surround.get_slider_value()

    def set_surround_slider_value(self, value: int):
        self.__cmp_surround.set_slider_value(value)

    def set_surround_slider_enabled(self, enabled: bool):
        self.__cmp_surround.set_slider_enabled(enabled)

    def set_surround_special_buttons_enabled(self, enabled: bool):
        self.__cmp_surround.set_special_buttons_enabled(enabled)

    def get_crystalizer_toggle_value(self) -> bool:
        return self.__cmp_crystalizer.get_toggle_value()

    def set_crystalizer_toggle_value(self, enabled: bool):
        self.__cmp_crystalizer.set_toggle_value(enabled)

    def get_crystalizer_toggle_enabled(self) -> bool:
        return self.__cmp_crystalizer.is_toggle_enabled()

    def set_crystalizer_toggle_enabled(self, enabled: bool):
        self.__cmp_crystalizer.set_toggle_enabled(enabled)

    def set_crystalizer_slider_enabled(self, enabled: bool):
        self.__cmp_crystalizer.set_slider_enabled(enabled)

    def get_crystalizer_slider_value(self) -> int:
        return self.__cmp_crystalizer.get_slider_value()

    def set_crystalizer_slider_value(self, value: int):
        self.__cmp_crystalizer.set_slider_value(value)

    def set_crystalizer_special_buttons_enabled(self, enabled: bool):
        self.__cmp_crystalizer.set_special_buttons_enabled(enabled)

    def get_bass_toggle_value(self) -> bool:
        return self.__cmp_bass.get_toggle_value()

    def set_bass_toggle_value(self, enabled: bool):
        self.__cmp_bass.set_toggle_value(enabled)

    def get_bass_toggle_enabled(self) -> bool:
        return self.__cmp_bass.is_toggle_enabled()

    def set_bass_toggle_enabled(self, enabled: bool):
        self.__cmp_bass.set_toggle_enabled(enabled)

    def get_bass_slider_value(self) -> int:
        return self.__cmp_bass.get_slider_value()

    def set_bass_slider_value(self, value: int):
        self.__cmp_bass.set_slider_value(value)

    def set_bass_slider_enabled(self, enabled: bool):
        self.__cmp_bass.set_slider_enabled(enabled)

    def set_bass_special_buttons_enabled(self, enabled: bool):
        self.__cmp_bass.set_special_buttons_enabled(enabled)

    def get_smart_volume_toggle_value(self) -> bool:
        return self.__cmp_smart_volume.get_toggle_value()

    def set_smart_volume_toggle_value(self, enabled: bool):
        self.__cmp_smart_volume.set_toggle_value(enabled)

    def get_smart_volume_toggle_enabled(self) -> bool:
        return self.__cmp_smart_volume.is_toggle_enabled()

    def set_smart_volume_toggle_enabled(self, enabled: bool):
        self.__cmp_smart_volume.set_toggle_enabled(enabled)

    def get_smart_volume_slider_value(self) -> int:
        return self.__cmp_smart_volume.get_slider_value()

    def set_smart_volume_slider_value(self, value: int):
        self.__cmp_smart_volume.set_slider_value(value)

    def set_smart_volume_slider_enabled(self, enabled: bool):
        self.__cmp_smart_volume.set_slider_enabled(enabled)

    def set_smart_volume_special_buttons_enabled(self, enabled: bool):
        self.__cmp_smart_volume.set_special_buttons_enabled(enabled)

    def get_dialog_plus_toggle_value(self) -> bool:
        return self.__cmp_dialog_plus.get_toggle_value()

    def set_dialog_plus_toggle_value(self, enabled: bool):
        self.__cmp_dialog_plus.set_toggle_value(enabled)

    def get_dialog_plus_toggle_enabled(self) -> bool:
        return self.__cmp_dialog_plus.is_toggle_enabled()

    def set_dialog_plus_toggle_enabled(self, enabled: bool):
        self.__cmp_dialog_plus.set_toggle_enabled(enabled)

    def get_dialog_plus_slider_value(self) -> int:
        return self.__cmp_dialog_plus.get_slider_value()

    def set_dialog_plus_slider_value(self, value: int):
        self.__cmp_dialog_plus.set_slider_value(value)

    def set_dialog_plus_slider_enabled(self, enabled: bool):
        self.__cmp_dialog_plus.set_slider_enabled(enabled)

    def set_dialog_plus_special_buttons_enabled(self, enabled: bool):
        self.__cmp_dialog_plus.set_special_buttons_enabled(enabled)


class Controller:
    def __init__(self):
        self.__model: Model | None = None
        self.__view: View | None = None  # use only in exceptional cases, update the view indirectly by using the model
        self.__g6_api: G6Api | None = None

    def bind(self, model: Model, view: View):
        self.__model = model
        self.__view = view

    def update_availability(self, g6_api: G6Api | None):
        self.__g6_api = g6_api

        slider_available = False
        toggle_available = False
        if self.__g6_api is not None:
            slider_available = self.__g6_api.sbx_slider_available()
            toggle_available = self.__g6_api.sbx_toggle_available()
        available = slider_available and toggle_available

        self.__model.set_surround_available(available)
        self.__model.set_bass_available(available)
        self.__model.set_crystalizer_available(available)
        self.__model.set_smart_volume_available(available)
        self.__model.set_dialog_plus_available(available)
        self.__model.set_profiles_available(available)

        # load the currently selected profile and sync UI with model
        if self.__g6_api is not None:
            current_profile = self.__g6_api.sbx_profile_selection()
            if current_profile is None:
                raise RuntimeError("Requested SBX profile from g6_api is None!")
            self.__apply_profile(current_profile)

    def on_profile_selected(self, profile_name: Profile.Name):
        # update model
        self.__apply_profile(profile_name)

        # send profile switch to G6
        if self.__g6_api is not None:
            self.__g6_api.sbx_profile_switch(profile_name=profile_name)

    def __apply_profile(self, profile_name: Profile.Name):
        # request sbx model from g6_api
        if self.__g6_api is None:
            return
        g6_model = self.__g6_api.get_model()
        sbx = g6_model.get_sbx(profile_name=profile_name)

        # update selected profile
        self.__model.set_profile(profile_name)

        # surround
        self.__model.set_surround_active(sbx.get_surround_toggle())
        self.__model.set_surround_value(sbx.get_surround_slider())
        # crystalizer
        self.__model.set_crystalizer_active(sbx.get_crystalizer_toggle())
        self.__model.set_crystalizer_value(sbx.get_crystalizer_slider())
        # bass
        self.__model.set_bass_active(sbx.get_bass_toggle())
        self.__model.set_bass_value(sbx.get_bass_slider())
        # dialog plus
        self.__model.set_dialog_plus_active(sbx.get_dialog_plus_toggle())
        self.__model.set_dialog_plus_value(sbx.get_dialog_plus_slider())
        # smart volume
        self.__model.set_smart_volume_active(sbx.get_smart_volume_toggle())
        special = sbx.get_smart_volume_special()
        if special is None:
            self.__model.set_smart_volume_value(sbx.get_smart_volume_slider())
        else:
            if special == SmartVolumeSpecialHex.SMART_VOLUME_NIGHT:
                self.__model.set_smart_volume_night_mode()
            elif special == SmartVolumeSpecialHex.SMART_VOLUME_LOUD:
                self.__model.set_smart_volume_loud_mode()

    def on_toggle(self, audio_feature: AudioFeature, event):
        # get the toggle button and the button's state
        toggle = event.GetEventObject()
        toggle_value = toggle.GetValue()

        # update model
        slider_audio_feature: AudioFeature
        slider_value: int
        match audio_feature:
            case AudioFeature.SURROUND_TOGGLE:
                self.__model.set_surround_active(toggle_value)
                slider_audio_feature = AudioFeature.SURROUND_SLIDER
                slider_value = self.__model.get_surround_value()
            case AudioFeature.CRYSTALIZER_TOGGLE:
                self.__model.set_crystalizer_active(toggle_value)
                slider_audio_feature = AudioFeature.CRYSTALIZER_SLIDER
                slider_value = self.__model.get_crystalizer_value()
            case AudioFeature.BASS_TOGGLE:
                self.__model.set_bass_active(toggle_value)
                slider_audio_feature = AudioFeature.BASS_SLIDER
                slider_value = self.__model.get_bass_value()
            case AudioFeature.SMART_VOLUME_TOGGLE:
                self.__model.set_smart_volume_active(toggle_value)
                slider_audio_feature = AudioFeature.SMART_VOLUME_SLIDER
                slider_value = self.__model.get_smart_volume_value()
            case AudioFeature.DIALOG_PLUS_TOGGLE:
                self.__model.set_dialog_plus_active(toggle_value)
                slider_audio_feature = AudioFeature.DIALOG_PLUS_SLIDER
                slider_value = self.__model.get_dialog_plus_value()
            case _:
                raise ValueError(f"Unsupported audio feature: {audio_feature}!")

        # send toggle command to G6
        if self.__g6_api is not None:
            # activate or deactivate audio feature on G6
            self.__g6_api.sbx_toggle(profile_name=self.__model.get_profile(),
                                     audio_feature=audio_feature,
                                     activate=toggle_value)
            self.__on_slide(audio_feature=slider_audio_feature, value=slider_value)

    def on_slide(self, audio_feature: AudioFeature, event):
        # get the slider value
        slider = event.GetEventObject()
        value = slider.GetValue()

        # update the model and send slider command to G6
        self.__on_slide(audio_feature=audio_feature, value=value)

    def __on_slide(self, audio_feature: AudioFeature, value: int):
        # update model
        match audio_feature:
            case AudioFeature.SURROUND_SLIDER:
                self.__model.set_surround_value(value)
            case AudioFeature.CRYSTALIZER_SLIDER:
                self.__model.set_crystalizer_value(value)
            case AudioFeature.BASS_SLIDER:
                self.__model.set_bass_value(value)
            case AudioFeature.DIALOG_PLUS_SLIDER:
                self.__model.set_dialog_plus_value(value)
            case AudioFeature.SMART_VOLUME_SLIDER:
                self.__model.set_smart_volume_value(value)
            case _:
                raise ValueError(f"Unsupported audio feature: {audio_feature}!")

        # send slider value to G6
        if self.__g6_api is not None:
            self.__g6_api.sbx_slider(profile_name=self.__model.get_profile(),
                                     audio_feature=audio_feature,
                                     value=value)

    def on_smart_volume_special(self, smart_volume_special_hex: SmartVolumeSpecialHex):
        # update model
        match smart_volume_special_hex:
            case SmartVolumeSpecialHex.SMART_VOLUME_NIGHT:
                self.__model.set_smart_volume_night_mode()
                self.__model.set_smart_volume_value(0)
            case SmartVolumeSpecialHex.SMART_VOLUME_LOUD:
                self.__model.set_smart_volume_loud_mode()
                self.__model.set_smart_volume_value(100)
            case _:
                raise ValueError(f"Unsupported smart volume special hex: {smart_volume_special_hex}!")

        # send smart volume special command to G6
        if self.__g6_api is not None:
            self.__g6_api.sbx_smart_volume_special(profile_name=self.__model.get_profile(),
                                                   smart_volume_special_hex=smart_volume_special_hex)


class SbxTab:
    def __init__(self):
        self.__model = Model()
        self.__view = View()
        self.__controller = Controller()

        # create bindings
        self.__model.bind(self.__view)
        self.__view.bind(self.__controller)
        self.__controller.bind(self.__model, self.__view)

    def create(self, notebook: wx.Notebook) -> wx.Panel:
        return self.__view.create(notebook)

    def update_availability(self, g6_api: G6Api | None):
        self.__controller.update_availability(g6_api=g6_api)
