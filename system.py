import ctypes
user32 = ctypes.windll.user32
user32.SetProcessDPIAware()

def get_screen_size():
    return 768, 1024
    # return user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)


#===================================================================


from ctypes import POINTER, WINFUNCTYPE, windll
from ctypes.wintypes import BOOL, HWND, RECT

def get_bounds(hwnd):

    prototype = WINFUNCTYPE(BOOL, HWND, POINTER(RECT))
    paramflags = (1, "hwnd"), (2, "lprect")
    GetWindowRect = prototype(("GetWindowRect", windll.user32), paramflags)
    rect = GetWindowRect(hwnd)

    return rect.top, rect.left, rect.bottom-rect.top, rect.right-rect.left