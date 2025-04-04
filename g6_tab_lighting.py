import sys

import wx


class LightingTab:

    def __init__(self):
        self.color_picker = None
        self.txt_red = None
        self.txt_green = None
        self.txt_blue = None

    def create(self, notebook: wx.Notebook) -> wx.Panel:
        panel = wx.Panel(notebook)
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        # hbox_picker
        hbox_picker = wx.BoxSizer(wx.HORIZONTAL)
        hbox_picker.Add(wx.StaticText(panel, label="Choose Color:"), flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=5)
        self.color_picker = wx.ColourPickerCtrl(panel)
        self.color_picker.Bind(wx.EVT_COLOURPICKER_CHANGED, self.__on_color_changed)
        hbox_picker.Add(self.color_picker, flag=wx.ALL, border=5)
        hbox.Add(hbox_picker, flag=wx.ALL, border=5)

        # hbox_rgb
        hbox_rgb = wx.BoxSizer(wx.HORIZONTAL)
        ## red
        hbox_rgb.Add(wx.StaticText(panel, label="R:"), flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=5)
        self.txt_red = wx.TextCtrl(panel)
        self.txt_red.Bind(wx.EVT_KILL_FOCUS, self.__on_rgb_text_changed)
        hbox_rgb.Add(self.txt_red, flag=wx.ALL, border=5)
        ## green
        hbox_rgb.Add(wx.StaticText(panel, label="G:"), flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=5)
        self.txt_green = wx.TextCtrl(panel)
        self.txt_green.Bind(wx.EVT_KILL_FOCUS, self.__on_rgb_text_changed)
        hbox_rgb.Add(self.txt_green, flag=wx.ALL, border=5)
        ## blue
        hbox_rgb.Add(wx.StaticText(panel, label="B:"), flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=5)
        self.txt_blue = wx.TextCtrl(panel)
        self.txt_blue.Bind(wx.EVT_KILL_FOCUS, self.__on_rgb_text_changed)
        hbox_rgb.Add(self.txt_blue, flag=wx.ALL, border=5)
        hbox.Add(hbox_rgb, flag=wx.ALL, border=5)

        # btn_apply
        hbox_apply = wx.BoxSizer(wx.HORIZONTAL)
        btn_apply = wx.Button(panel, label="Apply")
        btn_apply.Bind(wx.EVT_BUTTON, self.__on_apply)
        hbox_apply.Add(btn_apply, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=5)
        hbox.Add(hbox_apply, flag=wx.ALL, border=5)

        panel.SetSizer(hbox)
        return panel

    def __on_color_changed(self, event):
        color = self.color_picker.GetColour()
        self.txt_red.SetValue(str(color.Red()))
        self.txt_green.SetValue(str(color.Green()))
        self.txt_blue.SetValue(str(color.Blue()))

    def __on_rgb_text_changed(self, event):
        try:
            red = min(max(int(self.txt_red.GetValue()), 0), 255)
            green = min(max(int(self.txt_green.GetValue()), 0), 255)
            blue = min(max(int(self.txt_blue.GetValue()), 0), 255)
            color = wx.Colour(red, green, blue)
            self.color_picker.SetColour(color)
        except ValueError as e:
            print(e, file=sys.stderr, flush=True)

    @staticmethod
    def __on_apply(event):
        print('Applying...')
