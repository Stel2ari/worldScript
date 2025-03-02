import threading
import time
import tkinter as tk
import random

import keyboard
import pyautogui as pg
from worldMethods.radomMethods import *
from worldMethods.checkIfPngInScreen import image_detection

flag = True


def callback(logMethod, ms):
    logMethod(f"随机等待 {ms} 毫秒")


def auto_skip(left, top, logMethod):
    time.sleep(1)
    find_skip = True
    screen_region = (left + 200, top + 620, 65, 48)  # 检测区域(left, top, width, height)
    target_image = "worldMethods/puHunPngs/skipFight.png"  # 目标图片路径
    check_interval = 0.5  # 检测间隔（秒）
    condidence = 0.8  # 匹配置信度（0-1）

    while find_skip:
        if not flag:
            logMethod(f"---------进程终止---------")
            return "stop"
        find_skip = image_detection(screen_region, target_image, condidence)

        if find_skip:
            press_button((left + 195, left + 195 + 71), (top + 618, top + 618 + 50), "跳过", logMethod)
            time.sleep(check_interval)

    return "success"


def press_button(posObjLeft, posobjTop, btnName, logMethod):
    root = tk.Tk()

    # 当前按钮的随机区域与等待时间
    randPos = random_position(posObjLeft, posobjTop)
    randTim = random_time()

    # 等待
    root.after(randTim, callback(logMethod, randTim))

    # 鼠标移动耗时500~700ms模拟人工
    pg.moveTo(*randPos, random.uniform(0.26, 0.45))
    pg.click()
    logMethod(f"点击 “{btnName}” 按钮{randPos}")


def test(a):
    while True:
        global flag
        # 监听 Ctrl+D 组合键
        keyboard.wait("ctrl+d")
        flag = False
        print("\n检测到 Ctrl+D，正在停止...")


def ph(hwnd, left, top, logMethod):
    try:
        a = 1
        thread = threading.Thread(target=test, args=(a,))
        thread.start()

        print(left, top)
        root = tk.Tk()

        logMethod("---------普混脚本开始---------")

        # 点击活动
        press_button((left + 17, left + 47), (top + 267, top + 297), "活动", logMethod)
        if not flag:
            logMethod(f"---------进程终止---------")
            return

        # 点击挑战
        press_button((left + 157, left + 217), (top + 97, top + 117), "挑战", logMethod)
        if not flag:
            logMethod(f"---------进程终止---------")
            return

        # 点击团队混战
        press_button((left + 318, left + 378), (top + 445, top + 475), "参加", logMethod)
        if not flag:
            logMethod(f"---------进程终止---------")
            return

        # 等待2.2秒
        root.after(2200, callback(logMethod, 2200))
        if not flag:
            logMethod(f"---------进程终止---------")
            return

        # 点击团队混战
        press_button((left + 74, left + 347), (top + 390, top + 418), "团队混战", logMethod)
        if not flag:
            logMethod(f"---------进程终止---------")
            return

        # 点击开始
        press_button((left + 74, left + 347), (top + 390 + 232, top + 418 + 232), "开始", logMethod)
        if not flag:
            logMethod(f"---------进程终止---------")
            return

        # 假设角色初始位置为0号格，则行进路线为 0-4-8-12-13-14-15

        # ==============================================================================
        # 点击4号格
        press_button((left + 50, left + 85), (top + 344, top + 385), "4号格", logMethod)
        if not flag:
            logMethod(f"---------进程终止---------")
            return

        # 点击战个痛快
        press_button((left + 65, left + 355), (top + 532, top + 550), "战个痛快", logMethod)
        if not flag:
            logMethod(f"---------进程终止---------")
            return

        # 进行战斗点击自动跳过
        skipResult = auto_skip(left, top, logMethod)
        if skipResult == r'stop':
            logMethod(f"---------进程终止---------")
            return

        # 等待行动
        time.sleep(9)
        # 点击继续
        press_button((left + 65, left + 355), (top + 532, top + 550), "战个痛快", logMethod)

        # ==============================================================================
        # 点击8号格
        press_button((left + 50, left + 85), (top + 344 + 113, top + 385 + 113), "8号格", logMethod)
        if not flag:
            logMethod(f"---------进程终止---------")
            return

        # 点击战个痛快
        press_button((left + 65, left + 355), (top + 532, top + 550), "战个痛快", logMethod)
        if not flag:
            logMethod(f"---------进程终止---------")
            return

        # 进行战斗点击自动跳过
        skipResult = auto_skip(left, top, logMethod)
        if skipResult == r'stop':
            logMethod(f"---------进程终止---------")
            return

        # 等待行动
        time.sleep(9)
        # 点击继续
        press_button((left + 65, left + 355), (top + 532, top + 550), "战个痛快", logMethod)

        # ==============================================================================
        # 点击12号格
        press_button((left + 50, left + 85), (top + 344 + 113 + 113, top + 385 + 113 + 113), "12号格", logMethod)
        if not flag:
            logMethod(f"---------进程终止---------")
            return

        # 点击战个痛快
        press_button((left + 65, left + 355), (top + 532, top + 550), "战个痛快", logMethod)
        if not flag:
            logMethod(f"---------进程终止---------")
            return

        # 进行战斗点击自动跳过
        skipResult = auto_skip(left, top, logMethod)
        if skipResult == r'stop':
            logMethod(f"---------进程终止---------")
            return

        # 等待行动
        time.sleep(9)
        # 点击继续
        press_button((left + 65, left + 355), (top + 532, top + 550), "战个痛快", logMethod)

        # ==============================================================================
        # 点击13号格
        press_button((left + 50 + 100, left + 85 + 100), (top + 344 + 113 + 113, top + 385 + 113 + 113), "13号格",
                     logMethod)
        if not flag:
            logMethod(f"---------进程终止---------")
            return

        # 点击战个痛快
        press_button((left + 65, left + 355), (top + 532, top + 550), "战个痛快", logMethod)
        if not flag:
            logMethod(f"---------进程终止---------")
            return

        # 进行战斗点击自动跳过
        skipResult = auto_skip(left, top, logMethod)
        if skipResult == r'stop':
            logMethod(f"---------进程终止---------")
            return

        # 等待行动
        time.sleep(9)
        # 点击继续
        press_button((left + 65, left + 355), (top + 532, top + 550), "战个痛快", logMethod)

        # ==============================================================================
        # 点击14号格
        press_button((left + 50 + 100 + 100, left + 85 + 100 + 100), (top + 344 + 113 + 113, top + 385 + 113 + 113),
                     "14号格", logMethod)
        if not flag:
            logMethod(f"---------进程终止---------")
            return

        # 点击战个痛快
        press_button((left + 65, left + 355), (top + 532, top + 550), "战个痛快", logMethod)
        if not flag:
            logMethod(f"---------进程终止---------")
            return

        # 进行战斗点击自动跳过
        skipResult = auto_skip(left, top, logMethod)
        if skipResult == r'stop':
            logMethod(f"---------进程终止---------")
            return

        # 等待行动
        time.sleep(9)
        # 点击继续
        press_button((left + 65, left + 355), (top + 532, top + 550), "战个痛快", logMethod)

        # ==============================================================================
        # 点击15号格
        press_button((left + 50 + 100 + 100 + 100, left + 85 + 100 + 100 + 100),
                     (top + 344 + 113 + 113, top + 385 + 113 + 113), "15号格", logMethod)
        if not flag:
            logMethod(f"---------进程终止---------")
            return

        # 点击战个痛快
        press_button((left + 65, left + 355), (top + 532, top + 550), "战个痛快", logMethod)
        if not flag:
            logMethod(f"---------进程终止---------")
            return

        # 进行战斗点击自动跳过
        skipResult = auto_skip(left, top, logMethod)
        if skipResult == r'stop':
            logMethod(f"---------进程终止---------")
            return

        # 等待行动
        time.sleep(9)
        # 点击继续
        press_button((left + 65, left + 355), (top + 532, top + 550), "战个痛快", logMethod)

        # ==============================================================================
        # 点击16号格
        press_button((left + 50 + 100 + 100 + 100 + 100, left + 85 + 100 + 100 + 100 + 100),
                     (top + 344 + 113 + 113, top + 385 + 113 + 113), "16号格", logMethod)
        if not flag:
            logMethod(f"---------进程终止---------")
            return

        logMethod("---------普混脚本结束---------")

        return
    except Exception as e:
        logMethod(f"发生错误: {str(e)}")
