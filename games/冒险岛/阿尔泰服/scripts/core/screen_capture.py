"""
屏幕捕获与图像识别 - Artale 专用
基于 OpenCV 模板匹配
"""

import cv2
import numpy as np
import pyautogui
from PIL import Image
import time
from config import SCREEN


class ScreenCapture:
    """屏幕捕获与图像识别 for Artale"""

    def __init__(self, window_title="MapleStory Worlds"):
        self.window_title = window_title
        self.threshold = SCREEN["template_match_threshold"]

    def capture_window(self):
        """
        截取游戏窗口画面
        需要游戏处于窗口模式
        """
        # 使用 pyautogui 截图
        screenshot = pyautogui.screenshot()
        # 转换为 OpenCV 格式
        img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        return img

    def find_template(self, screen_img, template_path):
        """
        在截图中查找模板图像
        返回: (found: bool, center: (x, y) or None, confidence: float)
        """
        template = cv2.imread(template_path)
        if template is None:
            print(f"⚠️ 模板不存在: {template_path}")
            return False, None, 0.0

        result = cv2.matchTemplate(screen_img, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        if max_val >= self.threshold:
            h, w = template.shape[:2]
            center = (max_loc[0] + w // 2, max_loc[1] + h // 2)
            return True, center, max_val
        return False, None, max_val

    def find_all_templates(self, screen_img, template_path):
        """
        查找所有匹配的模板位置
        返回: [(center, confidence), ...]
        """
        template = cv2.imread(template_path)
        if template is None:
            return []

        result = cv2.matchTemplate(screen_img, template, cv2.TM_CCOEFF_NORMED)
        h, w = template.shape[:2]

        locations = np.where(result >= self.threshold)
        matches = []
        for pt in zip(*locations[::-1]):
            center = (pt[0] + w // 2, pt[1] + h // 2)
            conf = result[pt[1], pt[0]]
            matches.append((center, conf))

        return matches

    def find_player(self, screen_img):
        """
        识别玩家角色位置
        使用角色名牌模板
        """
        from config import CHARACTER
        name_tag_path = CHARACTER["name_tag_template"]
        found, center, conf = self.find_template(screen_img, name_tag_path)
        if found:
            print(f"✅ 找到玩家位置: {center} (置信度: {conf:.2f})")
        return found, center, conf

    def find_monsters(self, screen_img, monster_templates):
        """
        识别屏幕上的所有怪物
        monster_templates: list of template paths
        返回: [(center, monster_type), ...]
        """
        all_monsters = []
        for template_path in monster_templates:
            matches = self.find_all_templates(screen_img, template_path)
            monster_type = template_path.split("/")[-1].replace(".png", "")
            for center, conf in matches:
                all_monsters.append((center, monster_type, conf))

        # 按距离玩家的距离排序（优先攻击近的）
        player_found, player_pos, _ = self.find_player(screen_img)
        if player_found:
            all_monsters.sort(key=lambda x: self._distance(player_pos, x[0]))

        return all_monsters

    def _distance(self, pos1, pos2):
        """计算两点距离"""
        return ((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2) ** 0.5

    def is_hp_low(self, screen_img):
        """检测角色血量是否过低（需要牧师治疗）"""
        from config import PRIEST
        hp_threshold = PRIEST["heal_hp_threshold"]
        # 简化判断：检测红色血条区域
        # TODO: 需要实际截图模板来判断血量
        return False

    def wait_for_image(self, template_path, timeout=30):
        """等待图像出现"""
        start = time.time()
        while time.time() - start < timeout:
            img = self.capture_window()
            found, center, _ = self.find_template(img, template_path)
            if found:
                return True, center
            time.sleep(0.5)
        return False, None
