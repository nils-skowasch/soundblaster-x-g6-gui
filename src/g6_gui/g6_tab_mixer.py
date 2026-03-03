from collections.abc import Callable

import wx

from g6_cli import G6Api
from g6_cli.g6_spec import BOTH_CHANNELS, Channel
from g6_cli.g6_spec.mixer import MIXER_VR


class Model:
    def __init__(self):
        self.__view: View | None = None

        # --- playback (speakers) ---
        self.__playback_available = False
        self.__playback_active = True
        self.__playback_volume = 50
        self.__playback_volume_l = 50
        self.__playback_volume_r = 50

        # --- monitoring ---
        self.__monitoring_line_in_available = False
        self.__monitoring_line_in_active = True
        self.__monitoring_line_in_volume = 50
        self.__monitoring_line_in_volume_l = 50
        self.__monitoring_line_in_volume_r = 50

        self.__monitoring_external_mic_available = False
        self.__monitoring_external_mic_active = True
        self.__monitoring_external_mic_volume = 50
        self.__monitoring_external_mic_volume_l = 50
        self.__monitoring_external_mic_volume_r = 50

        self.__monitoring_spdif_in_available = False
        self.__monitoring_spdif_in_active = True
        self.__monitoring_spdif_in_volume = 50
        self.__monitoring_spdif_in_volume_l = 50
        self.__monitoring_spdif_in_volume_r = 50

        # --- recording ---
        self.__recording_external_mic_available = False
        self.__recording_external_mic_active = True
        self.__recording_external_mic_volume = 50
        self.__recording_external_mic_volume_l = 50
        self.__recording_external_mic_volume_r = 50

        self.__recording_line_in_available = False
        self.__recording_line_in_active = True
        self.__recording_line_in_volume = 50
        self.__recording_line_in_volume_l = 50
        self.__recording_line_in_volume_r = 50

        self.__recording_spdif_in_available = False
        self.__recording_spdif_in_active = True
        self.__recording_spdif_in_volume = 50
        self.__recording_spdif_in_volume_l = 50
        self.__recording_spdif_in_volume_r = 50

        self.__recording_what_u_hear_available = False
        self.__recording_what_u_hear_active = True
        self.__recording_what_u_hear_volume = 50
        self.__recording_what_u_hear_volume_l = 50
        self.__recording_what_u_hear_volume_r = 50

    def bind(self, view: "View"):
        self.__view = view

    # --- helpers ---

    @staticmethod
    def __handle_enabled(
            available: bool,
            active: bool,
            set_toggle_enabled: Callable[[bool], None],
            set_toggle_value: Callable[[bool], None],
            set_slider_enabled: Callable[[bool], None],
            set_gears_enabled: Callable[[bool], None],
    ) -> None:
        active_and_available = available and active
        set_toggle_enabled(available)
        set_toggle_value(active)
        set_slider_enabled(active_and_available)
        set_gears_enabled(active_and_available)

    # --- playback (speakers) ---

    def set_playback_available(self, available: bool) -> None:
        self.__playback_available = available
        self.__handle_playback_enabled()

    def is_playback_active(self) -> bool:
        return self.__playback_active

    def set_playback_active(self, active: bool) -> None:
        self.__playback_active = active
        self.__handle_playback_enabled()

    def get_playback_volume(self) -> int:
        return self.__playback_volume

    def set_playback_volume(self, value: int) -> None:
        self.__playback_volume = value
        self.__playback_volume_l = value
        self.__playback_volume_r = value
        self.__view.set_playback_volume_value(value)

    def get_playback_volume_l(self) -> int:
        return self.__playback_volume_l

    def set_playback_volume_l(self, value: int) -> None:
        self.__playback_volume_l = value

    def get_playback_volume_r(self) -> int:
        return self.__playback_volume_r

    def set_playback_volume_r(self, value: int) -> None:
        self.__playback_volume_r = value

    def __handle_playback_enabled(self) -> None:
        self.__handle_enabled(
            available=self.__playback_available,
            active=self.__playback_active,
            set_toggle_enabled=self.__view.set_playback_toggle_enabled,
            set_toggle_value=self.__view.set_playback_toggle_value,
            set_slider_enabled=self.__view.set_playback_volume_enabled,
            set_gears_enabled=self.__view.set_playback_gears_enabled,
        )

    # --- monitoring: line-in ---

    def set_monitoring_line_in_available(self, available: bool) -> None:
        self.__monitoring_line_in_available = available
        self.__handle_monitoring_line_in_enabled()

    def is_monitoring_line_in_active(self) -> bool:
        return self.__monitoring_line_in_active

    def set_monitoring_line_in_active(self, active: bool) -> None:
        self.__monitoring_line_in_active = active
        self.__handle_monitoring_line_in_enabled()

    def get_monitoring_line_in_volume(self) -> int:
        return self.__monitoring_line_in_volume

    def set_monitoring_line_in_volume(self, value: int) -> None:
        self.__monitoring_line_in_volume = value
        self.__monitoring_line_in_volume_l = value
        self.__monitoring_line_in_volume_r = value
        self.__view.set_monitoring_line_in_volume_value(value)

    def get_monitoring_line_in_volume_l(self) -> int:
        return self.__monitoring_line_in_volume_l

    def set_monitoring_line_in_volume_l(self, value: int) -> None:
        self.__monitoring_line_in_volume_l = value

    def get_monitoring_line_in_volume_r(self) -> int:
        return self.__monitoring_line_in_volume_r

    def set_monitoring_line_in_volume_r(self, value: int) -> None:
        self.__monitoring_line_in_volume_r = value

    def __handle_monitoring_line_in_enabled(self) -> None:
        self.__handle_enabled(
            available=self.__monitoring_line_in_available,
            active=self.__monitoring_line_in_active,
            set_toggle_enabled=self.__view.set_monitoring_line_in_toggle_enabled,
            set_toggle_value=self.__view.set_monitoring_line_in_toggle_value,
            set_slider_enabled=self.__view.set_monitoring_line_in_volume_enabled,
            set_gears_enabled=self.__view.set_monitoring_line_in_gears_enabled,
        )

    # --- monitoring: external mic ---

    def set_monitoring_external_mic_available(self, available: bool) -> None:
        self.__monitoring_external_mic_available = available
        self.__handle_monitoring_external_mic_enabled()

    def is_monitoring_external_mic_active(self) -> bool:
        return self.__monitoring_external_mic_active

    def set_monitoring_external_mic_active(self, active: bool) -> None:
        self.__monitoring_external_mic_active = active
        self.__handle_monitoring_external_mic_enabled()

    def get_monitoring_external_mic_volume(self) -> int:
        return self.__monitoring_external_mic_volume

    def set_monitoring_external_mic_volume(self, value: int) -> None:
        self.__monitoring_external_mic_volume = value
        self.__monitoring_external_mic_volume_l = value
        self.__monitoring_external_mic_volume_r = value
        self.__view.set_monitoring_external_mic_volume_value(value)

    def get_monitoring_external_mic_volume_l(self) -> int:
        return self.__monitoring_external_mic_volume_l

    def set_monitoring_external_mic_volume_l(self, value: int) -> None:
        self.__monitoring_external_mic_volume_l = value

    def get_monitoring_external_mic_volume_r(self) -> int:
        return self.__monitoring_external_mic_volume_r

    def set_monitoring_external_mic_volume_r(self, value: int) -> None:
        self.__monitoring_external_mic_volume_r = value

    def __handle_monitoring_external_mic_enabled(self) -> None:
        self.__handle_enabled(
            available=self.__monitoring_external_mic_available,
            active=self.__monitoring_external_mic_active,
            set_toggle_enabled=self.__view.set_monitoring_external_mic_toggle_enabled,
            set_toggle_value=self.__view.set_monitoring_external_mic_toggle_value,
            set_slider_enabled=self.__view.set_monitoring_external_mic_volume_enabled,
            set_gears_enabled=self.__view.set_monitoring_external_mic_gears_enabled,
        )

    # --- monitoring: spdif-in ---

    def set_monitoring_spdif_in_available(self, available: bool) -> None:
        self.__monitoring_spdif_in_available = available
        self.__handle_monitoring_spdif_in_enabled()

    def is_monitoring_spdif_in_active(self) -> bool:
        return self.__monitoring_spdif_in_active

    def set_monitoring_spdif_in_active(self, active: bool) -> None:
        self.__monitoring_spdif_in_active = active
        self.__handle_monitoring_spdif_in_enabled()

    def get_monitoring_spdif_in_volume(self) -> int:
        return self.__monitoring_spdif_in_volume

    def set_monitoring_spdif_in_volume(self, value: int) -> None:
        self.__monitoring_spdif_in_volume = value
        self.__monitoring_spdif_in_volume_l = value
        self.__monitoring_spdif_in_volume_r = value
        self.__view.set_monitoring_spdif_in_volume_value(value)

    def get_monitoring_spdif_in_volume_l(self) -> int:
        return self.__monitoring_spdif_in_volume_l

    def set_monitoring_spdif_in_volume_l(self, value: int) -> None:
        self.__monitoring_spdif_in_volume_l = value

    def get_monitoring_spdif_in_volume_r(self) -> int:
        return self.__monitoring_spdif_in_volume_r

    def set_monitoring_spdif_in_volume_r(self, value: int) -> None:
        self.__monitoring_spdif_in_volume_r = value

    def __handle_monitoring_spdif_in_enabled(self) -> None:
        self.__handle_enabled(
            available=self.__monitoring_spdif_in_available,
            active=self.__monitoring_spdif_in_active,
            set_toggle_enabled=self.__view.set_monitoring_spdif_in_toggle_enabled,
            set_toggle_value=self.__view.set_monitoring_spdif_in_toggle_value,
            set_slider_enabled=self.__view.set_monitoring_spdif_in_volume_enabled,
            set_gears_enabled=self.__view.set_monitoring_spdif_in_gears_enabled,
        )

    # --- recording: external mic ---

    def set_recording_external_mic_available(self, available: bool) -> None:
        self.__recording_external_mic_available = available
        self.__handle_recording_external_mic_enabled()

    def is_recording_external_mic_active(self) -> bool:
        return self.__recording_external_mic_active

    def set_recording_external_mic_active(self, active: bool) -> None:
        self.__recording_external_mic_active = active
        self.__handle_recording_external_mic_enabled()

    def get_recording_external_mic_volume(self) -> int:
        return self.__recording_external_mic_volume

    def set_recording_external_mic_volume(self, value: int) -> None:
        self.__recording_external_mic_volume = value
        self.__recording_external_mic_volume_l = value
        self.__recording_external_mic_volume_r = value
        self.__view.set_recording_external_mic_volume_value(value)

    def get_recording_external_mic_volume_l(self) -> int:
        return self.__recording_external_mic_volume_l

    def set_recording_external_mic_volume_l(self, value: int) -> None:
        self.__recording_external_mic_volume_l = value

    def get_recording_external_mic_volume_r(self) -> int:
        return self.__recording_external_mic_volume_r

    def set_recording_external_mic_volume_r(self, value: int) -> None:
        self.__recording_external_mic_volume_r = value

    def __handle_recording_external_mic_enabled(self) -> None:
        self.__handle_enabled(
            available=self.__recording_external_mic_available,
            active=self.__recording_external_mic_active,
            set_toggle_enabled=self.__view.set_recording_external_mic_toggle_enabled,
            set_toggle_value=self.__view.set_recording_external_mic_toggle_value,
            set_slider_enabled=self.__view.set_recording_external_mic_volume_enabled,
            set_gears_enabled=self.__view.set_recording_external_mic_gears_enabled,
        )

    # --- recording: line-in ---

    def set_recording_line_in_available(self, available: bool) -> None:
        self.__recording_line_in_available = available
        self.__handle_recording_line_in_enabled()

    def is_recording_line_in_active(self) -> bool:
        return self.__recording_line_in_active

    def set_recording_line_in_active(self, active: bool) -> None:
        self.__recording_line_in_active = active
        self.__handle_recording_line_in_enabled()

    def get_recording_line_in_volume(self) -> int:
        return self.__recording_line_in_volume

    def set_recording_line_in_volume(self, value: int) -> None:
        self.__recording_line_in_volume = value
        self.__recording_line_in_volume_l = value
        self.__recording_line_in_volume_r = value
        self.__view.set_recording_line_in_volume_value(value)

    def get_recording_line_in_volume_l(self) -> int:
        return self.__recording_line_in_volume_l

    def set_recording_line_in_volume_l(self, value: int) -> None:
        self.__recording_line_in_volume_l = value

    def get_recording_line_in_volume_r(self) -> int:
        return self.__recording_line_in_volume_r

    def set_recording_line_in_volume_r(self, value: int) -> None:
        self.__recording_line_in_volume_r = value

    def __handle_recording_line_in_enabled(self) -> None:
        self.__handle_enabled(
            available=self.__recording_line_in_available,
            active=self.__recording_line_in_active,
            set_toggle_enabled=self.__view.set_recording_line_in_toggle_enabled,
            set_toggle_value=self.__view.set_recording_line_in_toggle_value,
            set_slider_enabled=self.__view.set_recording_line_in_volume_enabled,
            set_gears_enabled=self.__view.set_recording_line_in_gears_enabled,
        )

    # --- recording: spdif-in ---

    def set_recording_spdif_in_available(self, available: bool) -> None:
        self.__recording_spdif_in_available = available
        self.__handle_recording_spdif_in_enabled()

    def is_recording_spdif_in_active(self) -> bool:
        return self.__recording_spdif_in_active

    def set_recording_spdif_in_active(self, active: bool) -> None:
        self.__recording_spdif_in_active = active
        self.__handle_recording_spdif_in_enabled()

    def get_recording_spdif_in_volume(self) -> int:
        return self.__recording_spdif_in_volume

    def set_recording_spdif_in_volume(self, value: int) -> None:
        self.__recording_spdif_in_volume = value
        self.__recording_spdif_in_volume_l = value
        self.__recording_spdif_in_volume_r = value
        self.__view.set_recording_spdif_in_volume_value(value)

    def get_recording_spdif_in_volume_l(self) -> int:
        return self.__recording_spdif_in_volume_l

    def set_recording_spdif_in_volume_l(self, value: int) -> None:
        self.__recording_spdif_in_volume_l = value

    def get_recording_spdif_in_volume_r(self) -> int:
        return self.__recording_spdif_in_volume_r

    def set_recording_spdif_in_volume_r(self, value: int) -> None:
        self.__recording_spdif_in_volume_r = value

    def __handle_recording_spdif_in_enabled(self) -> None:
        self.__handle_enabled(
            available=self.__recording_spdif_in_available,
            active=self.__recording_spdif_in_active,
            set_toggle_enabled=self.__view.set_recording_spdif_in_toggle_enabled,
            set_toggle_value=self.__view.set_recording_spdif_in_toggle_value,
            set_slider_enabled=self.__view.set_recording_spdif_in_volume_enabled,
            set_gears_enabled=self.__view.set_recording_spdif_in_gears_enabled,
        )

    # --- recording: what u hear ---

    def set_recording_what_u_hear_available(self, available: bool) -> None:
        self.__recording_what_u_hear_available = available
        self.__handle_recording_what_u_hear_enabled()

    def is_recording_what_u_hear_active(self) -> bool:
        return self.__recording_what_u_hear_active

    def set_recording_what_u_hear_active(self, active: bool) -> None:
        self.__recording_what_u_hear_active = active
        self.__handle_recording_what_u_hear_enabled()

    def get_recording_what_u_hear_volume(self) -> int:
        return self.__recording_what_u_hear_volume

    def set_recording_what_u_hear_volume(self, value: int) -> None:
        self.__recording_what_u_hear_volume = value
        self.__recording_what_u_hear_volume_l = value
        self.__recording_what_u_hear_volume_r = value
        self.__view.set_recording_what_u_hear_volume_value(value)

    def get_recording_what_u_hear_volume_l(self) -> int:
        return self.__recording_what_u_hear_volume_l

    def set_recording_what_u_hear_volume_l(self, value: int) -> None:
        self.__recording_what_u_hear_volume_l = value

    def get_recording_what_u_hear_volume_r(self) -> int:
        return self.__recording_what_u_hear_volume_r

    def set_recording_what_u_hear_volume_r(self, value: int) -> None:
        self.__recording_what_u_hear_volume_r = value

    def __handle_recording_what_u_hear_enabled(self) -> None:
        self.__handle_enabled(
            available=self.__recording_what_u_hear_available,
            active=self.__recording_what_u_hear_active,
            set_toggle_enabled=self.__view.set_recording_what_u_hear_toggle_enabled,
            set_toggle_value=self.__view.set_recording_what_u_hear_toggle_value,
            set_slider_enabled=self.__view.set_recording_what_u_hear_volume_enabled,
            set_gears_enabled=self.__view.set_recording_what_u_hear_gears_enabled,
        )


class View:
    class SliderGearsComposite(wx.BoxSizer):
        def __init__(self, parent: wx.Panel, label: str):
            super().__init__(wx.HORIZONTAL)

            self.__label = wx.StaticText(parent, label=label)
            self.__chk_active = wx.CheckBox(parent, label="Active")
            self.__chk_active.SetValue(True)

            self.__sld = wx.Slider(parent,
                                   minValue=MIXER_VR.get_min_value() // MIXER_VR.get_step_size(),
                                   maxValue=MIXER_VR.get_max_value() // MIXER_VR.get_step_size(),
                                   value=50 // MIXER_VR.get_step_size(),
                                   style=wx.SL_HORIZONTAL)

            self.__btn_gears = wx.Button(parent, label="⚙", size=wx.Size(40, -1))

            self.Add(self.__label, proportion=1, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=5)
            self.Add(self.__chk_active, proportion=1, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=5)
            self.Add(self.__sld, proportion=2, flag=wx.ALL | wx.EXPAND, border=5)
            self.Add(self.__btn_gears, proportion=0, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=5)

        def bind_toggle(self, handler: Callable[[wx.CommandEvent], None]) -> None:
            self.__chk_active.Bind(wx.EVT_CHECKBOX, handler)

        def bind_slider(self, handler: Callable[[wx.CommandEvent], None]) -> None:
            self.__sld.Bind(wx.EVT_SCROLL_CHANGED, handler)

        def bind_gears(self, handler: Callable[[wx.CommandEvent], None]) -> None:
            self.__btn_gears.Bind(wx.EVT_BUTTON, handler)

        def set_toggle_value(self, active: bool) -> None:
            self.__chk_active.SetValue(active)
            self.__chk_active.SetLabel("Active" if active else "Muted")

        def set_toggle_enabled(self, enabled: bool) -> None:
            self.__chk_active.Enable(enabled)

        def get_slider_value(self) -> int:
            return int(self.__sld.GetValue()) * MIXER_VR.get_step_size()

        def set_slider_value(self, value: int) -> None:
            self.__sld.SetValue(int(value) // MIXER_VR.get_step_size())

        def set_slider_enabled(self, enabled: bool) -> None:
            self.__sld.Enable(enabled)

        def set_gears_enabled(self, enabled: bool) -> None:
            self.__btn_gears.Enable(enabled)

    def __init__(self, frame: wx.Frame):
        self.__controller: Controller | None = None
        self.__frame = frame

        # --- composites ---
        self.__cmp_playback: View.SliderGearsComposite | None = None

        self.__cmp_monitoring_line_in: View.SliderGearsComposite | None = None
        self.__cmp_monitoring_external_mic: View.SliderGearsComposite | None = None
        self.__cmp_monitoring_spdif_in: View.SliderGearsComposite | None = None

        self.__cmp_recording_external_mic: View.SliderGearsComposite | None = None
        self.__cmp_recording_line_in: View.SliderGearsComposite | None = None
        self.__cmp_recording_spdif_in: View.SliderGearsComposite | None = None
        self.__cmp_recording_what_u_hear: View.SliderGearsComposite | None = None

    def bind(self, controller: "Controller"):
        self.__controller = controller

    def create(self, notebook: wx.Notebook) -> wx.Panel:
        panel = wx.Panel(notebook)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # --- playback ---
        grp_playback = wx.StaticBox(panel, label="Playback")
        grp_playback_sizer = wx.StaticBoxSizer(grp_playback, wx.VERTICAL)

        self.__cmp_playback = View.SliderGearsComposite(panel, "Speakers")
        self.__cmp_playback.bind_toggle(lambda event: self.__controller.on_toggle_playback(event))
        self.__cmp_playback.bind_slider(lambda event: self.__controller.on_slide_playback(event))
        self.__cmp_playback.bind_gears(lambda event: self.__controller.on_gears_playback())
        grp_playback_sizer.Add(self.__cmp_playback, flag=wx.ALL | wx.EXPAND, border=5)

        vbox.Add(grp_playback_sizer, flag=wx.ALL | wx.EXPAND, border=5)

        # --- monitoring ---
        grp_monitoring = wx.StaticBox(panel, label="Monitoring")
        grp_monitoring_sizer = wx.StaticBoxSizer(grp_monitoring, wx.VERTICAL)

        self.__cmp_monitoring_line_in = View.SliderGearsComposite(panel, "Line-In")
        self.__cmp_monitoring_line_in.bind_toggle(lambda event: self.__controller.on_toggle_monitoring_line_in(event))
        self.__cmp_monitoring_line_in.bind_slider(lambda event: self.__controller.on_slide_monitoring_line_in(event))
        self.__cmp_monitoring_line_in.bind_gears(lambda event: self.__controller.on_gears_monitoring_line_in())
        grp_monitoring_sizer.Add(self.__cmp_monitoring_line_in, flag=wx.ALL | wx.EXPAND, border=5)

        self.__cmp_monitoring_external_mic = View.SliderGearsComposite(panel, "External Microphone")
        self.__cmp_monitoring_external_mic.bind_toggle(
            lambda event: self.__controller.on_toggle_monitoring_external_mic(event)
        )
        self.__cmp_monitoring_external_mic.bind_slider(
            lambda event: self.__controller.on_slide_monitoring_external_mic(event)
        )
        self.__cmp_monitoring_external_mic.bind_gears(
            lambda event: self.__controller.on_gears_monitoring_external_mic())
        grp_monitoring_sizer.Add(self.__cmp_monitoring_external_mic, flag=wx.ALL | wx.EXPAND, border=5)

        self.__cmp_monitoring_spdif_in = View.SliderGearsComposite(panel, "SPDIF-In")
        self.__cmp_monitoring_spdif_in.bind_toggle(lambda event: self.__controller.on_toggle_monitoring_spdif_in(event))
        self.__cmp_monitoring_spdif_in.bind_slider(lambda event: self.__controller.on_slide_monitoring_spdif_in(event))
        self.__cmp_monitoring_spdif_in.bind_gears(lambda event: self.__controller.on_gears_monitoring_spdif_in())
        grp_monitoring_sizer.Add(self.__cmp_monitoring_spdif_in, flag=wx.ALL | wx.EXPAND, border=5)

        vbox.Add(grp_monitoring_sizer, flag=wx.ALL | wx.EXPAND, border=5)

        # --- recording ---
        grp_recording = wx.StaticBox(panel, label="Recording")
        grp_recording_sizer = wx.StaticBoxSizer(grp_recording, wx.VERTICAL)

        self.__cmp_recording_external_mic = View.SliderGearsComposite(panel, "External Mic")
        self.__cmp_recording_external_mic.bind_toggle(
            lambda event: self.__controller.on_toggle_recording_external_mic(event)
        )
        self.__cmp_recording_external_mic.bind_slider(
            lambda event: self.__controller.on_slide_recording_external_mic(event)
        )
        self.__cmp_recording_external_mic.bind_gears(lambda event: self.__controller.on_gears_recording_external_mic())
        grp_recording_sizer.Add(self.__cmp_recording_external_mic, flag=wx.ALL | wx.EXPAND, border=5)

        self.__cmp_recording_line_in = View.SliderGearsComposite(panel, "Line In")
        self.__cmp_recording_line_in.bind_toggle(lambda event: self.__controller.on_toggle_recording_line_in(event))
        self.__cmp_recording_line_in.bind_slider(lambda event: self.__controller.on_slide_recording_line_in(event))
        self.__cmp_recording_line_in.bind_gears(lambda event: self.__controller.on_gears_recording_line_in())
        grp_recording_sizer.Add(self.__cmp_recording_line_in, flag=wx.ALL | wx.EXPAND, border=5)

        self.__cmp_recording_spdif_in = View.SliderGearsComposite(panel, "SPDIF-In")
        self.__cmp_recording_spdif_in.bind_toggle(lambda event: self.__controller.on_toggle_recording_spdif_in(event))
        self.__cmp_recording_spdif_in.bind_slider(lambda event: self.__controller.on_slide_recording_spdif_in(event))
        self.__cmp_recording_spdif_in.bind_gears(lambda event: self.__controller.on_gears_recording_spdif_in())
        grp_recording_sizer.Add(self.__cmp_recording_spdif_in, flag=wx.ALL | wx.EXPAND, border=5)

        self.__cmp_recording_what_u_hear = View.SliderGearsComposite(panel, "What U Hear")
        self.__cmp_recording_what_u_hear.bind_toggle(
            lambda event: self.__controller.on_toggle_recording_what_u_hear(event)
        )
        self.__cmp_recording_what_u_hear.bind_slider(
            lambda event: self.__controller.on_slide_recording_what_u_hear(event)
        )
        self.__cmp_recording_what_u_hear.bind_gears(lambda event: self.__controller.on_gears_recording_what_u_hear())
        grp_recording_sizer.Add(self.__cmp_recording_what_u_hear, flag=wx.ALL | wx.EXPAND, border=5)

        vbox.Add(grp_recording_sizer, flag=wx.ALL | wx.EXPAND, border=5)

        panel.SetSizer(vbox)
        return panel

    # --- playback ---

    def set_playback_toggle_value(self, active: bool) -> None:
        self.__cmp_playback.set_toggle_value(active)

    def set_playback_toggle_enabled(self, enabled: bool) -> None:
        self.__cmp_playback.set_toggle_enabled(enabled)

    def get_playback_volume_value(self) -> int:
        return self.__cmp_playback.get_slider_value()

    def set_playback_volume_value(self, value: int) -> None:
        self.__cmp_playback.set_slider_value(value)

    def set_playback_volume_enabled(self, enabled: bool) -> None:
        self.__cmp_playback.set_slider_enabled(enabled)

    def set_playback_gears_enabled(self, enabled: bool) -> None:
        self.__cmp_playback.set_gears_enabled(enabled)

    # --- monitoring: line-in ---

    def set_monitoring_line_in_toggle_value(self, active: bool) -> None:
        self.__cmp_monitoring_line_in.set_toggle_value(active)

    def set_monitoring_line_in_toggle_enabled(self, enabled: bool) -> None:
        self.__cmp_monitoring_line_in.set_toggle_enabled(enabled)

    def get_monitoring_line_in_volume_value(self) -> int:
        return self.__cmp_monitoring_line_in.get_slider_value()

    def set_monitoring_line_in_volume_value(self, value: int) -> None:
        self.__cmp_monitoring_line_in.set_slider_value(value)

    def set_monitoring_line_in_volume_enabled(self, enabled: bool) -> None:
        self.__cmp_monitoring_line_in.set_slider_enabled(enabled)

    def set_monitoring_line_in_gears_enabled(self, enabled: bool) -> None:
        self.__cmp_monitoring_line_in.set_gears_enabled(enabled)

    # --- monitoring: external mic ---

    def set_monitoring_external_mic_toggle_value(self, active: bool) -> None:
        self.__cmp_monitoring_external_mic.set_toggle_value(active)

    def set_monitoring_external_mic_toggle_enabled(self, enabled: bool) -> None:
        self.__cmp_monitoring_external_mic.set_toggle_enabled(enabled)

    def get_monitoring_external_mic_volume_value(self) -> int:
        return self.__cmp_monitoring_external_mic.get_slider_value()

    def set_monitoring_external_mic_volume_value(self, value: int) -> None:
        self.__cmp_monitoring_external_mic.set_slider_value(value)

    def set_monitoring_external_mic_volume_enabled(self, enabled: bool) -> None:
        self.__cmp_monitoring_external_mic.set_slider_enabled(enabled)

    def set_monitoring_external_mic_gears_enabled(self, enabled: bool) -> None:
        self.__cmp_monitoring_external_mic.set_gears_enabled(enabled)

    # --- monitoring: spdif-in ---

    def set_monitoring_spdif_in_toggle_value(self, active: bool) -> None:
        self.__cmp_monitoring_spdif_in.set_toggle_value(active)

    def set_monitoring_spdif_in_toggle_enabled(self, enabled: bool) -> None:
        self.__cmp_monitoring_spdif_in.set_toggle_enabled(enabled)

    def get_monitoring_spdif_in_volume_value(self) -> int:
        return self.__cmp_monitoring_spdif_in.get_slider_value()

    def set_monitoring_spdif_in_volume_value(self, value: int) -> None:
        self.__cmp_monitoring_spdif_in.set_slider_value(value)

    def set_monitoring_spdif_in_volume_enabled(self, enabled: bool) -> None:
        self.__cmp_monitoring_spdif_in.set_slider_enabled(enabled)

    def set_monitoring_spdif_in_gears_enabled(self, enabled: bool) -> None:
        self.__cmp_monitoring_spdif_in.set_gears_enabled(enabled)

    # --- recording: external mic ---

    def set_recording_external_mic_toggle_value(self, active: bool) -> None:
        self.__cmp_recording_external_mic.set_toggle_value(active)

    def set_recording_external_mic_toggle_enabled(self, enabled: bool) -> None:
        self.__cmp_recording_external_mic.set_toggle_enabled(enabled)

    def get_recording_external_mic_volume_value(self) -> int:
        return self.__cmp_recording_external_mic.get_slider_value()

    def set_recording_external_mic_volume_value(self, value: int) -> None:
        self.__cmp_recording_external_mic.set_slider_value(value)

    def set_recording_external_mic_volume_enabled(self, enabled: bool) -> None:
        self.__cmp_recording_external_mic.set_slider_enabled(enabled)

    def set_recording_external_mic_gears_enabled(self, enabled: bool) -> None:
        self.__cmp_recording_external_mic.set_gears_enabled(enabled)

    # --- recording: line-in ---

    def set_recording_line_in_toggle_value(self, active: bool) -> None:
        self.__cmp_recording_line_in.set_toggle_value(active)

    def set_recording_line_in_toggle_enabled(self, enabled: bool) -> None:
        self.__cmp_recording_line_in.set_toggle_enabled(enabled)

    def get_recording_line_in_volume_value(self) -> int:
        return self.__cmp_recording_line_in.get_slider_value()

    def set_recording_line_in_volume_value(self, value: int) -> None:
        self.__cmp_recording_line_in.set_slider_value(value)

    def set_recording_line_in_volume_enabled(self, enabled: bool) -> None:
        self.__cmp_recording_line_in.set_slider_enabled(enabled)

    def set_recording_line_in_gears_enabled(self, enabled: bool) -> None:
        self.__cmp_recording_line_in.set_gears_enabled(enabled)

    # --- recording: spdif-in ---

    def set_recording_spdif_in_toggle_value(self, active: bool) -> None:
        self.__cmp_recording_spdif_in.set_toggle_value(active)

    def set_recording_spdif_in_toggle_enabled(self, enabled: bool) -> None:
        self.__cmp_recording_spdif_in.set_toggle_enabled(enabled)

    def get_recording_spdif_in_volume_value(self) -> int:
        return self.__cmp_recording_spdif_in.get_slider_value()

    def set_recording_spdif_in_volume_value(self, value: int) -> None:
        self.__cmp_recording_spdif_in.set_slider_value(value)

    def set_recording_spdif_in_volume_enabled(self, enabled: bool) -> None:
        self.__cmp_recording_spdif_in.set_slider_enabled(enabled)

    def set_recording_spdif_in_gears_enabled(self, enabled: bool) -> None:
        self.__cmp_recording_spdif_in.set_gears_enabled(enabled)

    # --- recording: what u hear ---

    def set_recording_what_u_hear_toggle_value(self, active: bool) -> None:
        self.__cmp_recording_what_u_hear.set_toggle_value(active)

    def set_recording_what_u_hear_toggle_enabled(self, enabled: bool) -> None:
        self.__cmp_recording_what_u_hear.set_toggle_enabled(enabled)

    def get_recording_what_u_hear_volume_value(self) -> int:
        return self.__cmp_recording_what_u_hear.get_slider_value()

    def set_recording_what_u_hear_volume_value(self, value: int) -> None:
        self.__cmp_recording_what_u_hear.set_slider_value(value)

    def set_recording_what_u_hear_volume_enabled(self, enabled: bool) -> None:
        self.__cmp_recording_what_u_hear.set_slider_enabled(enabled)

    def set_recording_what_u_hear_gears_enabled(self, enabled: bool) -> None:
        self.__cmp_recording_what_u_hear.set_gears_enabled(enabled)

    # --- dialogs ---

    def show_gears_dialog(
            self,
            title: str,
            value_l: int,
            value_r: int,
    ) -> tuple[int, int] | None:
        dialog = wx.Dialog(self.__frame, title=title, size=wx.Size(360, 220))

        vbox = wx.BoxSizer(wx.VERTICAL)

        sld_l = wx.Slider(dialog,
                          minValue=MIXER_VR.get_min_value() // MIXER_VR.get_step_size(),
                          maxValue=MIXER_VR.get_max_value() // MIXER_VR.get_step_size(),
                          value=int(value_l) // MIXER_VR.get_step_size(),
                          style=wx.SL_HORIZONTAL)
        sld_r = wx.Slider(dialog,
                          minValue=MIXER_VR.get_min_value() // MIXER_VR.get_step_size(),
                          maxValue=MIXER_VR.get_max_value() // MIXER_VR.get_step_size(),
                          value=int(value_r) // MIXER_VR.get_step_size(),
                          style=wx.SL_HORIZONTAL)

        vbox.Add(wx.StaticText(dialog, label="Left"), flag=wx.ALL, border=5)
        vbox.Add(sld_l, flag=wx.ALL | wx.EXPAND, border=5)
        vbox.Add(wx.StaticText(dialog, label="Right"), flag=wx.ALL, border=5)
        vbox.Add(sld_r, flag=wx.ALL | wx.EXPAND, border=5)

        btn_sizer = dialog.CreateButtonSizer(wx.OK | wx.CANCEL)
        vbox.Add(btn_sizer, flag=wx.ALL | wx.EXPAND, border=5)

        dialog.SetSizer(vbox)
        result = dialog.ShowModal()
        if result != wx.ID_OK:
            return None
        return int(sld_l.GetValue()) * MIXER_VR.get_step_size(), int(sld_r.GetValue()) * MIXER_VR.get_step_size()


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

        playback_available = False
        monitoring_line_in_available = False
        monitoring_external_mic_available = False
        monitoring_spdif_in_available = False
        recording_external_mic_available = False
        recording_line_in_available = False
        recording_spdif_in_available = False
        recording_what_u_hear_available = False

        if self.__g6_api is not None:
            playback_available = (
                    self.__g6_api.playback_mute_available()
                    and self.__g6_api.playback_volume_available()
            )

            monitoring_line_in_available = (
                    self.__g6_api.mixer_monitoring_line_in_mute_available()
                    and self.__g6_api.mixer_monitoring_line_in_volume_available()
            )
            monitoring_external_mic_available = (
                    self.__g6_api.mixer_monitoring_external_mic_mute_available()
                    and self.__g6_api.mixer_monitoring_external_mic_volume_available()
            )
            monitoring_spdif_in_available = (
                    self.__g6_api.mixer_monitoring_spdif_in_mute_available()
                    and self.__g6_api.mixer_monitoring_spdif_in_volume_available()
            )

            recording_external_mic_available = (
                    self.__g6_api.mixer_recording_external_mic_mute_available()
                    and self.__g6_api.mixer_recording_external_mic_volume_available()
            )
            recording_line_in_available = (
                    self.__g6_api.mixer_recording_line_in_mute_available()
                    and self.__g6_api.mixer_recording_line_in_volume_available()
            )
            recording_spdif_in_available = (
                    self.__g6_api.mixer_recording_spdif_in_mute_available()
                    and self.__g6_api.mixer_recording_spdif_in_volume_available()
            )
            recording_what_u_hear_available = (
                    self.__g6_api.mixer_recording_what_u_hear_mute_available()
                    and self.__g6_api.mixer_recording_what_u_hear_volume_available()
            )

        self.__model.set_playback_available(playback_available)

        self.__model.set_monitoring_line_in_available(monitoring_line_in_available)
        self.__model.set_monitoring_external_mic_available(monitoring_external_mic_available)
        self.__model.set_monitoring_spdif_in_available(monitoring_spdif_in_available)

        self.__model.set_recording_external_mic_available(recording_external_mic_available)
        self.__model.set_recording_line_in_available(recording_line_in_available)
        self.__model.set_recording_spdif_in_available(recording_spdif_in_available)
        self.__model.set_recording_what_u_hear_available(recording_what_u_hear_available)

    # --- playback (speakers) ---

    def on_toggle_playback(self, event) -> None:
        # receive value
        active = bool(event.GetEventObject().GetValue())

        # update model
        self.__model.set_playback_active(active)

        # send command to G6
        if self.__g6_api is not None:
            self.__g6_api.playback_mute(mute=not active)
            if active:
                self.__g6_api.playback_volume(volume_percent=self.__model.get_playback_volume(), channels=BOTH_CHANNELS)

    def on_slide_playback(self, event) -> None:
        # receive value
        value = self.__view.get_playback_volume_value()

        # update model
        self.__model.set_playback_volume(value)

        # send command to G6
        if self.__g6_api is not None and self.__model.is_playback_active():
            self.__g6_api.playback_volume(volume_percent=value, channels=BOTH_CHANNELS)

    def on_gears_playback(self) -> None:
        # show dialog
        result = self.__view.show_gears_dialog(
            title="Playback Settings",
            value_l=self.__model.get_playback_volume_l(),
            value_r=self.__model.get_playback_volume_r(),
        )
        if result is None:
            return

        # update model
        value_l, value_r = result
        self.__model.set_playback_volume_l(value_l)
        self.__model.set_playback_volume_r(value_r)

        # send command to G6
        if self.__g6_api is not None and self.__model.is_playback_active():
            self.__g6_api.playback_volume(volume_percent=value_l, channels={Channel.CHANNEL_1})
            self.__g6_api.playback_volume(volume_percent=value_r, channels={Channel.CHANNEL_2})

    # --- monitoring: line-in ---

    def on_toggle_monitoring_line_in(self, event) -> None:
        # receive value
        active = bool(event.GetEventObject().GetValue())

        # update model
        self.__model.set_monitoring_line_in_active(active)

        # send command to G6
        if self.__g6_api is not None:
            self.__g6_api.mixer_monitoring_line_in_mute(mute=not active)
            if active:
                self.__g6_api.mixer_monitoring_line_in_volume(
                    volume_percent=self.__model.get_monitoring_line_in_volume(),
                    channels=BOTH_CHANNELS,
                )

    def on_slide_monitoring_line_in(self, event) -> None:
        # receive value
        value = self.__view.get_monitoring_line_in_volume_value()

        # update model
        self.__model.set_monitoring_line_in_volume(value)

        # send command to G6
        if self.__g6_api is not None and self.__model.is_monitoring_line_in_active():
            self.__g6_api.mixer_monitoring_line_in_volume(volume_percent=value, channels=BOTH_CHANNELS)

    def on_gears_monitoring_line_in(self) -> None:
        # show dialog
        result = self.__view.show_gears_dialog(
            title="Monitoring Line-In Settings",
            value_l=self.__model.get_monitoring_line_in_volume_l(),
            value_r=self.__model.get_monitoring_line_in_volume_r(),
        )
        if result is None:
            return

        # update model
        value_l, value_r = result
        self.__model.set_monitoring_line_in_volume_l(value_l)
        self.__model.set_monitoring_line_in_volume_r(value_r)

        # send command to G6
        if self.__g6_api is not None and self.__model.is_monitoring_line_in_active():
            self.__g6_api.mixer_monitoring_line_in_volume(volume_percent=value_l, channels={Channel.CHANNEL_1})
            self.__g6_api.mixer_monitoring_line_in_volume(volume_percent=value_r, channels={Channel.CHANNEL_2})

    # --- monitoring: external mic ---

    def on_toggle_monitoring_external_mic(self, event) -> None:
        # receive value
        active = bool(event.GetEventObject().GetValue())

        # update model
        self.__model.set_monitoring_external_mic_active(active)

        # send command to G6
        if self.__g6_api is not None:
            self.__g6_api.mixer_monitoring_external_mic_mute(mute=not active)
            if active:
                self.__g6_api.mixer_monitoring_external_mic_volume(
                    volume_percent=self.__model.get_monitoring_external_mic_volume(),
                    channels=BOTH_CHANNELS,
                )

    def on_slide_monitoring_external_mic(self, event) -> None:
        # receive value
        value = self.__view.get_monitoring_external_mic_volume_value()

        # update model
        self.__model.set_monitoring_external_mic_volume(value)

        # send command to G6
        if self.__g6_api is not None and self.__model.is_monitoring_external_mic_active():
            self.__g6_api.mixer_monitoring_external_mic_volume(volume_percent=value, channels=BOTH_CHANNELS)

    def on_gears_monitoring_external_mic(self) -> None:
        # show dialog
        result = self.__view.show_gears_dialog(
            title="Monitoring External Mic Settings",
            value_l=self.__model.get_monitoring_external_mic_volume_l(),
            value_r=self.__model.get_monitoring_external_mic_volume_r(),
        )
        if result is None:
            return

        # update model
        value_l, value_r = result
        self.__model.set_monitoring_external_mic_volume_l(value_l)
        self.__model.set_monitoring_external_mic_volume_r(value_r)

        # send command to G6
        if self.__g6_api is not None and self.__model.is_monitoring_external_mic_active():
            self.__g6_api.mixer_monitoring_external_mic_volume(volume_percent=value_l, channels={Channel.CHANNEL_1})
            self.__g6_api.mixer_monitoring_external_mic_volume(volume_percent=value_r, channels={Channel.CHANNEL_2})

    # --- monitoring: spdif-in ---

    def on_toggle_monitoring_spdif_in(self, event) -> None:
        # receive value
        active = bool(event.GetEventObject().GetValue())

        # update model
        self.__model.set_monitoring_spdif_in_active(active)

        # send command to G6
        if self.__g6_api is not None:
            self.__g6_api.mixer_monitoring_spdif_in_mute(mute=not active)
            if active:
                self.__g6_api.mixer_monitoring_spdif_in_volume(
                    volume_percent=self.__model.get_monitoring_spdif_in_volume(),
                    channels=BOTH_CHANNELS,
                )

    def on_slide_monitoring_spdif_in(self, event) -> None:
        # receive value
        value = self.__view.get_monitoring_spdif_in_volume_value()

        # update model
        self.__model.set_monitoring_spdif_in_volume(value)

        # send command to G6
        if self.__g6_api is not None and self.__model.is_monitoring_spdif_in_active():
            self.__g6_api.mixer_monitoring_spdif_in_volume(volume_percent=value, channels=BOTH_CHANNELS)

    def on_gears_monitoring_spdif_in(self) -> None:
        # show dialog
        result = self.__view.show_gears_dialog(
            title="Monitoring SPDIF-In Settings",
            value_l=self.__model.get_monitoring_spdif_in_volume_l(),
            value_r=self.__model.get_monitoring_spdif_in_volume_r(),
        )
        if result is None:
            return

        # update model
        value_l, value_r = result
        self.__model.set_monitoring_spdif_in_volume_l(value_l)
        self.__model.set_monitoring_spdif_in_volume_r(value_r)

        # send command to G6
        if self.__g6_api is not None and self.__model.is_monitoring_spdif_in_active():
            self.__g6_api.mixer_monitoring_spdif_in_volume(volume_percent=value_l, channels={Channel.CHANNEL_1})
            self.__g6_api.mixer_monitoring_spdif_in_volume(volume_percent=value_r, channels={Channel.CHANNEL_2})

    # --- recording: external mic ---

    def on_toggle_recording_external_mic(self, event) -> None:
        # receive value
        active = bool(event.GetEventObject().GetValue())

        # update model
        self.__model.set_recording_external_mic_active(active)

        # send command to G6
        if self.__g6_api is not None:
            self.__g6_api.mixer_recording_external_mic_mute(mute=not active)
            if active:
                self.__g6_api.mixer_recording_external_mic_volume(
                    volume_percent=self.__model.get_recording_external_mic_volume(),
                    channels=BOTH_CHANNELS,
                )

    def on_slide_recording_external_mic(self, event) -> None:
        # receive value
        value = self.__view.get_recording_external_mic_volume_value()

        # update model
        self.__model.set_recording_external_mic_volume(value)

        # send command to G6
        if self.__g6_api is not None and self.__model.is_recording_external_mic_active():
            self.__g6_api.mixer_recording_external_mic_volume(volume_percent=value, channels=BOTH_CHANNELS)

    def on_gears_recording_external_mic(self) -> None:
        # show dialog
        result = self.__view.show_gears_dialog(
            title="Recording External Mic Settings",
            value_l=self.__model.get_recording_external_mic_volume_l(),
            value_r=self.__model.get_recording_external_mic_volume_r(),
        )
        if result is None:
            return

        # update model
        value_l, value_r = result
        self.__model.set_recording_external_mic_volume_l(value_l)
        self.__model.set_recording_external_mic_volume_r(value_r)

        # send command to G6
        if self.__g6_api is not None and self.__model.is_recording_external_mic_active():
            self.__g6_api.mixer_recording_external_mic_volume(volume_percent=value_l, channels={Channel.CHANNEL_1})
            self.__g6_api.mixer_recording_external_mic_volume(volume_percent=value_r, channels={Channel.CHANNEL_2})

    # --- recording: line-in ---

    def on_toggle_recording_line_in(self, event) -> None:
        # receive value
        active = bool(event.GetEventObject().GetValue())

        # update model
        self.__model.set_recording_line_in_active(active)

        # send command to G6
        if self.__g6_api is not None:
            self.__g6_api.mixer_recording_line_in_mute(mute=not active)
            if active:
                self.__g6_api.mixer_recording_line_in_volume(
                    volume_percent=self.__model.get_recording_line_in_volume(),
                    channels=BOTH_CHANNELS,
                )

    def on_slide_recording_line_in(self, event) -> None:
        # receive value
        value = self.__view.get_recording_line_in_volume_value()

        # update model
        self.__model.set_recording_line_in_volume(value)

        # send command to G6
        if self.__g6_api is not None and self.__model.is_recording_line_in_active():
            self.__g6_api.mixer_recording_line_in_volume(volume_percent=value, channels=BOTH_CHANNELS)

    def on_gears_recording_line_in(self) -> None:
        # show dialog
        result = self.__view.show_gears_dialog(
            title="Recording Line-In Settings",
            value_l=self.__model.get_recording_line_in_volume_l(),
            value_r=self.__model.get_recording_line_in_volume_r(),
        )
        if result is None:
            return

        # update model
        value_l, value_r = result
        self.__model.set_recording_line_in_volume_l(value_l)
        self.__model.set_recording_line_in_volume_r(value_r)

        # send command to G6
        if self.__g6_api is not None and self.__model.is_recording_line_in_active():
            self.__g6_api.mixer_recording_line_in_volume(volume_percent=value_l, channels={Channel.CHANNEL_1})
            self.__g6_api.mixer_recording_line_in_volume(volume_percent=value_r, channels={Channel.CHANNEL_2})

    # --- recording: spdif-in ---

    def on_toggle_recording_spdif_in(self, event) -> None:
        # receive value
        active = bool(event.GetEventObject().GetValue())

        # update model
        self.__model.set_recording_spdif_in_active(active)

        # send command to G6
        if self.__g6_api is not None:
            self.__g6_api.mixer_recording_spdif_in_mute(mute=not active)
            if active:
                self.__g6_api.mixer_recording_spdif_in_volume(
                    volume_percent=self.__model.get_recording_spdif_in_volume(),
                    channels=BOTH_CHANNELS,
                )

    def on_slide_recording_spdif_in(self, event) -> None:
        # receive value
        value = self.__view.get_recording_spdif_in_volume_value()

        # update model
        self.__model.set_recording_spdif_in_volume(value)

        # send command to G6
        if self.__g6_api is not None and self.__model.is_recording_spdif_in_active():
            self.__g6_api.mixer_recording_spdif_in_volume(volume_percent=value, channels=BOTH_CHANNELS)

    def on_gears_recording_spdif_in(self) -> None:
        # show dialog
        result = self.__view.show_gears_dialog(
            title="Recording SPDIF-In Settings",
            value_l=self.__model.get_recording_spdif_in_volume_l(),
            value_r=self.__model.get_recording_spdif_in_volume_r(),
        )
        if result is None:
            return

        # update model
        value_l, value_r = result
        self.__model.set_recording_spdif_in_volume_l(value_l)
        self.__model.set_recording_spdif_in_volume_r(value_r)

        # send command to G6
        if self.__g6_api is not None and self.__model.is_recording_spdif_in_active():
            self.__g6_api.mixer_recording_spdif_in_volume(volume_percent=value_l, channels={Channel.CHANNEL_1})
            self.__g6_api.mixer_recording_spdif_in_volume(volume_percent=value_r, channels={Channel.CHANNEL_2})

    # --- recording: what u hear ---

    def on_toggle_recording_what_u_hear(self, event) -> None:
        # receive value
        active = bool(event.GetEventObject().GetValue())

        # update model
        self.__model.set_recording_what_u_hear_active(active)

        # send command to G6
        if self.__g6_api is not None:
            self.__g6_api.mixer_recording_what_u_hear_mute(mute=not active)
            if active:
                self.__g6_api.mixer_recording_what_u_hear_volume(
                    volume_percent=self.__model.get_recording_what_u_hear_volume(),
                    channels=BOTH_CHANNELS,
                )

    def on_slide_recording_what_u_hear(self, event) -> None:
        # receive value
        value = self.__view.get_recording_what_u_hear_volume_value()

        # update model
        self.__model.set_recording_what_u_hear_volume(value)

        # send command to G6
        if self.__g6_api is not None and self.__model.is_recording_what_u_hear_active():
            self.__g6_api.mixer_recording_what_u_hear_volume(volume_percent=value, channels=BOTH_CHANNELS)

    def on_gears_recording_what_u_hear(self) -> None:
        # show dialog
        result = self.__view.show_gears_dialog(
            title="Recording What U Hear Settings",
            value_l=self.__model.get_recording_what_u_hear_volume_l(),
            value_r=self.__model.get_recording_what_u_hear_volume_r(),
        )
        if result is None:
            return

        # update model
        value_l, value_r = result
        self.__model.set_recording_what_u_hear_volume_l(value_l)
        self.__model.set_recording_what_u_hear_volume_r(value_r)

        # send command to G6
        if self.__g6_api is not None and self.__model.is_recording_what_u_hear_active():
            self.__g6_api.mixer_recording_what_u_hear_volume(volume_percent=value_l, channels={Channel.CHANNEL_1})
            self.__g6_api.mixer_recording_what_u_hear_volume(volume_percent=value_r, channels={Channel.CHANNEL_2})


class MixerTab:
    def __init__(self, frame: wx.Frame):
        self.__model = Model()
        self.__view = View(frame=frame)
        self.__controller = Controller()

        self.__model.bind(self.__view)
        self.__view.bind(self.__controller)
        self.__controller.bind(self.__model, self.__view)

    def create(self, notebook: wx.Notebook) -> wx.Panel:
        return self.__view.create(notebook)

    def update_availability(self, g6_api: G6Api | None):
        self.__controller.update_availability(g6_api=g6_api)
