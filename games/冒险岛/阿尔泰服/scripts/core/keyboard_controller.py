"""
键盘控制模块 - 模拟按键操作
"""

import pyautogui
import time
import random
from pynput.keyboard import Controller, Key
from config import KEYBOARD, ANTIBAN


class KeyboardController:
    """键盘控制 for Artale"""

    def __init__(self):
        self.keyboard = Controller()
        self.cfg = KEYBOARD
        self.antiban = ANTIBAN

    def _random_delay(self):
        """随机延迟（防封）"""
        delay = random.uniform(
            self.antiban["min_action_delay"],
            self.antiban["max_action_delay"]
        )
        time.sleep(delay)

    def press_key(self, key):
        """按下一个键"""
        self.keyboard.press(key)
        time.sleep(0.05)
        self.keyboard.release(key)
        self._random_delay()

    def hold_key(self, key, duration=0.5):
        """按住一个键"""
        self.keyboard.press(key)
        time.sleep(duration)
        self.keyboard.release(key)
        self._random_delay()

    def move_left(self):
        """向左移动"""
        self.press_key(self.cfg["move_left"])

    def move_right(self):
        """向右移动"""
        self.press_key(self.cfg["move_right"])

    def jump(self):
        """跳跃"""
        self.press_key(self.cfg["jump"])

    def attack(self):
        """普通攻击"""
        self.press_key(self.cfg["attack"])

    def use_skill(self, skill_key):
        """使用技能"""
        self.press_key(skill_key)

    def pickup(self):
        """捡物"""
        delay = random.uniform(0.1, self.antiban["random_pickup_delay"])
        time.sleep(delay)
        self.press_key(self.cfg["pickup"])

    def sit(self):
        """坐下休息"""
        self.press_key(self.cfg["sit"])

    def priest_heal(self):
        """牧师治疗"""
        self.use_skill(self.cfg.get("heal", "s"))

    def priest_buff(self):
        """牧师加Buff"""
        self.use_skill(self.cfg.get("buff", "q"))

    def combo_attack_right(self, attack_count=3):
        """
        组合攻击：向右移动并攻击
        常用于边移动边打怪
        """
        for _ in range(attack_count):
            self.attack()
            time.sleep(0.1)
            self.move_right()
            time.sleep(0.1)

    def combo_attack_left(self, attack_count=3):
        """组合攻击：向左移动并攻击"""
        for _ in range(attack_count):
            self.attack()
            time.sleep(0.1)
            self.move_left()
            time.sleep(0.1)

    def random_move(self):
        """随机移动（防封）"""
        actions = [self.move_left, self.move_right, self.jump]
        if self.antiban["random_movement"]:
            random.choice(actions)()
