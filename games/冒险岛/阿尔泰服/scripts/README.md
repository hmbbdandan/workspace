# 冒险岛: 阿尔泰服 (Artale) 自动脚本 v2.0

## 环境准备

### 1. 安装 MuMu 模拟器
- 下载地址: https://mumu.163.com/
- 配置：开启ADB端口（默认16384）
- 分辨率建议：960x540

### 2. 安装 Python 依赖
```bash
cd scripts
pip install -r requirements.txt
```

### 3. 连接测试
```bash
adb connect 127.0.0.1:16384  # 实例0
adb devices  # 确认连接
```

## 目录结构
```
scripts/
├── main.py                  # 主入口
├── config.py                # 配置文件
├── core/
│   ├── device_manager.py    # ADB设备管理
│   ├── screen_capture.py    # 截图+图像识别
│   └── keyboard_controller.py # 按键控制
├── assets/
│   ├── player/              # 玩家角色模板
│   ├── monsters/            # 怪物模板
│   ├── npc/                 # NPC模板
│   └── ui/                  # UI元素模板
└── requirements.txt
```

## 使用方法

### 调试模式（测试连接和截图）
```bash
python main.py --test
```

### 自动刷怪模式
```bash
# 需要先提供怪物模板到 assets/monsters/
python main.py --mode farm --speed fast
```

### 参数说明
| 参数 | 说明 |
|------|------|
| `--port` | ADB端口（默认16384） |
| `--device` | 设备数量 |
| `--speed` | 速度模式：normal/fast/turbo |
| `--mode` | 运行模式：farm/debug |

## 速度模式

| 模式 | 操作延迟 | 适用场景 |
|------|----------|----------|
| normal | 0.8-2.5秒 | 保守模式，防封 |
| fast | 0.2-0.5秒 | 平衡模式 |
| turbo | 0.1-0.2秒 | 效率优先 |

## 截图素材

详细的截图指南见 `assets/README.md`

需要提供的模板：
- `assets/player/name_tag.png` - 玩家名字标签
- `assets/monsters/*.png` - 各种怪物模板
- `assets/ui/drop_item.png` - 掉落物品

## 脚本功能

### 已实现
- ✅ ADB设备连接管理
- ✅ 屏幕截图（adb screencap）
- ✅ 模板匹配（OpenCV）
- ✅ 按键/点击控制
- ✅ 三档速度模式
- ✅ 怪物检测与追踪

### 待实现
- ❌ 牧师自动治疗
- ❌ 技能循环释放
- ❌ 自动补给（买药）
- ❌ 地图切换检测
- ❌ BOSS战斗

## 防封建议

1. **使用 fast 模式**，不要用 turbo
2. **每隔5-10分钟随机移动**
3. **不要24小时连续跑**
4. **优先白天运行**

⚠️ **注意**：冒险岛有明确封号风险，请谨慎使用

## 故障排除

### 截图失败
- 检查ADB连接：`adb devices`
- 重启模拟器的ADB：`adb kill-server && adb start-server`

### 找不到怪物
- 确认怪物模板已放置：`ls assets/monsters/`
- 测试匹配：`python main.py --test`

### 点击位置不准
- 校准坐标：检查游戏分辨率设置
- MuMu默认960x540
