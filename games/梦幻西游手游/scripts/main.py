"""
梦幻西游手游脚本 - 主入口 v2.0
"""

import time
import sys
import argparse
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from core.device_manager import DeviceManager
from core.screen_capture import ScreenCapture
from core.click_controller import ClickController
from tasks.shimen import ShimenTask
from config.settings import MUMU_BASE_PORT, DEVICE_COUNT


def parse_args():
    """命令行参数解析"""
    parser = argparse.ArgumentParser(description="梦幻西游手游脚本")
    parser.add_argument("--device-count", type=int, default=DEVICE_COUNT,
                        help=f"模拟器实例数量 (默认{DEVICE_COUNT})")
    parser.add_argument("--port", type=int, default=MUMU_BASE_PORT,
                        help=f"ADB基础端口 (默认{MUMU_BASE_PORT})")
    parser.add_argument("--rounds", type=int, default=20,
                        help="师门任务循环次数 (默认20)")
    parser.add_argument("--speed", choices=["normal", "fast", "turbo"], default="fast",
                        help="速度模式 (默认fast)")
    parser.add_argument("--debug", action="store_true",
                        help="调试模式：显示更多信息")
    parser.add_argument("--test", action="store_true",
                        help="测试模式：不执行实际点击，只诊断")
    return parser.parse_args()


def main():
    print("=" * 50)
    print("梦幻西游手游脚本 v2.0")
    print("=" * 50)

    args = parse_args()

    if args.debug:
        print(f"\n📊 配置信息:")
        print(f"   设备数量: {args.device_count}")
        print(f"   ADB端口: {args.port}")
        print(f"   任务轮数: {args.rounds}")
        print(f"   速度模式: {args.speed}")
        print(f"   调试模式: {'开启' if args.debug else '关闭'}")
        print(f"   测试模式: {'开启' if args.test else '关闭'}")

    # 1. 连接设备
    print(f"\n📱 连接模拟器设备 (端口 {args.port})...")
    dm = DeviceManager(base_port=args.port, device_count=args.device_count)

    if dm.connected_count == 0:
        print("❌ 没有找到任何模拟器实例，请检查:")
        print("   1. MuMu模拟器是否启动")
        print("   2. ADB端口是否正确 (默认16384)")
        print("   3. 模拟器ADB是否开启")
        print()
        print("💡 手动连接命令:")
        for i in range(args.device_count):
            print(f"   adb connect 127.0.0.1:{args.port + i}")
        return

    print(f"✅ 成功连接 {dm.connected_count} 个设备")

    # 2. 初始化模块
    sc = ScreenCapture(dm)
    cc = ClickController(dm, speed_mode=args.speed)

    print(f"\n⚡ 速度模式: {args.speed}")
    status = cc.antiban.status()
    print(f"   点击延迟: {status['click_delay']}")
    print(f"   坐标偏移: ±{status['offset_range']}px")

    # 3. 等待游戏加载
    print("\n⏳ 等待游戏加载...")
    time.sleep(3)

    # 4. 诊断测试
    if args.test:
        print("\n🔧 进入测试模式...")
        test_mode(dm, sc, cc)
        return

    print("\n🧪 连接测试...")
    try:
        for i in range(dm.connected_count):
            img = sc.capture(i)
            h, w = img.shape[:2]
            print(f"   设备{i+1}: ✅ 截图成功 ({w}x{h})")
    except Exception as e:
        print(f"   ❌ 截图失败: {e}")
        print("   请检查ADB连接和模拟器状态")
        return

    # 5. 启动师门任务
    print(f"\n🎯 启动师门任务 (每设备{args.rounds}轮)...")
    print("-" * 50)

    for i in range(dm.connected_count):
        print(f"\n>>> 开始设备 {i+1} <<<")
        task = ShimenTask(dm, sc, cc, max_rounds=args.rounds)
        task.run(i)
        print(f">>> 设备 {i+1} 完成 <<<")

        # 设备间随机间隔
        if i < dm.connected_count - 1:
            delay = 3 + i * 2
            print(f"    等待{delay}秒后处理下一个设备...")
            time.sleep(delay)

    print("\n" + "=" * 50)
    print("✅✅ 全部任务执行完成")
    print("=" * 50)


def test_mode(dm, sc, cc):
    """测试模式：检测设备和截图"""
    print("\n" + "=" * 30)
    print("测试模式 - 不执行实际任务")
    print("=" * 30)

    print("\n📱 设备信息:")
    for i in range(dm.connected_count):
        serial = f"127.0.0.1:{MUMU_BASE_PORT + i}"
        try:
            prop = dm.get_prop(i, "ro.product.model")
            print(f"   设备{i+1} ({serial}): {prop}")
        except:
            print(f"   设备{i+1} ({serial}): 连接但无法获取信息")

    print("\n🖼️ 截图测试:")
    for i in range(dm.connected_count):
        try:
            img = sc.capture(i)
            h, w = img.shape[:2]
            print(f"   设备{i+1}: ✅ {w}x{h}")
        except Exception as e:
            print(f"   设备{i+1}: ❌ {e}")

    print("\n🎮 点击测试:")
    if dm.connected_count > 0:
        print(f"   在设备0的 (100,100) 执行测试点击...")
        cc.tap(0, 100, 100)
        print("   ✅ 点击完成")
        print("\n💡 如果设备没有反应但点击返回成功，说明:")
        print("   1. ADB连接正常")
        print("   2. 坐标需要在游戏窗口内相对坐标")
        print("   3. 当前脚本使用 tap_game() 进行游戏内坐标点击")

    print("\n📋 速度模式状态:")
    status = cc.antiban.status()
    for k, v in status.items():
        print(f"   {k}: {v}")

    print("\n✅ 测试完成")
    print("\n💡 启动正式任务:")
    print("   python main.py --rounds 20 --speed fast")


if __name__ == "__main__":
    main()
