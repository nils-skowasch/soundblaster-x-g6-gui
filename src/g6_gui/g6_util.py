import os

import wx
from wx import Bitmap

from importlib.resources import files

def read_png_from_file(file_name: str, expected_width: int) -> Bitmap:
    image_path = str(files("g6_gui.icons").joinpath(file_name))
    if os.path.exists(image_path):
        return wx.Bitmap(name=image_path, type=wx.BITMAP_TYPE_PNG)
    return wx.Bitmap(width=expected_width, height=expected_width, depth=1)
