import wx


class RedirectText:
    def __init__(self, text_ctrl, color, original_stream):
        self.__text_ctrl = text_ctrl
        self.__color = color
        self.__original_stream = original_stream

    def write(self, string):
        if self.__original_stream:
            self.__original_stream.write(string)
        if self.__text_ctrl:
            try:
                wx.CallAfter(self.__safe_append, string)
            except Exception as e:
                # wx might be shutting down
                if self.__original_stream:
                    self.__original_stream.write(f"Error in RedirectText: {e}\n")

    def __safe_append(self, string):
        if self.__text_ctrl:
            self.__text_ctrl.SetDefaultStyle(wx.TextAttr(self.__color))
            self.__text_ctrl.AppendText(string)
            self.__text_ctrl.ShowPosition(self.__text_ctrl.GetLastPosition())

    def flush(self):
        if self.__original_stream:
            self.__original_stream.flush()

    # noinspection SpellCheckingInspection
    @staticmethod
    def isatty():
        return False
