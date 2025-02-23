import tkinter as tk
from tkinter import messagebox
from PIL import ImageGrab
import pyautogui  # 用于获取屏幕尺寸验证输入


def take_screenshot():
    try:
        # 获取用户输入的坐标参数
        left = int(entry_left.get())
        top = int(entry_top.get())
        width = int(entry_width.get())
        height = int(entry_height.get())

        # 计算右下角坐标
        right = left + width
        bottom = top + height

        # 获取屏幕尺寸用于验证
        screen_width, screen_height = pyautogui.size()

        # 验证输入有效性
        if any(v < 0 for v in [left, top, width, height]):
            raise ValueError("数值不能为负数")
        if right > screen_width or bottom > screen_height:
            raise ValueError("截图区域超出屏幕范围")
        if width <= 0 or height <= 0:
            raise ValueError("宽高必须大于0")

        # 截取指定区域
        screenshot = ImageGrab.grab(bbox=(left, top, right, bottom))

        # 保存截图（文件名包含时间戳防止覆盖）
        from datetime import datetime
        filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        screenshot.save(filename)

        messagebox.showinfo("成功", f"截图已保存为 {filename}")

    except ValueError as e:
        messagebox.showerror("输入错误", str(e))
    except Exception as e:
        messagebox.showerror("错误", f"截图失败: {str(e)}")


# 创建主窗口
root = tk.Tk()
root.title("区域截图工具")

# 获取屏幕尺寸用于提示
screen_width, screen_height = pyautogui.size()

# 创建输入组件
tk.Label(root, text=f"屏幕尺寸: {screen_width}x{screen_height}").grid(row=0, columnspan=2)

tk.Label(root, text="Left:").grid(row=1, column=0)
entry_left = tk.Entry(root)
entry_left.grid(row=1, column=1)

tk.Label(root, text="Top:").grid(row=2, column=0)
entry_top = tk.Entry(root)
entry_top.grid(row=2, column=1)

tk.Label(root, text="Width:").grid(row=3, column=0)
entry_width = tk.Entry(root)
entry_width.grid(row=3, column=1)

tk.Label(root, text="Height:").grid(row=4, column=0)
entry_height = tk.Entry(root)
entry_height.grid(row=4, column=1)

# 截图按钮
capture_btn = tk.Button(root, text="截取屏幕区域", command=take_screenshot)
capture_btn.grid(row=5, columnspan=2, pady=10)

# 运行主循环
root.mainloop()
