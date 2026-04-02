"""
师门任务模块
"""

import time
import random
from core.screen_capture import ScreenCapture
from core.click_controller import ClickController


class ShimenTask:
    """
    师门任务
    流程: 找师父 -> 接任务 -> 完成 -> 交任务 -> 循环
    """

    # 任务类型
    TASK_TYPES = ["送货", "抓怪", "战斗", "采购"]

    def __init__(self, device_manager, screen_capture, click_controller, max_rounds=20):
        self.dm = device_manager
        self.sc = screen_capture
        self.cc = click_controller
        self.max_rounds = max_rounds

        # 资源路径（后续需要截图替换）
        self.assets_dir = "../assets/shimen/"

    def run(self, device_index):
        """执行师门任务"""
        print(f"[设备{device_index}] 🚀 开始师门任务 (目标{self.max_rounds}轮)")

        for round_num in range(1, self.max_rounds + 1):
            print(f"[设备{device_index}] 第{round_num}/{self.max_rounds}轮")

            try:
                # 1. 找到并点击师门师父
                self._go_to_master(device_index)

                # 2. 点击"师门"按钮接任务
                self._accept_task(device_index)

                # 3. 判断任务类型并完成
                task_type = self._identify_task_type(device_index)
                self._complete_task(device_index, task_type)

                # 4. 回去交任务
                self._return_and_turn_in(device_index)

                # 随机休息一下
                self.cc.antiban.random_idle()

            except Exception as e:
                print(f"[设备{device_index}] ❌ 第{round_num}轮出错: {e}")
                self._recover(device_index)

        print(f"[设备{device_index}] ✅ 师门任务完成")

    def _go_to_master(self, device_index):
        """找到师门师父并对话"""
        # TODO: 需要实际截图替换
        # 方案: 点击小地图 -> 选择师门师父 -> 自动寻路
        pass

    def _accept_task(self, device_index):
        """点击"师门"接任务"""
        # TODO: 图像识别"师门"按钮
        pass

    def _identify_task_type(self, device_index):
        """识别任务类型: 送货/抓怪/战斗/采购"""
        # TODO: 读取任务描述文字，OCR识别
        return random.choice(self.TASK_TYPES)

    def _complete_task(self, device_index, task_type):
        """完成任务"""
        if task_type == "送货":
            self._do_delivery(device_index)
        elif task_type == "抓怪":
            self._do_catch(device_index)
        elif task_type == "战斗":
            self._do_battle(device_index)
        elif task_type == "采购":
            self._do_purchase(device_index)

    def _do_delivery(self, device_index):
        """送货任务"""
        # TODO: 自动寻路到目的地，点击NPC对话
        pass

    def _do_catch(self, device_index):
        """抓怪任务"""
        # TODO: 自动寻路到怪物处，战斗后捕捉
        pass

    def _do_battle(self, device_index):
        """战斗任务"""
        # TODO: 自动战斗，设置自动技能
        pass

    def _do_purchase(self, device_index):
        """采购任务"""
        # TODO: 购买指定物品
        pass

    def _return_and_turn_in(self, device_index):
        """回去交任务"""
        # TODO: 自动寻路回师门师父，交任务
        pass

    def _recover(self, device_index):
        """出错恢复"""
        # 返回主城，关闭弹窗，重新开始
        self.cc.back(device_index)
        time.sleep(2)
