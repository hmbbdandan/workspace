"""
屏幕捕获与图像识别 - Artale 冒险岛
基于 OpenCV 模板匹配
"""

import cv2
import numpy as np
import time


class ScreenCapture:
    """屏幕捕获与图像识别"""

    def __init__(self, device_manager):
        self.dm = device_manager
        self.threshold = 0.80

    def capture(self, device_index):
        """捕获设备屏幕，返回OpenCV图像"""
        raw = self.dm.screenshot(device_index)
        img = cv2.imdecode(np.frombuffer(raw, np.uint8), cv2.IMREAD_COLOR)
        return img

    def find_template(self, screenshot, template_path, threshold=None):
        """
        在截图中查找模板图像
        返回: (found: bool, center: (x, y) or None, confidence: float)
        """
        if threshold is None:
            threshold = self.threshold

        template = cv2.imread(template_path)
        if template is None:
            print(f"⚠️ 模板不存在: {template_path}")
            return False, None, 0.0

        result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        if max_val >= threshold:
            h, w = template.shape[:2]
            center = (max_loc[0] + w // 2, max_loc[1] + h // 2)
            return True, center, max_val
        return False, None, max_val

    def find_all(self, screenshot, template_path, threshold=None):
        """
        查找所有匹配位置
        返回: [(center, confidence), ...]
        """
        if threshold is None:
            threshold = self.threshold

        template = cv2.imread(template_path)
        if template is None:
            return []

        result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        h, w = template.shape[:2]

        locations = np.where(result >= threshold)
        matches = []
        for pt in zip(*locations[::-1]):
            center = (pt[0] + w // 2, pt[1] + h // 2)
            conf = result[pt[1], pt[0]]
            matches.append((center, conf))

        return matches

    def wait_for(self, device_index, template_path, timeout=30, check_interval=0.5):
        """等待图像出现"""
        start = time.time()
        while time.time() - start < timeout:
            img = self.capture(device_index)
            found, center, conf = self.find_template(img, template_path)
            if found:
                return True, center, conf
            time.sleep(check_interval)
        return False, None, 0.0

    def find_and_click(self, device_index, template_path, offset=(0, 0)):
        """查找图像并点击"""
        img = self.capture(device_index)
        found, center, conf = self.find_template(img, template_path)
        if found:
            x = center[0] + offset[0]
            y = center[1] + offset[1]
            self.dm.tap(device_index, x, y)
            return True, center
        return False, None

    # ========== 游戏特定检测 ==========

    def detect_player(self, screenshot):
        """检测玩家角色位置"""
        # 玩家角色通常有名字标签
        # 需要模板：assets/player/name_tag.png
        template_path = "assets/player/name_tag.png"
        return self.find_template(screenshot, template_path)

    def detect_monsters(self, screenshot, monster_templates):
        """检测屏幕上的怪物"""
        monsters = []
        for template_path in monster_templates:
            matches = self.find_all(screenshot, template_path)
            for center, conf in matches:
                monsters.append((center, template_path.split("/")[-1].replace(".png", ""), conf))

        # 按距离排序（假设玩家在屏幕中部偏左）
        player_found, player_pos, _ = self.detect_player(screenshot)
        if player_found:
            monsters.sort(key=lambda x: self._distance(player_pos, x[0]))
        return monsters

    def detect_hp_bar(self, screenshot):
        """检测玩家血条"""
        # 需要模板
        return self.find_template(screenshot, "assets/ui/hp_bar.png")

    def detect_mp_bar(self, screenshot):
        """检测玩家蓝条"""
        return self.find_template(screenshot, "assets/ui/mp_bar.png")

    def detect_items(self, screenshot):
        """检测掉落物品"""
        return self.find_all(screenshot, "assets/ui/drop_item.png")

    def detect_npc(self, screenshot):
        """检测NPC"""
        return self.find_all(screenshot, "assets/npc/*.png")

    def is_in_battle(self, screenshot):
        """检测是否在战斗状态"""
        # 战斗时会出现伤害数字或技能特效
        # 可以通过检测特定UI元素判断
        return False

    def is_standing(self, screenshot):
        """检测是否站立不动"""
        # 连续两帧对比，判断是否在移动
        return True

    @staticmethod
    def _distance(pos1, pos2):
        """计算两点距离"""
        return ((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2) ** 0.5
