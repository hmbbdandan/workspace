# 梦幻西游手游脚本

## 环境准备

### 1. 安装 MuMu 模拟器
- 下载地址: https://mumu.163.com/
- 多开5个实例（设置 → 多开 → 新建实例）
- 每个实例安装梦幻西游手游并登录账号

### 2. 安装 Python 依赖
```bash
cd scripts
pip install -r requirements.txt
```

### 3. 安装 ADB（MuMu自带）
确保 `adb` 命令可用，MuMu安装在：
`C:\Program Files (x86)\MuMu\emulator\nemu9.0.63\shell`

### 4. 配置环境变量（可选）
把 MuMu 的 adb 路径加到 PATH，或者直接用全路径连接

### 5. 连接测试
```bash
adb connect 127.0.0.1:16384  # 实例0
adb connect 127.0.0.1:16385  # 实例1
adb connect 127.0.0.1:16386  # 实例2
adb connect 127.0.0.1:16387  # 实例3
adb connect 127.0.0.1:16388  # 实例4
```

## 目录结构
```
scripts/
├── config/
│   └── settings.yaml      # 配置文件
├── core/
│   ├── device_manager.py   # 设备管理器
│   ├── screen_capture.py   # 截图/图像识别
│   ├── antiban.py          # 防封模块
│   └── click_controller.py # 点击控制器
├── tasks/
│   └── shimen.py          # 师门任务
├── assets/
│   └── shimen/            # 师门任务图像素材
├── requirements.txt
└── main.py                # 主入口
```

## 运行
```bash
python main.py
```

## 当前状态
⚠️ **框架已搭建，核心逻辑待实现**

已完成:
- ✅ 多设备管理框架
- ✅ 截图 + OpenCV图像识别
- ✅ 点击防封（随机延迟/偏移）
- ✅ 师门任务流程框架

待完成:
- ❌ 师门任务完整流程（需要截图素材）
- ❌ 捉鬼、副本等其他任务
- ❌ OCR文字识别集成
- ❌ 素材截图（需要你自己截）

## 下一步
需要你提供截图素材来完善脚本：
1. 师门师父位置截图
2. 师门任务按钮截图
3. 各种任务完成后的确认按钮截图

把这些截图放到 `assets/shimen/` 目录，我来完成具体的识别逻辑。
