import ctypes
from ctypes import wintypes

# 定义Windows API所需结构体和函数
user32 = ctypes.WinDLL('user32', use_last_error=True)


class RECT(ctypes.Structure):
    _fields_ = [
        ('left', wintypes.LONG),
        ('top', wintypes.LONG),
        ('right', wintypes.LONG),
        ('bottom', wintypes.LONG)
    ]


# API函数声明
user32.SetWindowPos.argtypes = (
    wintypes.HWND,  # hWnd
    wintypes.HWND,  # hWndInsertAfter
    wintypes.INT,  # X
    wintypes.INT,  # Y
    wintypes.INT,  # cx (宽度)
    wintypes.INT,  # cy (高度)
    wintypes.UINT  # uFlags
)

user32.MoveWindow.argtypes = (
    wintypes.HWND,  # hWnd
    wintypes.INT,  # X
    wintypes.INT,  # Y
    wintypes.INT,  # nWidth
    wintypes.INT,  # nHeight
    wintypes.BOOL  # bRepaint
)

# 常用标志常量
SWP_NOMOVE = 0x0002
SWP_NOZORDER = 0x0004
HWND_TOP = 0x0


def set_window_size(hwnd, logMethod):
    """
    设置窗口尺寸（保持当前位置和Z序）
    参数：
        hwnd: 窗口句柄
        width: 新宽度
        height: 新高度
    返回：成功返回True，失败返回False
    """
    flags = SWP_NOMOVE | SWP_NOZORDER
    result = user32.SetWindowPos(
        hwnd,
        HWND_TOP,
        0, 0,  # 由于使用SWP_NOMOVE，这些值被忽略
        452,
        764,
        flags
    )
    if not result:
        logMethod(f"设置窗口尺寸失败：{ctypes.WinError(ctypes.get_last_error())}")
    else:
        logMethod(f"已设置窗口尺寸：452 764")
        logMethod(f"!!!请勿移动窗口")


def get_window_position(hwnd, logMethod):
    """
    获取窗口左上角屏幕坐标
    参数：
        hwnd: 有效的窗口句柄
    返回：
        (x, y) 元组
    异常：
        当获取失败时抛出ctypes.WinError
    """
    rect = RECT()
    if not user32.GetWindowRect(hwnd, ctypes.byref(rect)):
        raise ctypes.WinError(ctypes.get_last_error())

    logMethod(f"获取窗口位置：{rect.left, rect.top}")
    return (rect.left, rect.top)





