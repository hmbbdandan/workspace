"""
设备管理器 - Artale 冒险岛
支持通过ADB连接MuMu模拟器实例
"""

import subprocess
import time
from ppadb.client import Client as AdbClient


class DeviceManager:
    """管理多个模拟器实例的ADB连接"""

    def __init__(self, base_port=16384, device_count=1):
        """
        base_port: MuMu模拟器基础端口 (默认16384)
        device_count: 连接设备数量
        """
        self.base_port = base_port
        self.device_count = device_count
        self.devices = []
        self._connect_all()

    def _connect_all(self):
        """连接所有模拟器实例"""
        client = AdbClient(host="127.0.0.1", port=5037)

        for i in range(self.device_count):
            serial = f"127.0.0.1:{self.base_port + i}"
            try:
                device = client.device(serial)
                self.devices.append(device)
                print(f"✅ 实例{i+1} ({serial}) 已连接")
            except Exception as e:
                print(f"❌ 实例{i+1} ({serial}) 连接失败: {e}")

    def screenshot(self, device_index):
        """获取设备截图（原始字节）"""
        if device_index >= len(self.devices):
            raise IndexError(f"设备索引 {device_index} 超出范围")
        return self.devices[device_index].screencap()

    def tap(self, device_index, x, y):
        """点击坐标"""
        if device_index >= len(self.devices):
            raise IndexError(f"设备索引 {device_index} 超出范围")
        self.devices[device_index].shell(f"input tap {x} {y}")

    def swipe(self, device_index, x1, y1, x2, y2, duration=300):
        """滑动"""
        if device_index >= len(self.devices):
            raise IndexError(f"设备索引 {device_index} 超出范围")
        self.devices[device_index].shell(
            f"input swipe {x1} {y1} {x2} {y2} {duration}"
        )

    def key(self, device_index, keycode):
        """发送按键事件"""
        if device_index >= len(self.devices):
            raise IndexError(f"设备索引 {device_index} 超出范围")
        self.devices[device_index].shell(f"input keyevent {keycode}")

    def text(self, device_index, text):
        """输入文本"""
        if device_index >= len(self.devices):
            raise IndexError(f"设备索引 {device_index} 超出范围")
        # 需要将空格替换
        text = text.replace(" ", "%s")
        self.devices[device_index].shell(f"input text {text}")

    def press_back(self, device_index):
        """返回键"""
        self.key(device_index, 4)

    def press_home(self, device_index):
        """Home键"""
        self.key(device_index, 3)

    def press_enter(self, device_index):
        """确认键"""
        self.key(device_index, 66)

    def get_prop(self, device_index, prop_name):
        """获取设备属性"""
        if device_index >= len(self.devices):
            raise IndexError(f"设备索引 {device_index} 超出范围")
        return self.devices[device_index].shell(f"getprop {prop_name}").strip()

    @property
    def connected_count(self):
        """返回已连接的设备数"""
        return len(self.devices)


# MuMu模拟器配置
MUMU_BASE_PORT = 16384
DEVICE_COUNT = 1  # 默认单设备
