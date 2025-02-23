import time
import tkinter as tk
import random
import pyautogui as pg
from worldMethods.radomMethods import *


def callback(logMethod, ms):
    logMethod(f"随机等待 {ms} 毫秒")


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


def ph(hwnd, left, top, logMethod):
    print(left,top)
    root = tk.Tk()

    logMethod("---------普混脚本开始---------")
    # 点击活动
    press_button((left + 17, left + 47), (top + 267, top + 297), "活动", logMethod)

    # 点击挑战
    press_button((left + 157, left + 217), (top + 97, top + 117), "挑战", logMethod)

    # 点击团队混战
    press_button((left + 318, left + 378), (top + 445, top + 475), "参加", logMethod)

    # 等待2.2秒
    root.after(2200, callback(logMethod, 2200))

    # 点击团队混战
    press_button((left + 74, left + 347), (top + 390, top + 418), "团队混战", logMethod)

    # 点击开始
    press_button((left + 74, left + 347), (top + 390 + 232, top + 418 + 232), "开始", logMethod)

    #假设角色初始位置为0号格，则行进路线为 0-4-8-12-13-14-15
    #点击4号格
    press_button((left + 50, left + 85), (top + 344, top + 385), "4号格", logMethod)

    #点击战个痛快
    press_button((left + 65, left + 355), (top + 532, top + 550), "战个痛快", logMethod)



    logMethod("---------普混脚本结束---------")
    #

