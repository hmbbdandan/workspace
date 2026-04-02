"""
屏幕捕获与图像识别模块
"""

import cv2
import numpy as np
from PIL import Image
import io
import time
from config.settings import CV


class ScreenCapture:
    """屏幕捕获与图像识别"""

    def __init__(self, device_manager):
        self.dm = device_manager
        self.threshold = CV["threshold"]
        self.timeout = CV["wait_timeout"]

    def capture(self, device_index):
        """捕获指定设备的屏幕，返回OpenCV图像"""
        raw = self.dm.screenshot(device_index)
        img = cv2.imdecode(np.frombuffer(raw, np.uint8), cv2.IMREAD_COLOR)
        return img

    def find_image(self, screenshot, template_path, threshold=None):
        """
        在截图中查找模板图像
        返回: (found: bool, center: (x, y) or None)
        """
        if threshold is None:
            threshold = self.threshold

        template = cv2.imread(template_path)
        if template is None:
            raise FileNotFoundError(f"模板文件不存在: {template_path}")

        result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        if max_val >= threshold:
            h, w = template.shape[:2]
            center = (max_loc[0] + w // 2, max_loc[1] + h // 2)
            return True, center
        return False, None

    def find_all(self, screenshot, template_path, threshold=None):
        """
        查找所有匹配位置
        返回: [(center, confidence), ...]
        """
        if threshold is None:
            threshold = self.threshold

        template = cv2.imread(template_path)
        if template is None:
            raise FileNotFoundError(f"模板文件不存在: {template_path}")

        result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        h, w = template.shape[:2]

        locations = np.where(result >= threshold)
        matches = []
        for pt in zip(*locations[::-1]):
            center = (pt[0] + w // 2, pt[1] + h // 2)
            conf = result[pt[1], pt[0]]
            matches.append((center, conf))

        return matches

    def wait_for_image(self, device_index, template_path, timeout=None, check_interval=0.5):
        """
        等待图像出现
        返回: (found: bool, center: (x, y) or None, time_cost: float)
        """
        if timeout is None:
            timeout = self.timeout

        start = time.time()
        while time.time() - start < timeout:
            img = self.capture(device_index)
            found, center = self.find_image(img, template_path)
            if found:
                return True, center, time.time() - start
            time.sleep(check_interval)

        return False, None, time.time() - start

    def click_on_found(self, device_index, template_path, offset=(0, 0)):
        """查找图像并点击"""
        img = self.capture(device_index)
        found, center = self.find_image(img, template_path)
        if found:
            x, y = center[0] + offset[0], center[1] + offset[1]
            self.dm.tap(device_index, x, y)
            return True
        return False
