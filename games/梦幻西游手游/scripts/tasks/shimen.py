"""
师门任务模块 v2.0
完整流程：找师父 -> 接任务 -> 识别任务类型 -> 执行 -> 交任务
"""

import time
import random
from pathlib import Path


class ShimenTask:
    """
    师门任务自动化

    游戏内流程：
    1. 点击小地图打开地图
    2. 选择师门师父位置，自动寻路
    3. 与师父对话，点击"师门"接任务
    4. 查看任务描述，识别任务类型
    5. 执行任务（送货/抓怪/战斗/采购）
    6. 回去找师父交任务
    7. 领取奖励
    """

    # 师门师父的大致位置（游戏内坐标，需要校准）
    MASTER_POS = (150, 200)

    # 小地图位置（游戏内坐标）
    MINIMAP_POS = (50, 50)

    # 师门按钮在对话框中的位置（相对坐标）
    SHIMEN_BTN_OFFSET = (0, 50)

    def __init__(self, dm, sc, cc, max_rounds=20):
        self.dm = dm
        self.sc = sc
        self.cc = cc
        self.max_rounds = max_rounds
        self.assets_dir = Path(__file__).parent.parent / "assets" / "shimen"

        # 速度模式
        self.cc.set_speed_mode("fast")

        # 任务状态
        self.current_task = None
        self.task_completed = 0

    def run(self, device_index):
        """执行师门任务主循环"""
        print(f"[设备{device_index}] 🚀 开始师门任务 (目标{self.max_rounds}轮)")

        for round_num in range(1, self.max_rounds + 1):
            self.task_completed = round_num - 1
            print(f"\n[设备{device_index}] ===== 第{round_num}/{self.max_rounds}轮 =====")

            try:
                # 确保在主界面
                self._ensure_main_ui(device_index)

                # 1. 打开地图，找师父
                print(f"[设备{device_index}] 📍 步骤1: 前往师门师父")
                if not self._go_to_master(device_index):
                    print(f"[设备{device_index}] ⚠️ 无法到达师父位置，尝试其他方式")
                    continue

                # 2. 与师父对话
                print(f"[设备{device_index}] 💬 步骤2: 与师父对话")
                self._talk_to_master(device_index)

                # 3. 接受师门任务
                print(f"[设备{device_index}] 📋 步骤3: 接受师门任务")
                if not self._accept_task(device_index):
                    print(f"[设备{device_index}] ⚠️ 任务接受失败")
                    self._dismiss_dialog(device_index)
                    continue

                # 4. 识别任务类型
                print(f"[设备{device_index}] 🔍 步骤4: 识别任务类型")
                task_type = self._identify_task_type(device_index)
                print(f"[设备{device_index}]    任务类型: {task_type}")

                # 5. 执行任务
                print(f"[设备{device_index}] 🎮 步骤5: 执行任务 ({task_type})")
                success = self._execute_task(device_index, task_type)
                if not success:
                    print(f"[设备{device_index}] ⚠️ 任务执行遇到问题")
                    self._recover_and_retry(device_index)
                    continue

                # 6. 回去交任务
                print(f"[设备{device_index}] 🏠 步骤6: 回去交任务")
                self._return_to_master(device_index)

                # 7. 交任务领奖励
                print(f"[设备{device_index}] 🎁 步骤7: 交任务领奖励")
                self._turn_in_task(device_index)

                print(f"[设备{device_index}] ✅ 第{round_num}轮完成")

                # 每完成一轮随机休息
                self.cc.antiban.random_idle()

            except Exception as e:
                print(f"[设备{device_index}] ❌ 第{round_num}轮异常: {e}")
                import traceback
                traceback.print_exc()
                self._emergency_recover(device_index)

        print(f"[设备{device_index}] ✅✅ 全部{self.max_rounds}轮师门任务完成!")

    def _ensure_main_ui(self, device_index):
        """确保在主界面（不是战斗、不是对话框等）"""
        for _ in range(3):
            # 如果有对话框，先关闭
            self._dismiss_dialog(device_index)

            # 检查是否在主界面（通过检测小地图等元素）
            img = self.sc.capture(device_index)

            # 尝试找小地图
            found, pos = self._find_minimap(img)
            if found:
                print(f"[设备{device_index}]    确认在主界面，小地图位置: {pos}")
                return True

            # 如果没找到小地图，可能在战斗或特殊界面
            print(f"[设备{device_index}]    未检测到主界面，等待...")
            time.sleep(1)

        return False

    def _find_minimap(self, screenshot):
        """在小地图位置检测小地图"""
        # 小地图通常在左上角，这里用几何特征检测
        # 实际上应该用模板匹配，但素材未准备好
        # 这里返回一个假设位置，后续要替换成真实模板匹配

        # 假设小地图在 (50, 50) 附近有明显的边缘
        h, w = screenshot.shape[:2]

        # 检查左上角区域是否有UI元素
        roi = screenshot[30:100, 30:100]

        # 计算这个区域的方差，如果有大面积同色区域可能是UI
        import numpy as np
        var = np.var(roi)

        # 简单判断：有内容而非纯色
        if var > 100:
            return True, (50, 50)

        return False, None

    def _go_to_master(self, device_index):
        """前往师门师父位置"""
        # 方法1: 直接点击小地图上的师父图标（如果有）
        # 方法2: 点击小地图打开大地图，选择师门师父
        # 方法3: 使用自动寻路

        print(f"[设备{device_index}]    打开地图...")
        # 点击小地图
        self.cc.tap_game(device_index, *self.MINIMAP_POS)
        time.sleep(1)

        # 等待地图打开，检测地图界面
        for attempt in range(5):
            img = self.sc.capture(device_index)
            if self._is_map_open(img):
                print(f"[设备{device_index}]    地图已打开")
                break
            time.sleep(0.5)
        else:
            print(f"[设备{device_index}]    地图未能打开")
            return False

        # 在地图上找师门师父位置并点击
        # 这里需要师父在大地图上的图标模板
        found = self._find_master_on_map(device_index)
        if found:
            print(f"[设备{device_index}]    已选中师父，开始自动寻路")
            time.sleep(0.5)
            # 点击"自动寻路"按钮
            self.cc.tap_game(device_index, 163, 400)  # 假设的自动寻路按钮位置
            return True

        # 如果找不到师父，尝试直接飞过去的快捷方式
        print(f"[设备{device_index}]    未找到师父图标，使用快捷方式")
        return self._quick_nav_to_master(device_index)

    def _is_map_open(self, screenshot):
        """检测地图是否打开"""
        # 地图打开后会有特定的UI元素，如"地图"标题或关闭按钮
        # 这里需要模板匹配，后续替换
        return False  # 暂时返回False，使用快捷方式

    def _find_master_on_map(self, device_index):
        """在大地图上找到师门师父"""
        # 模板匹配：找师父图标
        # 待实现：需要师父在大地图上的图标截图
        return False

    def _quick_nav_to_master(self, device_index):
        """快速导航到师父（师门快捷入口）"""
        # 游戏内有师门快捷入口，可以直接飞过去
        # 常见位置：右上角活动 -> 日常 -> 师门
        # 或者帮派图标 -> 师门

        print(f"[设备{device_index}]    尝试通过快捷入口前往")

        # 方法：从主界面直接点击"师门"快捷方式
        # 这个位置因服务器而异，需要实际截图
        # 常见方案：点击"日常"按钮

        # 假设日常按钮在右上角
        self.cc.tap_game(device_index, 290, 50)  # 右上角
        time.sleep(1)

        # 再在日常列表中找师门
        # 待实现：日常列表模板匹配

        return False

    def _talk_to_master(self, device_index):
        """与师父对话"""
        # 检测对话框是否出现
        for _ in range(5):
            img = self.sc.capture(device_index)
            if self._is_dialog_open(img):
                print(f"[设备{device_index}]    对话框已出现")
                return True
            time.sleep(0.5)

        # 如果对话框没出现，尝试点击师父NPC
        print(f"[设备{device_index}]    对话框未出现，尝试点击NPC")
        self.cc.tap_game(device_index, *self.MASTER_POS)
        time.sleep(1)

        for _ in range(5):
            img = self.sc.capture(device_index)
            if self._is_dialog_open(img):
                return True
            time.sleep(0.5)

        return False

    def _is_dialog_open(self, screenshot):
        """检测对话框是否打开"""
        # 对话框有特定的视觉特征
        # 待实现：模板匹配
        return False

    def _accept_task(self, device_index):
        """接受师门任务"""
        # 点击"师门"按钮接任务
        # 这个按钮在对话框中，需要相对位置

        print(f"[设备{device_index}]    寻找师门按钮...")

        # 尝试点击师门按钮（需要实际校准位置）
        # 位置可能在对话框中央下方
        shimen_btn_x = 163  # 居中
        shimen_btn_y = 350  # 对话框下半部分

        # 先尝试直接点击"师门"文字
        self.cc.tap_game(device_index, shimen_btn_x, shimen_btn_y)
        time.sleep(0.5)

        # 检测任务是否接受（观察是否有任务追踪）
        for _ in range(5):
            img = self.sc.capture(device_index)
            if self._has_task_tracker(img):
                print(f"[设备{device_index}]    任务已接受")
                return True
            time.sleep(0.5)

        # 如果没反应，尝试其他位置
        # 可能在对话框右侧或不同高度
        for offset_y in [-20, 0, 20, 40]:
            self.cc.tap_game(device_index, shimen_btn_x + 50, shimen_btn_y + offset_y)
            time.sleep(0.5)
            img = self.sc.capture(device_index)
            if self._has_task_tracker(img):
                return True

        return False

    def _has_task_tracker(self, screenshot):
        """检测是否有任务追踪（任务追踪栏是否有师门任务）"""
        # 任务追踪栏通常在右侧
        # 待实现：模板匹配
        return False

    def _identify_task_type(self, device_index):
        """识别任务类型"""
        # 读取任务描述文字
        # 游戏内任务描述会显示任务类型和目标

        # 方法1: OCR识别任务追踪栏的文字
        # 方法2: 匹配任务类型图标
        # 方法3: 读取任务对话框文字

        img = self.sc.capture(device_index)

        # 尝试读取任务描述区域（屏幕中央或任务追踪栏）
        task_desc_area = img[300:400, 200:450]  # 假设区域

        # TODO: OCR识别
        # 这里暂时返回随机类型用于测试
        task_types = ["送货", "抓怪", "战斗", "采购"]
        detected = random.choice(task_types)

        return detected

    def _execute_task(self, device_index, task_type):
        """执行任务"""
        print(f"[设备{device_index}]    开始执行: {task_type}")

        if task_type == "送货":
            return self._do_delivery(device_index)
        elif task_type == "抓怪":
            return self._do_catch(device_index)
        elif task_type == "战斗":
            return self._do_battle(device_index)
        elif task_type == "采购":
            return self._do_purchase(device_index)
        else:
            print(f"[设备{device_index}]    未知任务类型: {task_type}")
            return False

    def _do_delivery(self, device_index):
        """送货任务"""
        print(f"[设备{device_index}]    送货任务: 自动寻路到目的地")

        # 1. 点击任务追踪栏中的目标
        self.cc.tap_game(device_index, 300, 350)  # 任务追踪栏位置
        time.sleep(0.5)

        # 2. 等待自动寻路
        self._wait_for_autowalk(device_index)

        # 3. 到达后与NPC对话
        self._talk_and_interact(device_index, "送货交付")

        return True

    def _do_catch(self, device_index):
        """抓怪任务"""
        print(f"[设备{device_index}]    抓怪任务: 寻路到怪物位置")

        # 1. 点击任务追踪栏中的目标
        self.cc.tap_game(device_index, 300, 350)
        time.sleep(0.5)

        # 2. 等待自动寻路
        self._wait_for_autowalk(device_index)

        # 3. 遇到怪物，进入战斗
        print(f"[设备{device_index}]    进入战斗")
        self._auto_battle(device_index)

        # 4. 战斗后可能需要捕捉
        # 检测是否有捕捉选项
        self._try_catch_if_needed(device_index)

        return True

    def _do_battle(self, device_index):
        """战斗任务"""
        print(f"[设备{device_index}]    战斗任务")

        # 点击任务追踪栏
        self.cc.tap_game(device_index, 300, 350)
        time.sleep(0.5)

        # 等待自动寻路
        self._wait_for_autowalk(device_index)

        # 自动战斗
        self._auto_battle(device_index)

        return True

    def _do_purchase(self, device_index):
        """采购任务"""
        print(f"[设备{device_index}]    采购任务: 前往商店购买")

        # 1. 打开地图
        self.cc.tap_game(device_index, *self.MINIMAP_POS)
        time.sleep(1)

        # 2. 找商店位置（杂货店或指定NPC）
        # 3. 打开商店界面
        # 4. 购买指定物品

        # TODO: 具体实现需要截图素材

        return True

    def _wait_for_autowalk(self, device_index, timeout=30):
        """等待自动寻路完成"""
        print(f"[设备{device_index}]    等待自动寻路...")
        start = time.time()

        while time.time() - start < timeout:
            img = self.sc.capture(device_index)

            # 检测是否到达（任务追踪栏显示"已完成"）
            # 或者检测小地图上的定位点

            time.sleep(1)

            # 简单实现：等待固定时间
            # 实际上应该检测UI状态
            if time.time() - start > 10:
                print(f"[设备{device_index}]    寻路超时，假设到达")
                break

        return True

    def _talk_and_interact(self, device_index, action):
        """与NPC对话并执行动作"""
        # 检测对话框
        for _ in range(5):
            img = self.sc.capture(device_index)
            if self._is_dialog_open(img):
                break
            time.sleep(0.5)

        # 点击执行动作（如"交付"、"对话"等）
        # 位置需要根据实际UI调整
        self.cc.tap_game(device_index, 163, 350)
        time.sleep(0.5)

    def _auto_battle(self, device_index):
        """自动战斗"""
        print(f"[设备{device_index}]    开始自动战斗")

        # 检测战斗UI
        for _ in range(10):
            img = self.sc.capture(device_index)
            if self._is_in_battle(img):
                break
            time.sleep(0.5)

        # 设置自动战斗（如果有此选项）
        # 点击"自动"按钮
        self.cc.tap_game(device_index, 280, 400)  # 假设的自动按钮位置
        time.sleep(0.5)

        # 等待战斗完成（检测血条、战斗UI消失等）
        for _ in range(60):  # 最多60秒
            img = self.sc.capture(device_index)
            if not self._is_in_battle(img):
                print(f"[设备{device_index}]    战斗结束")
                return True
            time.sleep(1)

        print(f"[设备{device_index}]    战斗超时")
        return False

    def _is_in_battle(self, screenshot):
        """检测是否在战斗状态"""
        # 战斗状态有特定的UI：血条、行动按钮、敌人血条等
        # 待实现：模板匹配或特征检测
        return False

    def _try_catch_if_needed(self, device_index):
        """如果需要捕捉，尝试捕捉"""
        # 检测是否有"捕捉"选项
        for _ in range(5):
            img = self.sc.capture(device_index)
            # 检测捕捉按钮

            time.sleep(0.5)

        # 点击捕捉
        # self.cc.tap_game(device_index,捕捉按钮位置)

    def _return_to_master(self, device_index):
        """返回师门师父"""
        print(f"[设备{device_index}]    返回师门师父")

        # 方法1: 使用任务追踪栏点击师父
        # 方法2: 打开地图，选择师门师父
        # 方法3: 使用帮派图标快捷入口

        # 关闭可能存在的对话框
        self._dismiss_dialog(device_index)
        time.sleep(0.5)

        # 点击任务追踪栏的师父
        self.cc.tap_game(device_index, 300, 200)  # 师父在任务追踪栏中的位置
        time.sleep(0.5)

        # 等待自动寻路
        self._wait_for_autowalk(device_index)

    def _turn_in_task(self, device_index):
        """交任务"""
        # 1. 与师父对话
        self._talk_to_master(device_index)
        time.sleep(0.5)

        # 2. 点击"完成"或"交任务"按钮
        self.cc.tap_game(device_index, 163, 350)
        time.sleep(1)

        # 3. 领取奖励（如果有确认按钮）
        img = self.sc.capture(device_index)
        if self._is_reward_dialog(img):
            self.cc.tap_game(device_index, 163, 350)  # 领取奖励
            time.sleep(0.5)

        # 4. 关闭对话框
        self._dismiss_dialog(device_index)

    def _is_reward_dialog(self, screenshot):
        """检测奖励对话框"""
        # 待实现：模板匹配
        return False

    def _dismiss_dialog(self, device_index):
        """关闭对话框"""
        # 方法1: 点返回键
        # 方法2: 点击对话框外区域
        # 方法3: 点击"X"关闭按钮

        self.cc.back(device_index)
        time.sleep(0.3)

        # 如果没反应，尝试点击屏幕边缘关闭
        self.cc.tap_game(device_index, 20, 400)  # 左侧边缘
        time.sleep(0.3)

    def _recover_and_retry(self, device_index):
        """恢复并重试当前轮"""
        print(f"[设备{device_index}]    执行恢复...")
        self._emergency_recover(device_index)
        time.sleep(2)

    def _emergency_recover(self, device_index):
        """紧急恢复：回到主界面"""
        print(f"[设备{device_index}]    紧急恢复: 返回主界面")

        # 连续按返回键
        for _ in range(5):
            self.cc.back(device_index)
            time.sleep(0.3)

        # 如果有弹窗没关闭，再按几次
        for _ in range(3):
            self.cc.back(device_index)
            time.sleep(0.2)

        # 点击小地图确认在主界面
        time.sleep(1)


# 快捷测试
if __name__ == "__main__":
    print("师门任务模块 v2.0")
    print("需要连接设备后才能运行")
    print("请使用 main.py 启动完整脚本")
