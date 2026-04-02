"""
防封模块 - 随机化操作，防检测
支持速度模式切换
"""

import random
import time


class AntiBan:
    """防封机制：随机延迟、随机操作"""

    # 速度模式配置
    SPEED_MODES = {
        "normal": {
            "min_click_delay": 0.8,
            "max_click_delay": 2.5,
            "min_action_gap": 3.0,
            "max_idle_time": 15.0,
            "random_offset_range": 5,
        },
        "fast": {
            "min_click_delay": 0.2,
            "max_click_delay": 0.5,
            "min_action_gap": 0.5,
            "max_idle_time": 3.0,
            "random_offset_range": 3,
        },
        "turbo": {
            "min_click_delay": 0.1,
            "max_click_delay": 0.2,
            "min_action_gap": 0.2,
            "max_idle_time": 1.0,
            "random_offset_range": 2,
        },
    }

    def __init__(self, speed_mode="normal"):
        self.speed_mode = speed_mode
        self.cfg = self.SPEED_MODES[speed_mode]

    def set_speed_mode(self, mode):
        """切换速度模式: normal / fast / turbo"""
        if mode not in self.SPEED_MODES:
            raise ValueError(f"Unknown speed mode: {mode}")
        self.speed_mode = mode
        self.cfg = self.SPEED_MODES[mode]
        print(f"  ⚡ 速度模式切换: {mode}")

    def click_delay(self):
        """点击之间的随机延迟"""
        delay = random.uniform(self.cfg["min_click_delay"], self.cfg["max_click_delay"])
        time.sleep(delay)

    def action_gap(self):
        """操作之间的间隔"""
        delay = random.uniform(
            self.cfg["min_action_gap"],
            self.cfg["min_action_gap"] * 2  # 默认最大是最小的2倍
        )
        time.sleep(delay)

    def random_idle(self):
        """随机发呆"""
        delay = random.uniform(0, self.cfg["max_idle_time"])
        if delay > 2:  # 只有超过2秒才提示
            print(f"    💤 发呆 {delay:.1f}秒")
        time.sleep(delay)

    def random_swipe_offset(self, x1, y1, x2, y2, offset_range=None):
        """给滑动坐标加随机偏移，防固定轨迹"""
        if offset_range is None:
            offset_range = self.cfg["random_offset_range"]
        dx = random.randint(-offset_range, offset_range)
        dy = random.randint(-offset_range, offset_range)
        return (x1 + dx, y1 + dy, x2 + dx, y2 + dy)

    def random_click_offset(self, x, y, offset_range=None):
        """给点击坐标加随机偏移，防固定位置"""
        if offset_range is None:
            offset_range = self.cfg["random_offset_range"]
        dx = random.randint(-offset_range, offset_range)
        dy = random.randint(-offset_range, offset_range)
        return x + dx, y + dy

    def human_pattern(self, action_count=5):
        """模拟人类操作模式"""
        for _ in range(action_count):
            if random.random() < 0.3:
                self.random_idle()
            else:
                self.click_delay()

    def adaptive_delay(self, base_delay, risk_level="low"):
        """自适应延迟"""
        multipliers = {"low": 1.0, "medium": 1.5, "high": 2.5}
        mult = multipliers.get(risk_level, 1.0)
        delay = base_delay * mult * random.uniform(0.8, 1.2)
        time.sleep(delay)

    def status(self):
        """返回当前配置状态"""
        return {
            "mode": self.speed_mode,
            "click_delay": f"{self.cfg['min_click_delay']}-{self.cfg['max_click_delay']}s",
            "action_gap": f"{self.cfg['min_action_gap']}+s",
            "offset_range": self.cfg["random_offset_range"],
        }


# MuMu 模拟器配置
MUMU_BASE_PORT = 16384
DEVICE_COUNT = 5

# 模拟器窗口尺寸
EMULATOR_WIDTH = 960
EMULATOR_HEIGHT = 540

# 截图间隔
SCREENSHOT_INTERVAL = 0.5

# 防封配置（默认normal模式）
ANTIBAN = {
    "min_click_delay": 0.8,
    "max_click_delay": 2.5,
    "min_action_gap": 3.0,
    "max_idle_time": 15.0,
    "random_swipe": True,
}

# 图像识别配置
CV = {
    "threshold": 0.80,
    "wait_timeout": 30,
}