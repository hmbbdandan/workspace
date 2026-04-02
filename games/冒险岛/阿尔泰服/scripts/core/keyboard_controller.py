"""
按键控制器 - Artale 冒险岛
通过ADB发送按键事件
"""

import time
import random


class KeyController:
    """按键控制 - ADB模式"""

    # Android按键码
    KEY_LEFT = 21
    KEY_RIGHT = 22
    KEY_UP = 19
    KEY_DOWN = 20
    KEY_ENTER = 66
    KEY_BACK = 4
    KEY_HOME = 3

    def __init__(self, device_manager):
        self.dm = device_manager
        self.speed_mode = "normal"

    def set_speed_mode(self, mode):
        """设置速度模式: normal / fast / turbo"""
        self.speed_mode = mode

    def _delay(self):
        """根据速度模式延迟"""
        delays = {
            "normal": (0.5, 1.5),
            "fast": (0.1, 0.3),
            "turbo": (0.05, 0.1),
        }
        min_d, max_d = delays.get(self.speed_mode, (0.5, 1.5))
        time.sleep(random.uniform(min_d, max_d))

    def tap(self, device_index, x, y):
        """点击坐标"""
        self.dm.tap(device_index, x, y)
        self._delay()

    def move_left(self, device_index, duration=200):
        """向左移动（按住一段时间）"""
        # 按住左键
        self.dm.swipe(device_index, 100, 300, 100, 300, duration)
        self._delay()

    def move_right(self, device_index, duration=200):
        """向右移动"""
        self.dm.swipe(device_index, 600, 300, 600, 300, duration)
        self._delay()

    def jump(self, device_index):
        """跳跃"""
        # 向上滑动模拟跳跃
        self.dm.swipe(device_index, 400, 400, 400, 200, 150)
        self._delay()

    def attack(self, device_index):
        """普通攻击"""
        # 按攻击键
        self.dm.key(device_index, self.KEY_ENTER)  # 假设Enter是攻击
        self._delay()

    def pickup(self, device_index):
        """捡物"""
        self.dm.key(device_index, 66)  # 按键
        self._delay()

    def sit(self, device_index):
        """坐下休息"""
        self.dm.key(device_index, 74)  #坐下键
        self._delay()

    def use_skill(self, device_index, skill_slot):
        """使用技能（数字键1-9）"""
        # 技能快捷键
        key_map = {
            1: 8,   # 1 -> Keycode 8
            2: 9,
            3: 10,
            4: 11,
            5: 12,
            6: 13,
            7: 14,
            8: 15,
            9: 16,
        }
        if skill_slot in key_map:
            self.dm.key(device_index, key_map[skill_slot])
        self._delay()

    def heal(self, device_index):
        """治疗（牧师）"""
        self.use_skill(device_index, 2)
        self._delay()

    def buff(self, device_index):
        """加Buff（牧师）"""
        self.use_skill(device_index, 1)
        self._delay()

    def back(self, device_index):
        """返回"""
        self.dm.press_back(device_index)
        self._delay()

    def combo_attack_right(self, device_index, times=3):
        """组合攻击：向右移动并攻击"""
        for _ in range(times):
            self.dm.swipe(device_index, 400, 300, 500, 300, 200)  # 右移+攻击
            time.sleep(0.1)

    def combo_attack_left(self, device_index, times=3):
        """组合攻击：向左移动并攻击"""
        for _ in range(times):
            self.dm.swipe(device_index, 400, 300, 300, 300, 200)  # 左移+攻击
            time.sleep(0.1)

    def random_walk(self, device_index):
        """随机漫步（防封）"""
        actions = [
            lambda: self.dm.swipe(device_index, 400, 300, 300, 300, 300),
            lambda: self.dm.swipe(device_index, 400, 300, 500, 300, 300),
            lambda: self.dm.swipe(device_index, 400, 300, 400, 200, 200),
        ]
        random.choice(actions)()
        self._delay()


class AutoFarmController:
    """
    自动刷怪控制器
    整合移动、攻击、捡物
    """

    def __init__(self, device_manager):
        self.dm = device_manager
        self.keys = KeyController(device_manager)
        self.sc = None  # 需要外部设置

    def set_screen_capture(self, sc):
        """设置屏幕捕获器"""
        self.sc = sc

    def auto_farm_loop(self, device_index, monster_templates):
        """自动刷怪循环"""
        if not self.sc:
            raise ValueError("需要先设置ScreenCapture")

        idle_count = 0
        max_idle = 10

        while True:
            # 截图
            img = self.sc.capture(device_index)

            # 检测玩家
            player_found, player_pos, _ = self.sc.detect_player(img)
            if not player_found:
                print("⚠️ 未检测到玩家")
                time.sleep(1)
                continue

            # 检测怪物
            monsters = self.sc.detect_monsters(img, monster_templates)

            if monsters:
                idle_count = 0
                nearest = monsters[0]
                monster_pos = nearest[0]

                print(f"🎯 发现怪物在 {monster_pos}")

                # 接近怪物
                dx = monster_pos[0] - player_pos[0]
                if dx < -30:
                    self.keys.move_right(device_index, 300)
                elif dx > 30:
                    self.keys.move_left(device_index, 300)

                # 攻击
                self.keys.attack(device_index)

                # 捡物
                items = self.sc.detect_items(img)
                if items:
                    self.keys.pickup(device_index)

            else:
                idle_count += 1
                if idle_count > max_idle:
                    print("😴 无怪物，随机移动...")
                    self.keys.random_walk(device_index)
                    idle_count = 0

            time.sleep(0.2)
