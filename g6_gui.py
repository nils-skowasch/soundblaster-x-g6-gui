import wx


def print_hi(name):
    print(f'Hi, {name}')

    # Next, create an application object.
    app = wx.App()

    # Then a frame.
    frm = wx.Frame(None, title="Hello World")

    # Show it.
    frm.Show()

    # Start the event loop.
    app.MainLoop()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
