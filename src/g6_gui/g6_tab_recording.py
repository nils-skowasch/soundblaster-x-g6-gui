import wx

from g6_cli import G6Api
from g6_cli.g6_spec.recording import MicrophoneEqualizerPreset, MIC_RECORDING_VOLUME_VR, MIC_BOOST_DECIBEL_VR, \
    MIC_MONITORING_VOLUME_VR, VOICE_CLARITY_NOISE_REDUCTION_LEVEL_VR


class Model:
    def __init__(self):
        self.__view: View | None = None

        # --- mic recording volume ---
        self.__mic_recording_volume_available = False
        self.__mic_recording_volume: int = 50

        # --- mic boost ---
        self.__mic_boost_available = False
        self.__mic_boost: int = 10

        # --- mic monitoring ---
        self.__mic_monitoring_available = False
        self.__mic_monitoring_enabled: bool = False
        self.__mic_monitoring_volume: int = 50

        # --- voice clarity ---
        self.__voice_clarity_available = False
        self.__voice_clarity_active: bool = False

        # --- voice clarity > noise reduction ---
        self.__voice_clarity_noise_reduction_available = False
        self.__voice_clarity_noise_reduction_enabled: bool = False
        self.__voice_clarity_noise_reduction_level: int = 40

        # --- voice clarity > acoustic echo cancellation ---
        self.__voice_clarity_acoustic_echo_cancellation_available = False
        self.__voice_clarity_acoustic_echo_cancellation_enabled: bool = False

        # --- voice clarity > smart volume ---
        self.__voice_clarity_smart_volume_available = False
        self.__voice_clarity_smart_volume_enabled: bool = False

        # --- voice clarity > mic equalizer ---
        self.__voice_clarity_mic_equalizer_available = False
        self.__voice_clarity_mic_equalizer_enabled: bool = False
        self.__voice_clarity_mic_equalizer_preset: MicrophoneEqualizerPreset = MicrophoneEqualizerPreset.PRESET_1

    def bind(self, view: "View"):
        self.__view = view

    # --- mic recording volume ---

    def is_mic_recording_volume_available(self) -> bool:
        return self.__mic_recording_volume_available

    def set_mic_recording_volume_available(self, available: bool) -> None:
        self.__mic_recording_volume_available = available
        self.__handle_mic_recording_volume_enabled()

    def get_mic_recording_volume(self) -> int:
        return self.__mic_recording_volume

    def set_mic_recording_volume(self, volume: int) -> None:
        self.__mic_recording_volume = volume
        self.__view.set_mic_recording_volume_value(volume)

    def __handle_mic_recording_volume_enabled(self) -> None:
        self.__view.set_mic_recording_volume_enabled(self.__mic_recording_volume_available)

    # --- mic boost ---

    def is_mic_boost_available(self) -> bool:
        return self.__mic_boost_available

    def set_mic_boost_available(self, available: bool) -> None:
        self.__mic_boost_available = available
        self.__handle_mic_boost_enabled()

    def get_mic_boost(self) -> int:
        return self.__mic_boost

    def set_mic_boost(self, boost: int) -> None:
        self.__mic_boost = boost
        self.__view.set_mic_boost_value(boost)

    def __handle_mic_boost_enabled(self) -> None:
        self.__view.set_mic_boost_enabled(self.__mic_boost_available)

    # --- mic monitoring ---

    def is_mic_monitoring_available(self) -> bool:
        return self.__mic_monitoring_available

    def set_mic_monitoring_available(self, available: bool) -> None:
        self.__mic_monitoring_available = available
        self.__handle_mic_monitoring_enabled()

    def is_mic_monitoring_enabled(self) -> bool:
        return self.__mic_monitoring_enabled

    def set_mic_monitoring_enabled(self, enabled: bool) -> None:
        self.__mic_monitoring_enabled = enabled
        self.__view.set_mic_monitoring_checkbox_value(enabled)
        self.__handle_mic_monitoring_enabled()

    def get_mic_monitoring_volume(self) -> int:
        return self.__mic_monitoring_volume

    def set_mic_monitoring_volume(self, volume: int) -> None:
        self.__mic_monitoring_volume = volume
        self.__view.set_mic_monitoring_volume_value(volume)

    def __handle_mic_monitoring_enabled(self) -> None:
        self.__view.set_mic_monitoring_checkbox_enabled(self.__mic_monitoring_available)
        self.__view.set_mic_monitoring_volume_enabled(
            self.__mic_monitoring_available and self.__mic_monitoring_enabled
        )

    # --- voice clarity ---

    def is_voice_clarity_available(self) -> bool:
        return self.__voice_clarity_available

    def set_voice_clarity_available(self, available: bool) -> None:
        self.__voice_clarity_available = available
        self.__handle_voice_clarity_enabled()

    def is_voice_clarity_active(self) -> bool:
        return self.__voice_clarity_active

    def set_voice_clarity_active(self, active: bool) -> None:
        self.__voice_clarity_active = active
        self.__view.set_voice_clarity_toggle_value(active)
        self.__handle_voice_clarity_enabled()

    def __handle_voice_clarity_enabled(self) -> None:
        self.__view.set_voice_clarity_toggle_enabled(self.__voice_clarity_available)
        self.__handle_voice_clarity_noise_reduction_enabled()
        self.__handle_voice_clarity_acoustic_echo_cancellation_enabled()
        self.__handle_voice_clarity_smart_volume_enabled()
        self.__handle_voice_clarity_mic_equalizer_enabled()

    # --- voice clarity > noise reduction ---

    def is_voice_clarity_noise_reduction_available(self) -> bool:
        return self.__voice_clarity_noise_reduction_available

    def set_voice_clarity_noise_reduction_available(self, available: bool) -> None:
        self.__voice_clarity_noise_reduction_available = available
        self.__handle_voice_clarity_noise_reduction_enabled()

    def is_voice_clarity_noise_reduction_enabled(self) -> bool:
        return self.__voice_clarity_noise_reduction_enabled

    def set_voice_clarity_noise_reduction_enabled(self, enabled: bool) -> None:
        self.__voice_clarity_noise_reduction_enabled = enabled
        self.__view.set_voice_clarity_noise_reduction_checkbox_value(enabled)
        self.__handle_voice_clarity_noise_reduction_enabled()

    def get_voice_clarity_noise_reduction_level(self) -> int:
        return self.__voice_clarity_noise_reduction_level

    def set_voice_clarity_noise_reduction_level(self, level: int) -> None:
        self.__voice_clarity_noise_reduction_level = level
        self.__view.set_voice_clarity_noise_reduction_slider_value(level)

    def __handle_voice_clarity_noise_reduction_enabled(self) -> None:
        available_and_voice_clarity_active = (
                self.__voice_clarity_noise_reduction_available and self.__voice_clarity_active
        )
        self.__view.set_voice_clarity_noise_reduction_checkbox_enabled(available_and_voice_clarity_active)
        self.__view.set_voice_clarity_noise_reduction_slider_enabled(
            available_and_voice_clarity_active and self.__voice_clarity_noise_reduction_enabled
        )

    # --- voice clarity > acoustic echo cancellation ---

    def is_voice_clarity_acoustic_echo_cancellation_available(self) -> bool:
        return self.__voice_clarity_acoustic_echo_cancellation_available

    def set_voice_clarity_acoustic_echo_cancellation_available(self, available: bool) -> None:
        self.__voice_clarity_acoustic_echo_cancellation_available = available
        self.__handle_voice_clarity_acoustic_echo_cancellation_enabled()

    def is_voice_clarity_acoustic_echo_cancellation_enabled(self) -> bool:
        return self.__voice_clarity_acoustic_echo_cancellation_enabled

    def set_voice_clarity_acoustic_echo_cancellation_enabled(self, enabled: bool) -> None:
        self.__voice_clarity_acoustic_echo_cancellation_enabled = enabled
        self.__view.set_voice_clarity_acoustic_echo_cancellation_value(enabled)

    def __handle_voice_clarity_acoustic_echo_cancellation_enabled(self) -> None:
        available_and_voice_clarity_active = (
                self.__voice_clarity_acoustic_echo_cancellation_available and self.__voice_clarity_active
        )
        self.__view.set_voice_clarity_acoustic_echo_cancellation_enabled(available_and_voice_clarity_active)

    # --- voice clarity > smart volume ---

    def is_voice_clarity_smart_volume_available(self) -> bool:
        return self.__voice_clarity_smart_volume_available

    def set_voice_clarity_smart_volume_available(self, available: bool) -> None:
        self.__voice_clarity_smart_volume_available = available
        self.__handle_voice_clarity_smart_volume_enabled()

    def is_voice_clarity_smart_volume_enabled(self) -> bool:
        return self.__voice_clarity_smart_volume_enabled

    def set_voice_clarity_smart_volume_enabled(self, enabled: bool) -> None:
        self.__voice_clarity_smart_volume_enabled = enabled
        self.__view.set_voice_clarity_smart_volume_value(enabled)

    def __handle_voice_clarity_smart_volume_enabled(self) -> None:
        available_and_voice_clarity_active = (
                self.__voice_clarity_smart_volume_available and self.__voice_clarity_active
        )
        self.__view.set_voice_clarity_smart_volume_enabled(available_and_voice_clarity_active)

    # --- voice clarity > mic equalizer ---

    def is_voice_clarity_mic_equalizer_available(self) -> bool:
        return self.__voice_clarity_mic_equalizer_available

    def set_voice_clarity_mic_equalizer_available(self, available: bool) -> None:
        self.__voice_clarity_mic_equalizer_available = available
        self.__handle_voice_clarity_mic_equalizer_enabled()

    def is_voice_clarity_mic_equalizer_enabled(self) -> bool:
        return self.__voice_clarity_mic_equalizer_enabled

    def set_voice_clarity_mic_equalizer_enabled(self, enabled: bool) -> None:
        self.__voice_clarity_mic_equalizer_enabled = enabled
        self.__view.set_voice_clarity_mic_equalizer_checkbox_value(enabled)
        self.__handle_voice_clarity_mic_equalizer_enabled()

    def get_voice_clarity_mic_equalizer_preset(self) -> MicrophoneEqualizerPreset:
        return self.__voice_clarity_mic_equalizer_preset

    def set_voice_clarity_mic_equalizer_preset(self, preset: MicrophoneEqualizerPreset) -> None:
        self.__voice_clarity_mic_equalizer_preset = preset
        self.__view.set_voice_clarity_mic_equalizer_preset_value(preset)

    def __handle_voice_clarity_mic_equalizer_enabled(self) -> None:
        available_and_voice_clarity_active = (
                self.__voice_clarity_mic_equalizer_available and self.__voice_clarity_active
        )
        self.__view.set_voice_clarity_mic_equalizer_checkbox_enabled(available_and_voice_clarity_active)
        self.__view.set_voice_clarity_mic_equalizer_preset_enabled(
            available_and_voice_clarity_active and self.__voice_clarity_mic_equalizer_enabled
        )


class View:
    MIC_EQ_PRESET_CHOICES = [
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
        "Preset DM-1 - Improve vocal clarity",
    ]

    def __init__(self):
        self.__controller: Controller | None = None

        self.__sld_mic_volume: wx.Slider | None = None
        self.__sld_mic_boost: wx.Slider | None = None
        self.__chk_mic_monitoring: wx.CheckBox | None = None
        self.__sld_mic_monitoring: wx.Slider | None = None
        self.__tgl_voice_clarity: wx.ToggleButton | None = None
        self.__chk_noise_reduction: wx.CheckBox | None = None
        self.__sld_noise_reduction: wx.Slider | None = None
        self.__chk_echo_cancellation: wx.CheckBox | None = None
        self.__chk_smart_volume: wx.CheckBox | None = None
        self.__chk_mic_eq: wx.CheckBox | None = None
        self.__cmb_mic_eq_preset: wx.ComboBox | None = None

    def bind(self, controller: "Controller"):
        self.__controller = controller

    def create(self, notebook: wx.Notebook) -> wx.Panel:
        panel = wx.Panel(notebook)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # microphone recording volume
        vbox.Add(wx.StaticText(panel, label="Mic-Recording volume"), 0, wx.ALL, 5)
        self.__sld_mic_volume = wx.Slider(panel,
                                          minValue=MIC_RECORDING_VOLUME_VR.get_min_value() // MIC_RECORDING_VOLUME_VR.get_step_size(),
                                          maxValue=MIC_RECORDING_VOLUME_VR.get_max_value() // MIC_RECORDING_VOLUME_VR.get_step_size(),
                                          value=50 // MIC_RECORDING_VOLUME_VR.get_step_size(),
                                          style=wx.SL_HORIZONTAL)
        self.__sld_mic_volume.Bind(wx.EVT_SCROLL_CHANGED,
                                   lambda event: self.__controller.on_change_mic_recording_volume(event))
        vbox.Add(self.__sld_mic_volume, 0, wx.ALL | wx.EXPAND, 5)

        # microphone boost
        vbox.Add(wx.StaticText(panel, label="Microphone boost"), 0, wx.ALL, 5)
        self.__sld_mic_boost = wx.Slider(panel,
                                         minValue=MIC_BOOST_DECIBEL_VR.get_min_value() // MIC_BOOST_DECIBEL_VR.get_step_size(),
                                         maxValue=MIC_BOOST_DECIBEL_VR.get_max_value() // MIC_BOOST_DECIBEL_VR.get_step_size(),
                                         value=10 // MIC_BOOST_DECIBEL_VR.get_step_size(),
                                         style=wx.SL_HORIZONTAL)
        self.__sld_mic_boost.Bind(wx.EVT_SCROLL_CHANGED, lambda event: self.__controller.on_change_mic_boost(event))
        vbox.Add(self.__sld_mic_boost, 0, wx.ALL | wx.EXPAND, 5)

        # mic monitoring
        self.__chk_mic_monitoring = wx.CheckBox(panel, label="Use this device as Playback source (Monitoring)")
        self.__chk_mic_monitoring.Bind(wx.EVT_CHECKBOX, lambda event: self.__controller.on_toggle_mic_monitoring(event))
        vbox.Add(self.__chk_mic_monitoring, 0, wx.ALL, 5)

        vbox.Add(wx.StaticText(panel, label="Mic-Monitoring volume"), 0, wx.ALL, 5)
        self.__sld_mic_monitoring = wx.Slider(panel,
                                              minValue=MIC_MONITORING_VOLUME_VR.get_min_value() // MIC_MONITORING_VOLUME_VR.get_step_size(),
                                              maxValue=MIC_MONITORING_VOLUME_VR.get_max_value() // MIC_MONITORING_VOLUME_VR.get_step_size(),
                                              value=50 // MIC_MONITORING_VOLUME_VR.get_step_size(),
                                              style=wx.SL_HORIZONTAL)
        self.__sld_mic_monitoring.Bind(wx.EVT_SCROLL_CHANGED,
                                       lambda event: self.__controller.on_change_mic_monitoring_volume(event))
        vbox.Add(self.__sld_mic_monitoring, 0, wx.ALL | wx.EXPAND, 5)

        # voice clarity
        self.__tgl_voice_clarity = wx.ToggleButton(panel, label="Voice clarity")
        self.__tgl_voice_clarity.Bind(wx.EVT_TOGGLEBUTTON,
                                      lambda event: self.__controller.on_toggle_voice_clarity(event))
        vbox.Add(self.__tgl_voice_clarity, 0, wx.ALL, 5)

        # voice clarity options group
        vbox_voice_clarity = wx.StaticBoxSizer(wx.VERTICAL, panel, "Voice clarity options")

        self.__chk_noise_reduction = wx.CheckBox(panel, label="Noise reduction")
        self.__chk_noise_reduction.Bind(wx.EVT_CHECKBOX,
                                        lambda event: self.__controller.on_toggle_voice_clarity_noise_reduction(event))
        vbox_voice_clarity.Add(self.__chk_noise_reduction, 0, wx.ALL | wx.EXPAND, 5)

        self.__sld_noise_reduction = wx.Slider(panel,
                                               minValue=VOICE_CLARITY_NOISE_REDUCTION_LEVEL_VR.get_min_value() // VOICE_CLARITY_NOISE_REDUCTION_LEVEL_VR.get_step_size(),
                                               maxValue=VOICE_CLARITY_NOISE_REDUCTION_LEVEL_VR.get_max_value() // VOICE_CLARITY_NOISE_REDUCTION_LEVEL_VR.get_step_size(),
                                               value=40 // VOICE_CLARITY_NOISE_REDUCTION_LEVEL_VR.get_step_size(),
                                               style=wx.SL_HORIZONTAL)
        self.__sld_noise_reduction.Bind(wx.EVT_SCROLL_CHANGED,
                                        lambda event: self.__controller.on_change_voice_clarity_noise_reduction_level(event))
        vbox_voice_clarity.Add(self.__sld_noise_reduction, 0, wx.ALL | wx.EXPAND, 5)

        self.__chk_echo_cancellation = wx.CheckBox(panel, label="Acoustic Echo Cancellation")
        self.__chk_echo_cancellation.Bind(wx.EVT_CHECKBOX,
                                          lambda event: self.__controller.on_toggle_voice_clarity_acoustic_echo_cancellation(event))
        vbox_voice_clarity.Add(self.__chk_echo_cancellation, 0, wx.ALL | wx.EXPAND, 5)

        self.__chk_smart_volume = wx.CheckBox(panel, label="Smart Volume")
        self.__chk_smart_volume.Bind(wx.EVT_CHECKBOX, lambda event: self.__controller.on_toggle_voice_clarity_smart_volume(event))
        vbox_voice_clarity.Add(self.__chk_smart_volume, 0, wx.ALL | wx.EXPAND, 5)

        self.__chk_mic_eq = wx.CheckBox(panel, label="Mic-EQ")
        self.__chk_mic_eq.Bind(wx.EVT_CHECKBOX, lambda event: self.__controller.on_toggle_voice_clarity_mic_equalizer(event))
        vbox_voice_clarity.Add(self.__chk_mic_eq, 0, wx.ALL | wx.EXPAND, 5)

        self.__cmb_mic_eq_preset = wx.ComboBox(panel, choices=self.MIC_EQ_PRESET_CHOICES, style=wx.CB_READONLY)
        self.__cmb_mic_eq_preset.SetSelection(0)
        self.__cmb_mic_eq_preset.Bind(wx.EVT_COMBOBOX,
                                      lambda event: self.__controller.on_change_voice_clarity_mic_equalizer_preset(event))
        vbox_voice_clarity.Add(self.__cmb_mic_eq_preset, 0, wx.ALL | wx.EXPAND, 5)

        vbox.Add(vbox_voice_clarity, 0, wx.ALL | wx.EXPAND, 5)

        panel.SetSizer(vbox)
        return panel

    # --- mic recording volume ---

    def get_mic_recording_volume_value(self) -> int:
        return self.__sld_mic_volume.GetValue() * MIC_RECORDING_VOLUME_VR.get_step_size()

    def set_mic_recording_volume_value(self, volume: int) -> None:
        self.__sld_mic_volume.SetValue(volume // MIC_RECORDING_VOLUME_VR.get_step_size())

    def set_mic_recording_volume_enabled(self, enabled: bool) -> None:
        self.__sld_mic_volume.Enable(enabled)

    # --- mic boost ---

    def get_mic_boost_value(self) -> int:
        return self.__sld_mic_boost.GetValue() * MIC_BOOST_DECIBEL_VR.get_step_size()

    def set_mic_boost_value(self, boost: int) -> None:
        self.__sld_mic_boost.SetValue(boost // MIC_BOOST_DECIBEL_VR.get_step_size())

    def set_mic_boost_enabled(self, enabled: bool) -> None:
        self.__sld_mic_boost.Enable(enabled)

    # --- mic monitoring ---

    def set_mic_monitoring_checkbox_value(self, enabled: bool) -> None:
        self.__chk_mic_monitoring.SetValue(enabled)

    def set_mic_monitoring_checkbox_enabled(self, enabled: bool) -> None:
        self.__chk_mic_monitoring.Enable(enabled)

    def get_mic_monitoring_volume_value(self) -> int:
        return self.__sld_mic_monitoring.GetValue() * MIC_MONITORING_VOLUME_VR.get_step_size()

    def set_mic_monitoring_volume_value(self, volume: int) -> None:
        self.__sld_mic_monitoring.SetValue(volume // MIC_MONITORING_VOLUME_VR.get_step_size())

    def set_mic_monitoring_volume_enabled(self, enabled: bool) -> None:
        self.__sld_mic_monitoring.Enable(enabled)

    # --- voice clarity ---

    def set_voice_clarity_toggle_value(self, active: bool) -> None:
        self.__tgl_voice_clarity.SetValue(active)

    def set_voice_clarity_toggle_enabled(self, enabled: bool) -> None:
        self.__tgl_voice_clarity.Enable(enabled)

    # --- voice clarity > noise reduction ---

    def set_voice_clarity_noise_reduction_checkbox_value(self, enabled: bool) -> None:
        self.__chk_noise_reduction.SetValue(enabled)

    def set_voice_clarity_noise_reduction_checkbox_enabled(self, enabled: bool) -> None:
        self.__chk_noise_reduction.Enable(enabled)

    def get_voice_clarity_noise_reduction_level_value(self) -> int:
        return self.__sld_noise_reduction.GetValue() * VOICE_CLARITY_NOISE_REDUCTION_LEVEL_VR.get_step_size()

    def set_voice_clarity_noise_reduction_slider_value(self, level: int) -> None:
        self.__sld_noise_reduction.SetValue(level // VOICE_CLARITY_NOISE_REDUCTION_LEVEL_VR.get_step_size())

    def set_voice_clarity_noise_reduction_slider_enabled(self, enabled: bool) -> None:
        self.__sld_noise_reduction.Enable(enabled)

    # --- voice clarity > acoustic echo cancellation ---

    def set_voice_clarity_acoustic_echo_cancellation_value(self, enabled: bool) -> None:
        self.__chk_echo_cancellation.SetValue(enabled)

    def set_voice_clarity_acoustic_echo_cancellation_enabled(self, enabled: bool) -> None:
        self.__chk_echo_cancellation.Enable(enabled)

    # --- voice clarity > smart volume ---

    def set_voice_clarity_smart_volume_value(self, enabled: bool) -> None:
        self.__chk_smart_volume.SetValue(enabled)

    def set_voice_clarity_smart_volume_enabled(self, enabled: bool) -> None:
        self.__chk_smart_volume.Enable(enabled)

    # --- voice clarity > mic equalizer ---

    def set_voice_clarity_mic_equalizer_checkbox_value(self, enabled: bool) -> None:
        self.__chk_mic_eq.SetValue(enabled)

    def set_voice_clarity_mic_equalizer_checkbox_enabled(self, enabled: bool) -> None:
        self.__chk_mic_eq.Enable(enabled)

    def set_voice_clarity_mic_equalizer_preset_value(self, preset: MicrophoneEqualizerPreset) -> None:
        self.__cmb_mic_eq_preset.SetSelection(_PRESET_TO_INDEX[preset])

    def set_voice_clarity_mic_equalizer_preset_enabled(self, enabled: bool) -> None:
        self.__cmb_mic_eq_preset.Enable(enabled)


class Controller:
    def __init__(self):
        self.__model: Model | None = None
        self.__view: View | None = None  # only for exceptional cases
        self.__g6_api: G6Api | None = None

    def bind(self, model: Model, view: View):
        self.__model = model
        self.__view = view

    def update_availability(self, g6_api: G6Api | None):
        self.__g6_api = g6_api

        mic_recording_volume_available = False
        mic_boost_available = False
        mic_monitoring_available = False
        voice_clarity_available = False
        voice_clarity_noise_reduction_available = False
        voice_clarity_acoustic_echo_cancellation_available = False
        voice_clarity_smart_volume_available = False
        voice_clarity_mic_equalizer_available = False

        if self.__g6_api is not None:
            mic_recording_volume_available = self.__g6_api.recording_mic_recording_volume_available()
            mic_boost_available = self.__g6_api.recording_mic_boost_available()
            mic_monitoring_available = self.__g6_api.recording_mic_monitoring_available()
            voice_clarity_available = self.__g6_api.recording_voice_clarity_enabled_available()
            voice_clarity_noise_reduction_available = self.__g6_api.recording_voice_clarity_noise_reduction_level_available()
            voice_clarity_acoustic_echo_cancellation_available = (
                self.__g6_api.recording_voice_clarity_acoustic_echo_cancellation_enabled_available()
            )
            voice_clarity_smart_volume_available = self.__g6_api.recording_voice_clarity_smart_volume_enabled_available()
            voice_clarity_mic_equalizer_available = self.__g6_api.recording_voice_clarity_mic_equalizer_enabled_available()

        self.__model.set_mic_recording_volume_available(mic_recording_volume_available)
        self.__model.set_mic_boost_available(mic_boost_available)
        self.__model.set_mic_monitoring_available(mic_monitoring_available)
        self.__model.set_voice_clarity_available(voice_clarity_available)
        self.__model.set_voice_clarity_noise_reduction_available(voice_clarity_noise_reduction_available)
        self.__model.set_voice_clarity_acoustic_echo_cancellation_available(
            voice_clarity_acoustic_echo_cancellation_available
        )
        self.__model.set_voice_clarity_smart_volume_available(voice_clarity_smart_volume_available)
        self.__model.set_voice_clarity_mic_equalizer_available(voice_clarity_mic_equalizer_available)

    def on_change_mic_recording_volume(self, event) -> None:
        # get the slider value
        volume = self.__view.get_mic_recording_volume_value()

        # update model
        self.__model.set_mic_recording_volume(volume)

        # send command to G6
        if self.__g6_api is not None:
            self.__g6_api.recording_mic_recording_volume(volume_percent=volume)

    def on_change_mic_boost(self, event) -> None:
        # get the slider value
        boost = self.__view.get_mic_boost_value()

        # update model
        self.__model.set_mic_boost(boost)

        # send command to G6
        if self.__g6_api is not None:
            self.__g6_api.recording_mic_boost(decibel=boost)

    def on_toggle_mic_monitoring(self, event) -> None:
        # get the checkbox state
        enabled = bool(event.GetEventObject().GetValue())

        # update model
        self.__model.set_mic_monitoring_enabled(enabled)

        # send command to G6
        if self.__g6_api is not None:
            self.__g6_api.recording_mic_monitoring_mute(mute=not enabled)

    def on_change_mic_monitoring_volume(self, event) -> None:
        # get the slider value
        volume = self.__view.get_mic_monitoring_volume_value()

        # update model
        self.__model.set_mic_monitoring_volume(volume)

        # send command to G6
        if self.__g6_api is not None:
            self.__g6_api.recording_mic_monitoring_volume(volume_percent=volume)

    def on_toggle_voice_clarity(self, event) -> None:
        # get the toggle button state
        active = bool(event.GetEventObject().GetValue())

        # update model
        self.__model.set_voice_clarity_active(active)

        # send command to G6
        if self.__g6_api is not None:
            self.__g6_api.recording_voice_clarity_enabled(enable=active)

    def on_toggle_voice_clarity_noise_reduction(self, event) -> None:
        # get the checkbox state
        enabled = bool(event.GetEventObject().GetValue())

        # update model
        self.__model.set_voice_clarity_noise_reduction_enabled(enabled)

        # send command to G6 (noise reduction level)
        if self.__g6_api is not None:
            level = self.__model.get_voice_clarity_noise_reduction_level() if enabled else 0
            self.__g6_api.recording_voice_clarity_noise_reduction_level(level_percent=level)

    def on_change_voice_clarity_noise_reduction_level(self, event) -> None:
        # get the slider value
        level = self.__view.get_voice_clarity_noise_reduction_level_value()

        # update model
        self.__model.set_voice_clarity_noise_reduction_level(level)

        # send command to G6
        if self.__g6_api is not None:
            self.__g6_api.recording_voice_clarity_noise_reduction_level(level_percent=level)

    def on_toggle_voice_clarity_acoustic_echo_cancellation(self, event) -> None:
        # get the checkbox state
        enabled = bool(event.GetEventObject().GetValue())

        # update model
        self.__model.set_voice_clarity_acoustic_echo_cancellation_enabled(enabled)

        # send command to G6
        if self.__g6_api is not None:
            self.__g6_api.recording_voice_clarity_acoustic_echo_cancellation_enabled(enable=enabled)

    def on_toggle_voice_clarity_smart_volume(self, event) -> None:
        # get the checkbox state
        enabled = bool(event.GetEventObject().GetValue())

        # update model
        self.__model.set_voice_clarity_smart_volume_enabled(enabled)

        # send command to G6
        if self.__g6_api is not None:
            self.__g6_api.recording_voice_clarity_smart_volume_enabled(enable=enabled)

    def on_toggle_voice_clarity_mic_equalizer(self, event) -> None:
        # get the checkbox state
        enabled = bool(event.GetEventObject().GetValue())

        # update model
        self.__model.set_voice_clarity_mic_equalizer_enabled(enabled)

        # send command to G6
        if self.__g6_api is not None:
            self.__g6_api.recording_voice_clarity_mic_equalizer_enabled(enable=enabled)

    def on_change_voice_clarity_mic_equalizer_preset(self, event) -> None:
        # get the selected preset
        selection = event.GetEventObject().GetSelection()
        preset = _INDEX_TO_PRESET[selection]

        # update model
        self.__model.set_voice_clarity_mic_equalizer_preset(preset)

        # send command to G6
        if self.__g6_api is not None:
            self.__g6_api.recording_voice_clarity_mic_equalizer_preset(preset=preset)


_PRESET_TO_INDEX: dict[MicrophoneEqualizerPreset, int] = {
    MicrophoneEqualizerPreset.PRESET_1: 0,
    MicrophoneEqualizerPreset.PRESET_2: 1,
    MicrophoneEqualizerPreset.PRESET_3: 2,
    MicrophoneEqualizerPreset.PRESET_4: 3,
    MicrophoneEqualizerPreset.PRESET_5: 4,
    MicrophoneEqualizerPreset.PRESET_6: 5,
    MicrophoneEqualizerPreset.PRESET_7: 6,
    MicrophoneEqualizerPreset.PRESET_8: 7,
    MicrophoneEqualizerPreset.PRESET_9: 8,
    MicrophoneEqualizerPreset.PRESET_10: 9,
    MicrophoneEqualizerPreset.PRESET_DM_1: 10,
}
_INDEX_TO_PRESET: dict[int, MicrophoneEqualizerPreset] = {v: k for k, v in _PRESET_TO_INDEX.items()}


class RecordingTab:
    def __init__(self):
        self.__model = Model()
        self.__view = View()
        self.__controller = Controller()

        self.__model.bind(self.__view)
        self.__view.bind(self.__controller)
        self.__controller.bind(self.__model, self.__view)

    def create(self, notebook: wx.Notebook) -> wx.Panel:
        return self.__view.create(notebook)

    def update_availability(self, g6_api: G6Api | None):
        self.__controller.update_availability(g6_api=g6_api)
