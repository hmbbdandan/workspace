"""
冒险岛: 阿尔泰服 (Artale) - 自动脚本主入口 v2.0
支持 ADB 连接 MuMu 模拟器
"""

import time
import sys
import argparse
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from core.device_manager import DeviceManager
from core.screen_capture import ScreenCapture
from core.keyboard_controller import KeyController, AutoFarmController
from config import MUMU_BASE_PORT, DEVICE_COUNT, ANTIBAN


def parse_args():
    parser = argparse.ArgumentParser(description="冒险岛:阿尔泰服 自动脚本")
    parser.add_argument("--port", type=int, default=MUMU_BASE_PORT, help="ADB基础端口")
    parser.add_argument("--device", type=int, default=1, help="设备数量")
    parser.add_argument("--mode", choices=["farm", "debug"], default="debug", help="运行模式")
    parser.add_argument("--speed", choices=["normal", "fast", "turbo"], default="fast", help="速度模式")
    parser.add_argument("--test", action="store_true", help="测试模式")
    return parser.parse_args()


def main():
    print("=" * 50)
    print("冒险岛: 阿尔泰服 (Artale) 自动脚本 v2.0")
    print("=" * 50)

    args = parse_args()

    # 1. 连接设备
    print(f"\n📱 连接模拟器 (端口 {args.port})...")
    dm = DeviceManager(base_port=args.port, device_count=args.device)

    if dm.connected_count == 0:
        print("❌ 没有找到模拟器，请检查:")
        print("   1. MuMu模拟器是否启动")
        print("   2. ADB端口是否正确")
        print(f"\n💡 手动连接: adb connect 127.0.0.1:{args.port}")
        return

    print(f"✅ 已连接 {dm.connected_count} 个设备")

    # 2. 初始化模块
    sc = ScreenCapture(dm)
    keys = KeyController(dm)
    keys.set_speed_mode(args.speed)

    print(f"\n⚡ 速度模式: {args.speed}")

    # 3. 测试截图
    print("\n🧪 测试截图...")
    try:
        img = sc.capture(0)
        h, w = img.shape[:2]
        print(f"   ✅ 截图成功 ({w}x{h})")
    except Exception as e:
        print(f"   ❌ 截图失败: {e}")
        return

    # 4. 调试模式
    if args.mode == "debug" or args.test:
        debug_mode(dm, sc, keys)
        return

    # 5. 自动刷怪模式
    if args.mode == "farm":
        farm_mode(dm, sc, keys)


def debug_mode(dm, sc, keys):
    """调试模式：测试各项功能"""
    print("\n" + "=" * 40)
    print("调试模式")
    print("=" * 40)

    device = 0

    # 测试截图
    print("\n📸 截图测试...")
    for i in range(3):
        img = sc.capture(device)
        print(f"   第{i+1}次: {img.shape[1]}x{img.shape[0]}")
        time.sleep(0.5)

    # 测试点击
    print("\n👆 点击测试...")
    print("   点击屏幕中央 (400, 300)...")
    dm.tap(device, 400, 300)
    time.sleep(1)

    # 测试按键
    print("\n⌨️ 按键测试...")
    print("   按返回键...")
    dm.press_back(device)
    time.sleep(1)

    # 测试移动
    print("\n🚶 移动测试...")
    print("   向右移动...")
    keys.move_right(device, 500)
    time.sleep(1)

    # 测试跳跃
    print("\n🦘 跳跃测试...")
    keys.jump(device)
    time.sleep(1)

    # 尝试检测玩家
    print("\n🎯 玩家检测...")
    img = sc.capture(device)
    found, pos, conf = sc.detect_player(img)
    if found:
        print(f"   ✅ 找到玩家: {pos} (置信度: {conf:.2f})")
    else:
        print("   ⚠️ 未检测到玩家（可能需要提供模板图片）")

    # 尝试检测物品
    print("\n💎 物品检测...")
    items = sc.detect_items(img)
    print(f"   发现 {len(items)} 个物品")

    print("\n" + "=" * 40)
    print("✅ 调试完成")
    print("=" * 40)


def farm_mode(dm, sc, keys):
    """自动刷怪模式"""
    print("\n" + "=" * 40)
    print("自动刷怪模式")
    print("=" * 40)

    # 获取怪物模板
    monster_templates = get_monster_templates()
    if not monster_templates:
        print("⚠️ 没有找到怪物模板，请先提供截图素材")
        print("   模板目录: assets/monsters/")
        return

    print(f"\n📁 加载了 {len(monster_templates)} 个怪物模板")

    # 创建自动控制器
    farm = AutoFarmController(dm)
    farm.sc = sc

    print("\n🚀 开始自动刷怪 (Ctrl+C 停止)...")
    print("-" * 40)

    try:
        farm.auto_farm_loop(0, monster_templates)
    except KeyboardInterrupt:
        print("\n\n⏹️ 停止自动刷怪")
        print("=" * 40)


def get_monster_templates():
    """获取怪物模板路径列表"""
    assets_dir = Path(__file__).parent / "assets" / "monsters"
    if not assets_dir.exists():
        return []

    templates = []
    for f in assets_dir.glob("*.png"):
        templates.append(str(f))

    return templates


if __name__ == "__main__":
    main()
