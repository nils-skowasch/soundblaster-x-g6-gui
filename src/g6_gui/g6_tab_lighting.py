import wx

from g6_cli import G6Api


class Model:
    def __init__(self):
        self.__view: View | None = None

        # --- lighting ---
        self.__lighting_available = False  # HID
        self.__lighting_enabled: bool = True
        self.__red: int = 0
        self.__green: int = 0
        self.__blue: int = 0

    def bind(self, view: "View"):
        self.__view = view

    # --- lighting ---

    def is_lighting_available(self) -> bool:
        return self.__lighting_available

    def set_lighting_available(self, available: bool) -> None:
        self.__lighting_available = available
        self.__handle_lighting_enabled()

    def is_lighting_enabled(self) -> bool:
        return self.__lighting_enabled

    def set_lighting_enabled(self, enabled: bool) -> None:
        self.__lighting_enabled = enabled
        self.__handle_lighting_enabled()

    def get_red(self) -> int:
        return self.__red

    def set_red(self, value: int) -> None:
        self.__red = value
        self.__view.set_red_value(value)

    def get_green(self) -> int:
        return self.__green

    def set_green(self, value: int) -> None:
        self.__green = value
        self.__view.set_green_value(value)

    def get_blue(self) -> int:
        return self.__blue

    def set_blue(self, value: int) -> None:
        self.__blue = value
        self.__view.set_blue_value(value)

    def set_rgb(self, red: int, green: int, blue: int) -> None:
        self.__red = red
        self.__green = green
        self.__blue = blue
        self.__view.set_rgb_values(red, green, blue)

    def __handle_lighting_enabled(self) -> None:
        self.__view.set_lighting_controls_enabled(self.__lighting_available and self.__lighting_enabled)


class View:
    def __init__(self):
        self.__controller: Controller | None = None

        self.__color_picker: wx.ColourPickerCtrl | None = None
        self.__txt_red: wx.SpinCtrl | None = None
        self.__txt_green: wx.SpinCtrl | None = None
        self.__txt_blue: wx.SpinCtrl | None = None

    def bind(self, controller: "Controller"):
        self.__controller = controller

    def create(self, notebook: wx.Notebook) -> wx.Panel:
        panel = wx.Panel(notebook)
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        # hbox_picker
        hbox_picker = wx.BoxSizer(wx.HORIZONTAL)
        hbox_picker.Add(wx.StaticText(panel, label="Choose Color:"), flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=5)
        self.__color_picker = wx.ColourPickerCtrl(panel)
        self.__color_picker.Bind(wx.EVT_COLOURPICKER_CHANGED, lambda event: self.__controller.on_color_changed(event))
        hbox_picker.Add(self.__color_picker, flag=wx.ALL, border=5)
        hbox.Add(hbox_picker, flag=wx.ALL, border=5)

        # hbox_rgb
        hbox_rgb = wx.BoxSizer(wx.HORIZONTAL)
        # hbox_rgb > red
        hbox_rgb.Add(wx.StaticText(panel, label="R:"), flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=5)
        self.__txt_red = wx.SpinCtrl(panel, min=0, max=255, initial=0)
        self.__txt_red.Bind(wx.EVT_SPINCTRL, lambda event: self.__controller.on_rgb_text_changed(event))
        hbox_rgb.Add(self.__txt_red, flag=wx.ALL, border=5)
        # hbox_rgb > green
        hbox_rgb.Add(wx.StaticText(panel, label="G:"), flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=5)
        self.__txt_green = wx.SpinCtrl(panel, min=0, max=255, initial=0)
        self.__txt_green.Bind(wx.EVT_SPINCTRL, lambda event: self.__controller.on_rgb_text_changed(event))
        hbox_rgb.Add(self.__txt_green, flag=wx.ALL, border=5)
        # hbox_rgb > blue
        hbox_rgb.Add(wx.StaticText(panel, label="B:"), flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=5)
        self.__txt_blue = wx.SpinCtrl(panel, min=0, max=255, initial=0)
        self.__txt_blue.Bind(wx.EVT_SPINCTRL, lambda event: self.__controller.on_rgb_text_changed(event))
        hbox_rgb.Add(self.__txt_blue, flag=wx.ALL, border=5)
        hbox.Add(hbox_rgb, flag=wx.ALL, border=5)

        panel.SetSizer(hbox)
        return panel

    # --- lighting ---

    def set_red_value(self, value: int) -> None:
        self.__txt_red.SetValue(value)
        self.__update_color_picker()

    def set_green_value(self, value: int) -> None:
        self.__txt_green.SetValue(value)
        self.__update_color_picker()

    def set_blue_value(self, value: int) -> None:
        self.__txt_blue.SetValue(value)
        self.__update_color_picker()

    def set_rgb_values(self, red: int, green: int, blue: int) -> None:
        self.__txt_red.SetValue(red)
        self.__txt_green.SetValue(green)
        self.__txt_blue.SetValue(blue)
        self.__update_color_picker()

    def get_red_value(self) -> int:
        return self.__txt_red.GetValue()

    def get_green_value(self) -> int:
        return self.__txt_green.GetValue()

    def get_blue_value(self) -> int:
        return self.__txt_blue.GetValue()

    def set_lighting_controls_enabled(self, enabled: bool) -> None:
        self.__color_picker.Enable(enabled)
        self.__txt_red.Enable(enabled)
        self.__txt_green.Enable(enabled)
        self.__txt_blue.Enable(enabled)

    def __update_color_picker(self) -> None:
        red = self.__txt_red.GetValue()
        green = self.__txt_green.GetValue()
        blue = self.__txt_blue.GetValue()
        color = wx.Colour(red, green, blue)
        self.__color_picker.SetColour(color)


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

        lighting_available = False
        if self.__g6_api is not None:
            lighting_available = self.__g6_api.lighting_enable_set_rgb_available()

        self.__model.set_lighting_available(lighting_available)

        # load the currently selected profile and sync UI with model
        if self.__g6_api is not None:
            self.__apply_api_model()

    def __apply_api_model(self):
        # load lighting data from api model
        if self.__g6_api is None:
            return
        lighting = self.__g6_api.get_model().get_lighting()

        # update ui model
        self.__model.set_lighting_enabled(lighting.get_enabled())
        self.__model.set_rgb(red=lighting.get_rgb()[0], green=lighting.get_rgb()[1], blue=lighting.get_rgb()[2])

    def on_color_changed(self, event) -> None:
        # get color from color picker
        color = event.GetColour()
        red = color.Red()
        green = color.Green()
        blue = color.Blue()

        # update model
        self.__model.set_rgb(red, green, blue)

        # send command to G6
        if self.__g6_api is not None:
            self.__g6_api.lighting_enable_set_rgb(red=red, green=green, blue=blue)

    def on_rgb_text_changed(self, event) -> None:
        # get RGB values from spin controls
        red = min(max(self.__view.get_red_value(), 0), 255)
        green = min(max(self.__view.get_green_value(), 0), 255)
        blue = min(max(self.__view.get_blue_value(), 0), 255)

        # update model
        self.__model.set_rgb(red, green, blue)

        # send command to G6
        if self.__g6_api is not None:
            self.__g6_api.lighting_enable_set_rgb(red=red, green=green, blue=blue)


class LightingTab:
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
