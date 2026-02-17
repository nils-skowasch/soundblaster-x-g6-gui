from collections.abc import Callable

import wx

from g6_cli import G6Api
from g6_cli.g6_spec import PlaybackFilter
from g6_gui.g6_models import AudioMode, AudioOutput


class Model:
    def __init__(self):
        self.__view: View | None = None

        # --- speakers ---
        self.__speakers_toggle_available = False  # HID
        self.__speakers_selected = True
        self.__speakers_audio_mode_available = False  # Audio
        self.__speakers_audio_mode: AudioMode = AudioMode.STEREO

        # --- headphones ---
        self.__headphones_toggle_available = False  # HID
        self.__headphones_selected = False
        self.__headphones_audio_mode_available = False  # Audio
        self.__headphones_audio_mode: AudioMode = AudioMode.STEREO

        # --- direct mode ---
        self.__direct_mode_available = False  # HID
        self.__direct_mode_active: bool = False

        # --- spdif out direct mode ---
        self.__spdif_out_direct_mode_available = False  # HID
        self.__spdif_out_direct_mode_active: bool = False

        # --- filter ---
        self.__filter_available = False  # HID
        self.__filter: PlaybackFilter = PlaybackFilter.FAST_ROLL_OFF_MINIMUM_PHASE

    def bind(self, view: "View"):
        self.__view = view

    # --- speakers ---

    def is_speakers_toggle_available(self) -> bool:
        return self.__speakers_toggle_available

    def set_speakers_toggle_available(self, available: bool) -> None:
        self.__speakers_toggle_available = available
        self.__handle_speakers_enabled()

    def is_speakers_selected(self) -> bool:
        return self.__speakers_selected

    def set_speakers_selected(self) -> None:
        self.__speakers_selected = True
        self.__headphones_selected = False
        self.__view.set_speakers_radio_value(True)
        self.__view.set_headphones_radio_value(False)
        self.__handle_speakers_enabled()
        self.__handle_headphones_enabled()

    def is_speakers_audio_mode_available(self) -> bool:
        return self.__speakers_audio_mode_available

    def set_speakers_audio_mode_available(self, available: bool) -> None:
        self.__speakers_audio_mode_available = available
        self.__handle_speakers_enabled()

    def get_speakers_audio_mode(self) -> AudioMode:
        return self.__speakers_audio_mode

    def set_speakers_audio_mode(self, mode: AudioMode) -> None:
        self.__speakers_audio_mode = mode
        self.__view.set_speakers_audio_mode(mode)

    def __handle_speakers_enabled(self) -> None:
        self.__view.set_speakers_radio_enabled(self.__speakers_toggle_available)
        self.__view.set_speakers_audio_mode_enabled(self.__speakers_audio_mode_available and self.__speakers_selected)

    # --- headphones ---

    def is_headphones_toggle_available(self) -> bool:
        return self.__headphones_toggle_available

    def set_headphones_toggle_available(self, available: bool) -> None:
        self.__headphones_toggle_available = available
        self.__handle_headphones_enabled()

    def is_headphones_selected(self) -> bool:
        return self.__headphones_selected

    def set_headphones_selected(self) -> None:
        self.__headphones_selected = True
        self.__speakers_selected = False
        self.__view.set_headphones_radio_value(True)
        self.__view.set_speakers_radio_value(False)
        self.__handle_headphones_enabled()
        self.__handle_speakers_enabled()

    def is_headphones_audio_mode_available(self) -> bool:
        return self.__headphones_audio_mode_available

    def set_headphones_audio_mode_available(self, available: bool) -> None:
        self.__headphones_audio_mode_available = available
        self.__handle_headphones_enabled()

    def get_headphones_audio_mode(self) -> AudioMode:
        return self.__headphones_audio_mode

    def set_headphones_audio_mode(self, mode: AudioMode) -> None:
        self.__headphones_audio_mode = mode
        self.__view.set_headphones_audio_mode(mode)

    def __handle_headphones_enabled(self) -> None:
        self.__view.set_headphones_radio_enabled(self.__headphones_toggle_available)
        self.__view.set_headphones_audio_mode_enabled(
            self.__headphones_audio_mode_available and self.__headphones_selected
        )

    # --- direct mode ---

    def is_direct_mode_available(self) -> bool:
        return self.__direct_mode_available

    def set_direct_mode_available(self, available: bool) -> None:
        self.__direct_mode_available = available
        self.__handle_direct_mode_enabled()

    def is_direct_mode_active(self) -> bool:
        return self.__direct_mode_active

    def set_direct_mode_active(self, active: bool) -> None:
        self.__direct_mode_active = active
        self.__view.set_direct_mode_value(active)

    def __handle_direct_mode_enabled(self) -> None:
        self.__view.set_direct_mode_enabled(self.__direct_mode_available)

    # --- spdif out direct mode ---

    def is_spdif_out_direct_mode_available(self) -> bool:
        return self.__spdif_out_direct_mode_available

    def set_spdif_out_direct_mode_available(self, available: bool) -> None:
        self.__spdif_out_direct_mode_available = available
        self.__handle_spdif_out_direct_mode_enabled()

    def is_spdif_out_direct_mode_active(self) -> bool:
        return self.__spdif_out_direct_mode_active

    def set_spdif_out_direct_mode_active(self, active: bool) -> None:
        self.__spdif_out_direct_mode_active = active
        self.__view.set_spdif_out_direct_mode_value(active)

    def __handle_spdif_out_direct_mode_enabled(self) -> None:
        self.__view.set_spdif_out_direct_mode_enabled(self.__spdif_out_direct_mode_available)

    # --- filter ---

    def is_filter_available(self) -> bool:
        return self.__filter_available

    def set_filter_available(self, available: bool) -> None:
        self.__filter_available = available
        self.__handle_filter_enabled()

    def get_filter(self) -> PlaybackFilter:
        return self.__filter

    def set_filter(self, _filter: PlaybackFilter) -> None:
        self.__filter = _filter
        self.__view.set_filter_value(_filter)

    def __handle_filter_enabled(self) -> None:
        self.__view.set_filter_enabled(self.__filter_available)


class View:
    AUDIO_MODE_CHOICES = ["Stereo", "Virtual Surround 5.1", "Virtual Surround 7.1"]
    FILTER_CHOICES = [
        "Fast Roll-Off - Minimum Phase",
        "Slow Roll-Off - Minimum Phase",
        "Fast Roll-Off - Linear Phase",
        "Slow Roll-Off - Linear Phase",
    ]

    class RadioComboComposite(wx.BoxSizer):
        def __init__(
                self,
                parent: wx.Panel,
                label: str,
                group_start: bool,
                choices: list[str],
        ):
            super().__init__(wx.HORIZONTAL)

            radio_style = wx.RB_GROUP if group_start else 0
            self.__rad = wx.RadioButton(parent, label=label, style=radio_style)
            self.__cmb = wx.ComboBox(parent, choices=choices, style=wx.CB_READONLY)
            self.__cmb.SetSelection(0)

            self.Add(self.__rad, proportion=1, flag=wx.ALL | wx.EXPAND, border=5)
            self.Add(self.__cmb, proportion=2, flag=wx.ALL | wx.EXPAND, border=5)

        def bind_radio(self, handler: Callable[[wx.CommandEvent], None]) -> None:
            self.__rad.Bind(wx.EVT_RADIOBUTTON, handler)

        def bind_combo(self, handler: Callable[[wx.CommandEvent], None]) -> None:
            self.__cmb.Bind(wx.EVT_COMBOBOX, handler)

        def set_radio_value(self, selected: bool) -> None:
            self.__rad.SetValue(selected)

        def set_radio_enabled(self, enabled: bool) -> None:
            self.__rad.Enable(enabled)

        def set_combo_enabled(self, enabled: bool) -> None:
            self.__cmb.Enable(enabled)

        def get_combo_selection(self) -> int:
            return self.__cmb.GetSelection()

        def set_combo_selection(self, selection: int) -> None:
            self.__cmb.SetSelection(selection)

    def __init__(self):
        self.__controller: Controller | None = None

        self.__cmp_speakers: View.RadioComboComposite | None = None
        self.__cmp_headphones: View.RadioComboComposite | None = None
        self.__tgl_directmode: wx.ToggleButton | None = None
        self.__tgl_spdif: wx.ToggleButton | None = None
        self.__cmb_filter: wx.ComboBox | None = None

    def bind(self, controller: "Controller"):
        self.__controller = controller

    def create(self, notebook: wx.Notebook) -> wx.Panel:
        panel = wx.Panel(notebook)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # speakers
        self.__cmp_speakers = View.RadioComboComposite(
            panel,
            "Speakers",
            group_start=True,
            choices=self.AUDIO_MODE_CHOICES,
        )
        self.__cmp_speakers.bind_radio(lambda event: self.__controller.on_select_audio_output(AudioOutput.SPEAKERS))
        self.__cmp_speakers.bind_combo(
            lambda event: self.__controller.on_change_audio_mode(AudioOutput.SPEAKERS, event))
        vbox.Add(self.__cmp_speakers, flag=wx.EXPAND)

        # headphones
        self.__cmp_headphones = View.RadioComboComposite(
            panel,
            "Headphones",
            group_start=False,
            choices=self.AUDIO_MODE_CHOICES,
        )
        self.__cmp_headphones.bind_radio(lambda event: self.__controller.on_select_audio_output(AudioOutput.HEADPHONES))
        self.__cmp_headphones.bind_combo(
            lambda event: self.__controller.on_change_audio_mode(AudioOutput.HEADPHONES, event))
        vbox.Add(self.__cmp_headphones, flag=wx.EXPAND)

        # direct modes
        self.__tgl_directmode = wx.ToggleButton(panel, label="Directmode")
        self.__tgl_directmode.Bind(wx.EVT_TOGGLEBUTTON, lambda event: self.__controller.on_toggle_direct_mode(event))
        vbox.Add(self.__tgl_directmode, flag=wx.ALL | wx.EXPAND, border=5)

        self.__tgl_spdif = wx.ToggleButton(panel, label="SPDIF-Out Directmode")
        self.__tgl_spdif.Bind(wx.EVT_TOGGLEBUTTON,
                              lambda event: self.__controller.on_toggle_spdif_out_direct_mode(event))
        vbox.Add(self.__tgl_spdif, flag=wx.ALL | wx.EXPAND, border=5)

        # filter
        self.__cmb_filter = wx.ComboBox(panel, choices=self.FILTER_CHOICES, style=wx.CB_READONLY)
        self.__cmb_filter.SetSelection(0)
        self.__cmb_filter.Bind(wx.EVT_COMBOBOX, lambda event: self.__controller.on_change_filter(event))
        vbox.Add(self.__cmb_filter, flag=wx.ALL | wx.EXPAND, border=5)

        panel.SetSizer(vbox)
        return panel

    # --- speakers ---

    def set_speakers_radio_value(self, selected: bool) -> None:
        self.__cmp_speakers.set_radio_value(selected)

    def set_speakers_radio_enabled(self, enabled: bool) -> None:
        self.__cmp_speakers.set_radio_enabled(enabled)

    def set_speakers_audio_mode(self, mode: AudioMode) -> None:
        self.__cmp_speakers.set_combo_selection(mode.value)

    def set_speakers_audio_mode_enabled(self, enabled: bool) -> None:
        self.__cmp_speakers.set_combo_enabled(enabled)

    # --- headphones ---

    def set_headphones_radio_value(self, selected: bool) -> None:
        self.__cmp_headphones.set_radio_value(selected)

    def set_headphones_radio_enabled(self, enabled: bool) -> None:
        self.__cmp_headphones.set_radio_enabled(enabled)

    def set_headphones_audio_mode(self, mode: AudioMode) -> None:
        self.__cmp_headphones.set_combo_selection(mode.value)

    def set_headphones_audio_mode_enabled(self, enabled: bool) -> None:
        self.__cmp_headphones.set_combo_enabled(enabled)

    # --- direct mode ---

    def set_direct_mode_value(self, enabled: bool) -> None:
        self.__tgl_directmode.SetValue(enabled)

    def set_direct_mode_enabled(self, enabled: bool) -> None:
        self.__tgl_directmode.Enable(enabled)

    # --- spdif out direct mode ---

    def set_spdif_out_direct_mode_value(self, enabled: bool) -> None:
        self.__tgl_spdif.SetValue(enabled)

    def set_spdif_out_direct_mode_enabled(self, enabled: bool) -> None:
        self.__tgl_spdif.Enable(enabled)

    # --- filter ---

    def set_filter_value(self, playback_filter: PlaybackFilter) -> None:
        self.__cmb_filter.SetSelection(_FILTER_TO_INDEX[playback_filter])

    def set_filter_enabled(self, enabled: bool) -> None:
        self.__cmb_filter.Enable(enabled)


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

        toggle_to_speakers_available = False
        speakers_audio_mode_available = False
        toggle_to_headphones_available = False
        headphones_audio_mode_available = False
        direct_mode_available = False
        spdif_out_direct_mode_available = False
        filter_available = False

        if self.__g6_api is not None:
            toggle_to_speakers_available = self.__g6_api.playback_toggle_to_speakers_available()
            speakers_audio_mode_available = self.__g6_api.playback_speakers_to_stereo_available()
            toggle_to_headphones_available = self.__g6_api.playback_toggle_to_headphones_available()
            headphones_audio_mode_available = self.__g6_api.playback_headphones_to_stereo_available()
            direct_mode_available = self.__g6_api.playback_enable_direct_mode_available()
            spdif_out_direct_mode_available = self.__g6_api.playback_enable_spdif_out_direct_mode_available()
            filter_available = self.__g6_api.playback_filter_available()

        self.__model.set_speakers_toggle_available(toggle_to_speakers_available)
        self.__model.set_speakers_audio_mode_available(speakers_audio_mode_available)
        self.__model.set_headphones_toggle_available(toggle_to_headphones_available)
        self.__model.set_headphones_audio_mode_available(headphones_audio_mode_available)
        self.__model.set_direct_mode_available(direct_mode_available)
        self.__model.set_spdif_out_direct_mode_available(spdif_out_direct_mode_available)
        self.__model.set_filter_available(filter_available)

    def on_select_audio_output(self, audio_output: AudioOutput) -> None:
        match audio_output:
            case AudioOutput.SPEAKERS:
                self.__model.set_speakers_selected()
                if self.__g6_api is not None:
                    self.__g6_api.playback_toggle_to_speakers()
            case AudioOutput.HEADPHONES:
                self.__model.set_headphones_selected()
                if self.__g6_api is not None:
                    self.__g6_api.playback_toggle_to_headphones()
            case _:
                raise ValueError(f"Unexpected audio_output: {audio_output}")

    def on_change_audio_mode(self, audio_output: AudioOutput, event) -> None:
        # get the selected audio mode
        selection = event.GetEventObject().GetSelection()
        audio_mode = AudioMode(selection)

        # update model
        match audio_output:
            case AudioOutput.SPEAKERS:
                self.__model.set_speakers_audio_mode(audio_mode)
            case AudioOutput.HEADPHONES:
                self.__model.set_headphones_audio_mode(audio_mode)
            case _:
                raise ValueError(f"Unexpected audio_output: {audio_output}")

        # send command to G6
        if self.__g6_api is not None:
            match audio_output:
                case AudioOutput.SPEAKERS:
                    match audio_mode:
                        case AudioMode.STEREO:
                            self.__g6_api.playback_speakers_to_stereo()
                        case AudioMode.VIRTUAL_SURROUND_5_1:
                            self.__g6_api.playback_speakers_to_5_1()
                        case AudioMode.VIRTUAL_SURROUND_7_1:
                            self.__g6_api.playback_speakers_to_7_1()
                        case _:
                            raise ValueError(f"Unexpected audio_mode: {audio_mode}")
                case AudioOutput.HEADPHONES:
                    match audio_mode:
                        case AudioMode.STEREO:
                            self.__g6_api.playback_headphones_to_stereo()
                        case AudioMode.VIRTUAL_SURROUND_5_1:
                            self.__g6_api.playback_headphones_to_5_1()
                        case AudioMode.VIRTUAL_SURROUND_7_1:
                            self.__g6_api.playback_headphones_to_7_1()
                        case _:
                            raise ValueError(f"Unexpected audio_mode: {audio_mode}")
                case _:
                    raise ValueError(f"Unexpected audio_output: {audio_output}")

    def on_toggle_direct_mode(self, event) -> None:
        # get active state
        active = bool(event.GetEventObject().GetValue())

        # update model
        self.__model.set_direct_mode_active(active)

        # send command to G6
        if self.__g6_api is not None:
            self.__g6_api.playback_enable_direct_mode(active)

    def on_toggle_spdif_out_direct_mode(self, event) -> None:
        # get active state
        active = bool(event.GetEventObject().GetValue())

        # update model
        self.__model.set_spdif_out_direct_mode_active(active)

        # send command to G6
        if self.__g6_api is not None:
            self.__g6_api.playback_enable_spdif_out_direct_mode(active)

    def on_change_filter(self, event) -> None:
        # get selected filter
        selection = event.GetEventObject().GetSelection()
        playback_filter = _INDEX_TO_FILTER[selection]

        # update model
        self.__model.set_filter(playback_filter)

        # send command to G6
        if self.__g6_api is not None:
            self.__g6_api.playback_filter(playback_filter)


_FILTER_TO_INDEX: dict[PlaybackFilter, int] = {
    PlaybackFilter.FAST_ROLL_OFF_MINIMUM_PHASE: 0,
    PlaybackFilter.SLOW_ROLL_OFF_MINIMUM_PHASE: 1,
    PlaybackFilter.FAST_ROLL_OFF_LINEAR_PHASE: 2,
    PlaybackFilter.SLOW_ROLL_OFF_LINEAR_PHASE: 3,
}
_INDEX_TO_FILTER: dict[int, PlaybackFilter] = {v: k for k, v in _FILTER_TO_INDEX.items()}


class PlaybackTab:
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
