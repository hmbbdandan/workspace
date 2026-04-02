"""
设备管理器 - 管理多个MuMu模拟器实例
"""

import subprocess
import socket
import time
from ppadb.client import Client as AdbClient


class DeviceManager:
    """管理多个模拟器实例"""

    def __init__(self, base_port=16384, device_count=5):
        self.base_port = base_port
        self.device_count = device_count
        self.devices = []
        self._connect_all()

    def _connect_all(self):
        """连接所有模拟器实例"""
        # 连接到MuMu的ADB服务器
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
        """获取指定实例的截图"""
        if device_index >= len(self.devices):
            raise IndexError(f"设备索引 {device_index} 超出范围")
        return self.devices[device_index].screencap()

    def tap(self, device_index, x, y):
        """点击指定实例的坐标"""
        if device_index >= len(self.devices):
            raise IndexError(f"设备索引 {device_index} 超出范围")
        self.devices[device_index].shell(f"input tap {x} {y}")

    def swipe(self, device_index, x1, y1, x2, y2, duration=300):
        """滑动指定实例"""
        if device_index >= len(self.devices):
            raise IndexError(f"设备索引 {device_index} 超出范围")
        self.devices[device_index].shell(
            f"input swipe {x1} {y1} {x2} {y2} {duration}"
        )

    def press_back(self, device_index):
        """按返回键"""
        if device_index >= len(self.devices):
            raise IndexError(f"设备索引 {device_index} 超出范围")
        self.devices[device_index].shell("input keyevent KEYCODE_BACK")

    def press_home(self, device_index):
        """按Home键"""
        if device_index >= len(self.devices):
            raise IndexError(f"设备索引 {device_index} 超出范围")
        self.devices[device_index].shell("input keyevent KEYCODE_HOME")

    def get_prop(self, device_index, prop_name):
        """获取设备属性"""
        if device_index >= len(self.devices):
            raise IndexError(f"设备索引 {device_index} 超出范围")
        return self.devices[device_index].shell(f"getprop {prop_name}").strip()

    def restart_app(self, device_index, package_name):
        """重启应用"""
        if device_index >= len(self.devices):
            raise IndexError(f"设备索引 {device_index} 超出范围")
        device = self.devices[device_index]
        device.shell(f"am force-stop {package_name}")
        time.sleep(1)
        device.shell(f"am start -n {package_name}/.App")

    @property
    def connected_count(self):
        """返回已连接的设备数"""
        return len(self.devices)
