from enum import IntEnum

import wx

from g6_cli import G6Api


class DecoderMode(IntEnum):
    NORMAL = 0
    FULL = 1
    NIGHT = 2


class Model:
    def __init__(self):
        self.__view: View | None = None

        self.__decoder_mode_available = False  # HID
        self.__decoder_mode: DecoderMode = DecoderMode.NORMAL

    def bind(self, view: "View"):
        self.__view = view

    # --- decoder mode ---

    def is_decoder_mode_available(self) -> bool:
        return self.__decoder_mode_available

    def set_decoder_mode_available(self, available: bool) -> None:
        self.__decoder_mode_available = available
        self.__handle_decoder_mode_enabled()

    def get_decoder_mode(self) -> DecoderMode:
        return self.__decoder_mode

    def set_decoder_mode(self, mode: DecoderMode) -> None:
        self.__decoder_mode = mode
        self.__view.set_decoder_mode_value(mode)

    def __handle_decoder_mode_enabled(self) -> None:
        self.__view.set_decoder_mode_enabled(self.__decoder_mode_available)


class View:
    class RadioComposite(wx.BoxSizer):
        def __init__(self, parent: wx.Panel, label: str, group_start: bool):
            super().__init__(wx.HORIZONTAL)

            radio_style = wx.RB_GROUP if group_start else 0
            self.__rad = wx.RadioButton(parent, label=label, style=radio_style)

            self.Add(self.__rad, proportion=1, flag=wx.ALL | wx.EXPAND, border=5)

        def bind_radio(self, handler) -> None:
            self.__rad.Bind(wx.EVT_RADIOBUTTON, handler)

        def set_radio_value(self, selected: bool) -> None:
            self.__rad.SetValue(selected)

        def set_radio_enabled(self, enabled: bool) -> None:
            self.__rad.Enable(enabled)

    def __init__(self):
        self.__controller: Controller | None = None

        self.__cmp_normal: View.RadioComposite | None = None
        self.__cmp_full: View.RadioComposite | None = None
        self.__cmp_night: View.RadioComposite | None = None

    def bind(self, controller: "Controller"):
        self.__controller = controller

    def create(self, notebook: wx.Notebook) -> wx.Panel:
        panel = wx.Panel(notebook)
        vbox = wx.BoxSizer(wx.VERTICAL)

        self.__cmp_normal = View.RadioComposite(panel, "Normal", group_start=True)
        self.__cmp_normal.bind_radio(lambda event: self.__controller.on_select_decoder_mode(DecoderMode.NORMAL))
        vbox.Add(self.__cmp_normal, flag=wx.EXPAND)

        self.__cmp_full = View.RadioComposite(panel, "Full", group_start=False)
        self.__cmp_full.bind_radio(lambda event: self.__controller.on_select_decoder_mode(DecoderMode.FULL))
        vbox.Add(self.__cmp_full, flag=wx.EXPAND)

        self.__cmp_night = View.RadioComposite(panel, "Night", group_start=False)
        self.__cmp_night.bind_radio(lambda event: self.__controller.on_select_decoder_mode(DecoderMode.NIGHT))
        vbox.Add(self.__cmp_night, flag=wx.EXPAND)

        panel.SetSizer(vbox)
        return panel

    # --- decoder mode ---

    def set_decoder_mode_value(self, mode: DecoderMode) -> None:
        self.__cmp_normal.set_radio_value(mode == DecoderMode.NORMAL)
        self.__cmp_full.set_radio_value(mode == DecoderMode.FULL)
        self.__cmp_night.set_radio_value(mode == DecoderMode.NIGHT)

    def set_decoder_mode_enabled(self, enabled: bool) -> None:
        self.__cmp_normal.set_radio_enabled(enabled)
        self.__cmp_full.set_radio_enabled(enabled)
        self.__cmp_night.set_radio_enabled(enabled)


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

        decoder_mode_available = False
        if self.__g6_api is not None:
            decoder_mode_available = self.__g6_api.decoder_mode_available()

        self.__model.set_decoder_mode_available(decoder_mode_available)

    def on_select_decoder_mode(self, mode: DecoderMode) -> None:
        # update model
        self.__model.set_decoder_mode(mode)

        # send command to G6
        if self.__g6_api is not None:
            self.__g6_api.decoder_mode(decoder_mode_enum=mode)


class DecoderTab:
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
