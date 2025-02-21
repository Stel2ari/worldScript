import ctypes
from ctypes import wintypes

# 加载 user32.dll
user32 = ctypes.WinDLL("user32", use_last_error=True)


# 定义 POINT 结构体
class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]


# 定义 API 函数原型
user32.WindowFromPoint.argtypes = [POINT]
user32.WindowFromPoint.restype = wintypes.HWND

user32.GetWindowTextLengthW.argtypes = [wintypes.HWND]
user32.GetWindowTextLengthW.restype = ctypes.c_int

user32.GetWindowTextW.argtypes = [wintypes.HWND, wintypes.LPWSTR, ctypes.c_int]
user32.GetWindowTextW.restype = ctypes.c_int

user32.GetAncestor.argtypes = [wintypes.HWND, ctypes.c_uint]
user32.GetAncestor.restype = wintypes.HWND


def get_window_info(x: int, y: int) -> tuple:
    """
    根据屏幕坐标获取窗口句柄和名称
    返回值: (句柄, 窗口标题)
    """
    # 获取指定坐标处的窗口句柄
    point = POINT(x, y)
    hwnd = user32.WindowFromPoint(point)

    # 获取顶层窗口句柄 (处理子窗口情况)
    root_hwnd = user32.GetAncestor(hwnd, 2)  # GA_ROOT

    # 获取窗口标题
    text_length = user32.GetWindowTextLengthW(root_hwnd)
    if text_length > 0:
        buffer = ctypes.create_unicode_buffer(text_length + 1)
        user32.GetWindowTextW(root_hwnd, buffer, text_length + 1)
        title = buffer.value
    else:
        title = ""

    return (root_hwnd, title)
