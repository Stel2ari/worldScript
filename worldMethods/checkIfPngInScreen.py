import cv2
import numpy as np
import pyautogui
import time


def image_detection(screen_region, target_image, threshold=0.8):
    """
    检测指定屏幕区域中是否存在目标图片
    :param screen_region: (left, top, width, height)
    :param target_image: 目标图片路径
    :param threshold: 匹配阈值（0-1）
    :return: bool
    """
    # 截取屏幕区域
    screen_img = pyautogui.screenshot(region=screen_region)
    screen_img = cv2.cvtColor(np.array(screen_img), cv2.COLOR_RGB2BGR)

    # 读取目标图片
    template = cv2.imread(target_image)
    if template is None:
        raise FileNotFoundError(f"目标图片 {target_image} 未找到")

    # 执行模板匹配
    result = cv2.matchTemplate(screen_img, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    return max_val >= threshold
