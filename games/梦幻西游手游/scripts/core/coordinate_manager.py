"""
坐标管理器 - 统一管理游戏窗口坐标

支持两种模式：
1. ADB模式：坐标为Android设备原生坐标
2. MacScreencap模式：坐标为Mac屏幕绝对坐标（游戏窗口在副屏）
"""

import subprocess
import cv2
import numpy as np


class CoordinateManager:
    """游戏窗口坐标管理"""

    # 副屏游戏窗口位置（测试得到）
    GAME_WINDOW_OFFSET_X = 1540  # 主屏宽度 + D2相对X
    GAME_WINDOW_OFFSET_Y = 148
    GAME_WIDTH = 326
    GAME_HEIGHT = 453

    def __init__(self, mode="adb"):
        """
        mode: "adb" - Android设备坐标 (MuMu模拟器)
              "mac" - Mac屏幕绝对坐标 (游戏窗口在副屏)
        """
        self.mode = mode

    def set_game_window(self, offset_x, offset_y, width, height):
        """手动设置游戏窗口位置和大小"""
        self.GAME_WINDOW_OFFSET_X = offset_x
        self.GAME_WINDOW_OFFSET_Y = offset_y
        self.GAME_WIDTH = width
        self.GAME_HEIGHT = height

    def game_to_absolute(self, game_x, game_y):
        """游戏内相对坐标 -> 绝对坐标"""
        if self.mode == "adb":
            # ADB模式：坐标已经是设备原生坐标
            return game_x, game_y
        else:
            # Mac模式：需要加上窗口偏移
            return self.GAME_WINDOW_OFFSET_X + game_x, self.GAME_WINDOW_OFFSET_Y + game_y

    def absolute_to_game(self, abs_x, abs_y):
        """绝对坐标 -> 游戏内相对坐标"""
        if self.mode == "adb":
            return abs_x, abs_y
        else:
            return abs_x - self.GAME_WINDOW_OFFSET_X, abs_y - self.GAME_WINDOW_OFFSET_Y

    def click_game(self, game_x, game_y):
        """点击游戏窗口内的相对坐标"""
        abs_x, abs_y = self.game_to_absolute(game_x, game_y)
        return abs_x, abs_y

    @staticmethod
    def detect_game_window_mac():
        """
        自动检测游戏窗口在Mac屏幕上的位置（需要先截取包含窗口的截图）
        返回: (offset_x, offset_y, width, height) or None
        """
        # 使用screencapture截取副屏
        try:
            result = subprocess.run(
                ['/usr/sbin/screencapture', '-x', '-D', '2', '/tmp/screen_detect.png'],
                capture_output=True, timeout=5
            )
            if result.returncode != 0:
                # 尝试主屏
                result = subprocess.run(
                    ['/usr/sbin/screencapture', '-x', '-D', '1', '/tmp/screen_detect.png'],
                    capture_output=True, timeout=5
                )
        except Exception:
            return None

        img = cv2.imread('/tmp/screen_detect.png')
        if img is None:
            return None

        # 检测游戏窗口边缘（深色边框 + 特定宽高比）
        # 梦幻西游手游窗口一般是326x453或类似比例
        h, w = img.shape[:2]
        print(f"  屏幕分辨率: {w}x{h}")

        return None  # 需要模板匹配才能精确确定位置

    def get_window_info(self):
        """获取当前窗口信息"""
        return {
            "mode": self.mode,
            "offset_x": self.GAME_WINDOW_OFFSET_X,
            "offset_y": self.GAME_WINDOW_OFFSET_Y,
            "width": self.GAME_WIDTH,
            "height": self.GAME_HEIGHT,
            "game_area": f"({self.GAME_WINDOW_OFFSET_X},{self.GAME_WINDOW_OFFSET_Y}) + {self.GAME_WIDTH}x{self.GAME_HEIGHT}"
        }


class RegionMatcher:
    """
    基于区域特征的快速匹配
    不需要完整模板，只需知道要点击的"特征区域"
    """

    def __init__(self, screenshot):
        self.screenshot = screenshot
        self.h, self.w = screenshot.shape[:2]

    def find_color_region(self, color_range, morphology=True):
        """
        查找指定颜色范围的区域
        color_range: ((lower_b, lower_g, lower_r), (upper_b, upper_g, upper_r))
        返回: 满足条件的中心点列表
        """
        hsv = cv2.cvtColor(self.screenshot, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, color_range[0], color_range[1])

        if morphology:
            kernel = np.ones((5, 5), np.uint8)
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        centers = []
        for cnt in contours:
            M = cv2.moments(cnt)
            if M["m00"] > 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                centers.append((cx, cy))

        return centers

    def find_template_center(self, template_path, threshold=0.8):
        """查找模板中心位置"""
        template = cv2.imread(template_path)
        if template is None:
            return None

        result = cv2.matchTemplate(self.screenshot, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        if max_val >= threshold:
            th, tw = template.shape[:2]
            center = (max_loc[0] + tw // 2, max_loc[1] + th // 2)
            return center, max_val
        return None, 0