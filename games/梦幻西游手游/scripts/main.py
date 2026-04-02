"""
梦幻西游手游脚本 - 主入口
"""

import time
import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from core.device_manager import DeviceManager
from core.screen_capture import ScreenCapture
from core.click_controller import ClickController
from tasks.shimen import ShimenTask
from config.settings import MUMU_BASE_PORT, DEVICE_COUNT


def main():
    print("=" * 50)
    print("梦幻西游手游脚本")
    print("=" * 50)

    # 1. 连接设备
    print("\n📱 连接模拟器设备...")
    dm = DeviceManager(base_port=MUMU_BASE_PORT, device_count=DEVICE_COUNT)

    if dm.connected_count == 0:
        print("❌ 没有找到任何模拟器实例，请检查MuMu模拟器是否启动")
        return

    print(f"✅ 成功连接 {dm.connected_count} 个设备")

    # 2. 初始化模块
    sc = ScreenCapture(dm)
    cc = ClickController(dm)

    # 3. 等待游戏加载
    print("\n⏳ 等待游戏加载...")
    time.sleep(5)

    # 4. 测试截图（调试用）
    print("\n🧪 测试截图...")
    try:
        for i in range(dm.connected_count):
            img = sc.capture(i)
            print(f"  设备{i+1}: 截图成功 {img.shape}")
    except Exception as e:
        print(f"  ❌ 截图失败: {e}")
        print("  请检查ADB连接是否正常")

    # 5. 启动师门任务
    print("\n🎯 启动师门任务...")
    for i in range(dm.connected_count):
        task = ShimenTask(dm, sc, cc, max_rounds=20)
        task.run(i)

    print("\n✅ 全部任务执行完成")


if __name__ == "__main__":
    main()
