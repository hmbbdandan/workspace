#!/usr/bin/env python3
"""
诊断工具 - 帮你确定截图和坐标问题
运行方式: python diagnose.py
"""

import sys
import subprocess
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

def main():
    print("=" * 50)
    print("梦幻西游手游 - 诊断工具")
    print("=" * 50)

    # 1. 测试ADB连接
    print("\n📱 1. 测试ADB连接...")
    try:
        from core.device_manager import DeviceManager
        from core.screen_capture import ScreenCapture
        dm = DeviceManager(base_port=16384, device_count=5)
        if dm.connected_count > 0:
            print(f"   ✅ ADB连接正常，{dm.connected_count}个设备已连接")
        else:
            print("   ❌ 没有ADB设备")
            print("   请确保MuMu模拟器已启动并开启ADB")
    except Exception as e:
        print(f"   ❌ ADB连接失败: {e}")
        return

    # 2. 测试截图
    print("\n🖼️  2. 测试截图...")
    sc = ScreenCapture(dm)
    try:
        img = sc.capture(0)
        print(f"   ✅ 截图成功: {img.shape[1]}x{img.shape[0]}")
    except Exception as e:
        print(f"   ❌ 截图失败: {e}")
        return

    # 3. 测试Mac屏幕截图
    print("\n🖥️  3. 测试Mac屏幕截图...")
    for d in ['2', '1']:
        try:
            result = subprocess.run(
                ['/usr/sbin/screencapture', '-x', '-D', d, '/tmp/mac_screen.png'],
                capture_output=True, timeout=5
            )
            import cv2
            img = cv2.imread('/tmp/mac_screen.png')
            if img is not None:
                print(f"   ✅ 屏幕D{d}: {img.shape[1]}x{img.shape[0]}")
            else:
                print(f"   ⚠️ 屏幕D{d}: 无法读取")
        except Exception as e:
            print(f"   ⚠️ 屏幕D{d}: {e}")

    # 4. 坐标测试
    print("\n🎯 4. 坐标点击测试...")
    print("   正在执行测试点击...")
    from core.click_controller import ClickController
    cc = ClickController(dm)
    
    # 读取当前状态
    status = cc.status()
    print(f"   当前速度模式: {status['speed_mode']}")
    print(f"   当前坐标模式: {status['coord_mode']}")
    print(f"   游戏窗口: {status['window_info']['game_area']}")

    # 5. 速度测试
    print("\n⚡ 5. 速度模式对比...")
    print("   10次点击耗时对比:")
    
    for mode in ['normal', 'fast', 'turbo']:
        cc.set_speed_mode(mode)
        start = time.time()
        for _ in range(10):
            cc.tap_fixed(0, 100, 100)
        elapsed = time.time() - start
        print(f"   - {mode}: {elapsed:.2f}秒")

    print("\n" + "=" * 50)
    print("诊断完成")
    print("=" * 50)
    print("\n💡 建议:")
    print("1. 如果要加快速度，使用: cc.set_speed_mode('fast') 或 'turbo'")
    print("2. 如果游戏窗口位置变了，更新 CoordinateManager 的 GAME_WINDOW_OFFSET_*")
    print("3. 提供游戏截图素材到 assets/shimen/ 目录以启用图像识别")


if __name__ == "__main__":
    main()