"""
自动升级脚本 - Artale 阿尔泰服
基于 OpenCV 模板匹配 + 键盘模拟
"""

import time
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.screen_capture import ScreenCapture
from core.keyboard_controller import KeyboardController
from config import SUPPORTED_MAPS, PRIEST, ANTIBAN


class AutoLevelUp:
    """Artale 自动升级脚本"""

    def __init__(self, character_class="priest"):
        self.sc = ScreenCapture()
        self.kc = KeyboardController()
        self.character_class = character_class
        self.is_running = False

    def start(self, map_name, monster_names):
        """
        开始自动升级
        map_name: 地图名称 (如 "north_forst_training_ground_2")
        monster_names: 怪物类型列表 (如 ["green_mushroom", "spike_mushroom"])
        """
        if map_name not in SUPPORTED_MAPS:
            print(f"❌ 不支持的地图: {map_name}")
            print(f"支持的地图: {list(SUPPORTED_MAPS.keys())}")
            return

        map_info = SUPPORTED_MAPS[map_name]
        print(f"🚀 开始自动升级")
        print(f"   地图: {map_info['name']}")
        print(f"   怪物: {monster_names}")
        print(f"   职业: {self.character_class}")

        self.is_running = True
        try:
            self._auto_farm_loop(map_name, monster_names)
        except KeyboardInterrupt:
            print("\n⏹️ 停止自动升级")
            self.is_running = False

    def _auto_farm_loop(self, map_name, monster_names):
        """自动刷怪循环"""
        # 构建怪物模板路径
        monster_templates = [
            f"assets/monsters/{name}.png" for name in monster_names
        ]

        idle_counter = 0
        max_idle = 10  # 连续未发现怪物次数上限

        while self.is_running:
            # 1. 截图
            screen = self.sc.capture_window()

            # 2. 检测玩家位置
            player_found, player_pos, _ = self.sc.find_player(screen)

            # 3. 检测怪物
            monsters = self.sc.find_monsters(screen, monster_templates)

            if monsters:
                idle_counter = 0
                nearest = monsters[0]  # 最近的怪物
                monster_pos = nearest[0]
                monster_type = nearest[1]

                print(f"🎯 发现 {monster_type} 在 {monster_pos}")

                # 4. 移动到怪物位置并攻击
                self._approach_and_attack(monster_pos, player_pos)

                # 5. 捡物
                self._pickup_items()

                # 6. 牧师辅助
                if self.character_class == "priest":
                    self._priest_support()

            else:
                idle_counter += 1
                if idle_counter > max_idle:
                    print("😴 没有发现怪物，随机移动...")
                    self.kc.random_move()
                    idle_counter = 0
                else:
                    # 原地等待一下
                    time.sleep(0.5)

            # 随机延迟
            time.sleep(random.uniform(0.1, 0.3))

    def _approach_and_attack(self, monster_pos, player_pos):
        """接近怪物并攻击"""
        if not player_pos:
            return

        dx = monster_pos[0] - player_pos[0]

        # 判断方向并移动
        if dx < -50:  # 怪物在左边
            self.kc.move_left()
        elif dx > 50:  # 怪物在右边
            self.kc.move_right()

        # 攻击
        self.kc.attack()

    def _pickup_items(self):
        """捡物品"""
        self.kc.pickup()

    def _priest_support(self):
        """牧师辅助技能"""
        # 检测血量
        if self.sc.is_hp_low(None):
            self.kc.priest_heal()

        # 定期加Buff
        # (实际需要判断Buff持续时间)

    def stop(self):
        """停止脚本"""
        self.is_running = False
        print("⏹️ 正在停止...")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Artale 自动升级脚本")
    parser.add_argument("--map", required=True, help="地图名称")
    parser.add_argument("--monsters", required=True, help="怪物类型，用逗号分隔")
    parser.add_argument("--class", dest="char_class", default="priest", help="职业")

    args = parser.parse_args()
    monster_list = args.monsters.split(",")

    bot = AutoLevelUp(character_class=args.char_class)
    bot.start(args.map, monster_list)


if __name__ == "__main__":
    main()
