import os

import wx
from wx import Bitmap


def read_png_from_file(file_name: str, expected_width: int) -> Bitmap:
    relative_image_path = f"icons/{file_name}"
    if os.path.exists(relative_image_path):
        return wx.Bitmap(name=relative_image_path, type=wx.BITMAP_TYPE_PNG)
    return wx.Bitmap(width=expected_width, height=expected_width, depth=1)
