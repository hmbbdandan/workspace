# macOS 知识体系

> 学习时间：2026-04-02
> 系统版本：macOS 15.7.6 Sequoia
> 芯片：Apple M1 Pro

---

## 一、系统架构

### 1.1 核心组件
- **Darwin**: Unix内核
- **Aqua**: GUI界面
- **Quartz**: 2D图形
- **Metal**: GPU加速
- **Core Animation**: 动画引擎
- **WebKit**: 浏览器引擎
- **Apple Silicon (M1 Pro)**: ARM64架构

### 1.2 重要目录结构
```
/System/Library/          # 系统库
    /Applications/        # 系统应用
    /CoreServices/       # 核心服务
    /Extensions/         # 内核扩展
    /Frameworks/         # 开发框架
    /PrivateFrameworks/  # 私有框架
/Users/yutan/            # 用户目录
    /Library/            # 用户库
        /Application Support/  # 应用数据
        /Preferences/          # 应用偏好设置
        /LaunchAgents/         # 用户启动项
        /Caches/               # 缓存
        /Logs/                 # 日志
/var/log/                # 系统日志
/tmp/                    # 临时文件
```

---

## 二、显示系统

### 2.1 蛋总的显示器配置
- **主屏**: MacBook Pro 14寸内置 Liquid Retina XDR
  - 分辨率: 3024 x 1964 (Retina 2x)
  - 实际UI分辨率: 1512 x 982
  - 位置: 内置
- **副屏**: Samsung LS27B61x (QHD)
  - 分辨率: 2560 x 1440
  - 刷新率: 75Hz
  - 位置: 在主屏**右侧** (X=1512)
  - 常用于：游戏（梦幻西游手游）

### 2.2 坐标系统
- **Retina屏幕**: macOS报告的坐标是物理像素，但UI逻辑分辨率是实际像素的一半
  - 主屏逻辑: 1512 x 982
  - 主屏物理: 3024 x 1964
- **副屏**: 无Retina，物理=逻辑
  - 分辨率: 2560 x 1440
- **游戏窗口位置**（副屏D2）:
  - 偏移量: (1540, 148)
  - 游戏区域: 326 x 453

### 2.3 截图命令
```bash
# 基本截图
/usr/sbin/screencapture -x /tmp/screen.png           # 全屏截图
/usr/sbin/screencapture -x -D 1 /tmp/screen.png      # 主屏截图
/usr/sbin/screencapture -x -D 2 /tmp/screen.png      # 副屏截图
/usr/sbin/screencapture -x -R x,y,w,h /tmp/area.png  # 区域截图

# 交互式截图
/usr/sbin/screencapture -i /tmp/interactive.png      # 选区截图(带GUI)
screencapture -W                                      # 选择窗口截图
screencapture -c                                      # 直接复制到剪贴板
```

⚠️ **注意**: 游戏可能有硬件加速保护导致截图黑屏，需要：
- 系统设置 → 隐私与安全性 → 屏幕录制 → 允许对应App

---

## 三、常用快捷键

### 3.1 系统级
| 快捷键 | 功能 |
|--------|------|
| ⌘ + Space | 打开Spotlight搜索 |
| ⌘ + Tab | 切换应用程序 |
| ⌘ + ` | 切换同一应用的不同窗口 |
| ⌘ + Q | 退出应用 |
| ⌘ + W | 关闭窗口 |
| ⌘ + H | 隐藏应用窗口 |
| ⌘ + M | 最小化窗口到Dock |
| ⌘ + , | 打开应用偏好设置 |
| ⌘ + Option + Esc | 强制退出菜单 |
| Control + ⌘ + Q | 锁屏 |
| ⌘ + Shift + Q | 退出登录 |

### 3.2 文件操作
| 快捷键 | 功能 |
|--------|------|
| ⌘ + C | 复制 |
| ⌘ + V | 粘贴 |
| ⌘ + X | 剪切 |
| ⌘ + Z | 撤销 |
| ⌘ + Shift + Z | 重做 |
| ⌘ + A | 全选 |
| ⌘ + D | 复制/贴上当前文件夹(副本) |
| ⌘ + Delete | 移到废纸篓 |
| ⌘ + Shift + Delete | 清空废纸篓 |
| Return/Enter | 重命名 |
| ⌘ + L | 创建替身(快捷方式) |
| ⌘ + I | 显示简介 |
| Space | 快速查看(Preview) |

### 3.3 Finder
| 快捷键 | 功能 |
|--------|------|
| ⌘ + N | 新建Finder窗口 |
| ⌘ + Shift + N | 新建文件夹 |
| ⌘ + O | 打开选中项 |
| ⌘ + Shift + G | 前往文件夹 |
| ⌘ + J | 显示视图选项 |
| ⌘ + / | 显示/隐藏路径栏 |
| ⌘ + [ | 后退 |
| ⌘ + ] | 前进 |
| ⌘ + Up | 前往上级目录 |
| ⌘ + Down | 前往选中项目录 |

### 3.4 文本编辑
| 快捷键 | 功能 |
|--------|------|
| ⌘ + S | 保存 |
| ⌘ + P | 打印 |
| ⌘ + F | 查找 |
| ⌘ + G | 查找下一个 |
| ⌘ + E | 查找所选 |
| Tab | 缩进 |
| Shift + Tab | 取消缩进 |
| ⌘ + / | 注释/取消注释 |

### 3.5 截图快捷键
| 快捷键 | 功能 |
|--------|------|
| ⌘ + Shift + 3 | 全屏截图 |
| ⌘ + Shift + 4 | 选择区域截图 |
| ⌘ + Shift + 4 + Space | 选择窗口截图 |
| ⌘ + Shift + 5 | 打开截图工具栏 |
| ⌘ + Control + Shift + 3 | 全屏截图到剪贴板 |
| ⌘ + Control + Shift + 4 | 区域截图到剪贴板 |

### 3.6 终端特定
| 快捷键 | 功能 |
|--------|------|
| ⌘ + K | 清屏 |
| ⌘ + T | 新标签页 |
| ⌘ + W | 关闭标签页 |
| ⌘ + N | 新窗口 |
| ⌘ + D | 垂直分屏 |
| ⌘ + Shift + D | 水平分屏 |
| Tab | 自动补全 |
| Control + C | 取消当前命令 |

---

## 四、触控板手势

### 4.1 基本手势
| 手势 | 功能 |
|------|------|
| 单指轻点 | 选中/点击 |
| 双指轻点 | 右键菜单 |
| 双指滚动 | 滚动页面 |
| 双指捏合 | 缩放 |
| 双指旋转 | 旋转图片 |
| 三指轻点 | 查词/翻译 |
| 四指展开 | 显示桌面 |
| 四指合拢 | 显示启动台 |

### 4.2 Mission Control 相关
| 手势 | 功能 |
|------|------|
| 四指上滑 | 打开Mission Control |
| 四指下滑 | 显示当前应用所有窗口 |
| 三指左右滑 | 切换全屏应用/桌面 |

### 4.3 蛋总的触控板配置
```
Clicking = 0 (轻点点击已关闭，需用力点按)
FirstClickThreshold = 1
SecondClickThreshold = 1
TrackpadCornerSecondaryClick = 0
ForceSuppressed = 0
```

---

## 五、命令行工具

### 5.1 系统管理
```bash
# 系统信息
sw_vers                      # macOS版本
uname -a                     # 内核信息
system_profiler SPSoftwareDataType  # 详细软件信息

# 电源管理
pmset -g                     # 查看电源状态
pmset -a displaysleep 30     # 设置显示器睡眠时间
caffeinate -u -t 3600        # 阻止休眠1小时
caffeinate -i -s             # 阻止空闲睡眠和系统睡眠

# 进程管理
ps aux | grep <name>         # 查找进程
kill -9 <pid>                # 强制结束进程
top -o cpu                   # 按CPU排序查看进程

# 内存
top -l 1 | grep PhysMem       # 内存使用情况
vm_stat                       # 虚拟内存统计
```

### 5.2 文件操作
```bash
# 文件元数据
mdls <file>                  # 查看文件元数据
mdls -name kMDItemKind <file> # 查看文件类型

# Spotlight搜索
mdfind "kind:image"           # 搜索所有图片
mdfind -onlyin /Users/yutan "keyword"  # 在特定目录搜索

# 文件权限
chmod 755 <file>             # 设置权限
chown yutan:staff <file>     # 更改所有者

# 创建符号链接
ln -s /path/to/target /path/to/link
```

### 5.3 网络相关
```bash
# 网络诊断
ifconfig                      # 网络接口信息
networksetup -listallhardwareports  # 端口列表
ping -c 4 <host>             # Ping测试
traceroute <host>            # 路由追踪
curl -I <url>                # HTTP头信息

# Wi-Fi
networksetup -getairportnetwork en0  # 获取当前Wi-Fi
networksetup -setairportnetwork en0 <SSID> <password>
```

### 5.4 磁盘管理
```bash
diskutil list                # 列出所有磁盘
diskutil info /dev/disk0s1  # 磁盘详情
diskutil repairVolume /dev/disk0s1  # 修复磁盘
```

### 5.5 AppleScript自动化
```bash
# 执行AppleScript
osascript -e 'tell application "Finder" to quit'
osascript -e 'display dialog "Hello"'

# 打开应用
open -a Safari
open -a "Google Chrome"
open /path/to/file

# 打开URL
open https://www.example.com

# 打开文件夹并选中文件
open -R /path/to/file  # 在Finder中显示
```

### 5.6 defaults 偏好设置
```bash
# 读取偏好设置
defaults read com.apple.finder ShowPathbar
defaults read com.apple.dock autohide

# 写入偏好设置
defaults write com.apple.dock autohide -bool true
defaults write com.apple.dock autohide-delay -float 0

# 重置偏好（删除.plist文件后重启）
defaults delete com.apple.dock
killall Dock

# 常用偏好设置位置
~/Library/Preferences/com.apple.*
~/Library/Preferences/<bundle-identifier>.plist
```

### 5.7 剪贴板
```bash
pbcopy < file.txt            # 复制文件内容到剪贴板
echo "text" | pbcopy         # 复制文本到剪贴板
pbpaste                      # 粘贴剪贴板内容
pbpaste > file.txt           # 粘贴到文件
```

### 5.8 安全管理
```bash
# SIP状态
csrutil status               # 查看SIP
sudo csrutil disable         # 关闭SIP(需恢复模式)

# FileVault
fdesetup status             # 查看加密状态
fdesetup enable             # 启用加密

# 钥匙串
security find-internet-password -s example.com
security find-internet-password -a "username" -s "server"
```

### 5.9 Time Machine
```bash
tmutil listbackups           # 列出所有备份
tmutil latestbackup          # 最新备份路径
tmutil deletebackup /path/to/backup  # 删除备份
tmutil startbackup --auto     # 开始备份
```

---

## 六、系统偏好设置

### 6.1 Apple菜单
- 关于本机 → 系统报告 → 硬件概览
- App Store → 自动更新
- 系统设置... → 进入系统设置App

### 6.2 系统设置 (macOS 13+)
```
应用                     # 应用设置、通知
Wi-Fi                    # 无线网络
蓝牙                     # 蓝牙设备
网络                     # 网络配置（以太网、VPN等）
通知                     # 通知中心设置
声音                     # 输出/输入设备、音量
专注模式                 #勿扰模式
屏幕使用时间             # 使用统计
边栏                     # Dock/菜单栏设置
外观                     # 浅色/深色/自动
桌面与程序坞              # Dock、任务切换等
控制中心                 # 菜单栏图标自定义
键盘                     # 键盘、快捷键、输入法
鼠标                     # 鼠标设置
触控板                   # 手势和点击设置
显示器                    # 分辨率、夜览、True Tone
壁纸                     # 桌面壁纸
屏幕保护程序              # 屏幕保护
电池                     # 电池健康、节能选项
打印机与扫描仪            # 打印机列表
扫描仪                    # 内置摄像头等
日期与时间               # 时间同步
时区                     # 时区设置
语言与地区               # 语言优先级
先进                     # 辅助功能设置
隐私与安全性              # 隐私、权限、安全
软件更新                  # 系统更新
共享                      # 文件共享、屏幕共享
Time Machine             # 备份设置
启动磁盘                  # 启动磁盘选择
辅助功能说明              # VoiceOver等
```

---

## 七、应用程序生态

### 7.1 蛋总已安装的应用
**开发工具**:
- Xcode (15.5)
- Python 3.13
- Infuse (视频)
- Adobe Acrobat DC
- Cisdem PDF Password Remover
- wpsoffice (金山文档)

**通讯工具**:
- WeChat (微信)
- QQ
- DingTalk (钉钉)
- Foxmail (邮件)
- AliMail (阿里邮箱)
- Telegram
- Skype
- Microsoft Teams
- TencentMeeting (腾讯会议)

**效率工具**:
- Notability (笔记)
- Goodnotes
- 微信读书
- 网易有道翻译

**媒体娱乐**:
- 哔哩哔哩
- QQ音乐
- 抖音
- 雷神加速器
- 奇游加速器
- Thunder (下载)
- 夸克网盘
- aDrive

**游戏**:
- 梦幻西游.app
- World of Warcraft
- MapleStory Worlds

**远程/工具**:
- ToDesk (远程桌面)
- UURemote
- UrPointer
- iShot (截图工具)
- logioptionsplus (罗技鼠标)
- VideoCompressorMac

**系统工具**:
- Safari (26.4)
- Google Chrome
- Lark (飞书)
- Sudoku (数独)
- Utilities (系统工具文件夹)

### 7.2 系统自带应用
```
/System/CurrentVersion/Utilities/
    Activity Monitor.app      # 活动监视器
    AirPort Utility.app      # AirPort设置
    Archive Utility.app      # 归档工具
    Audio MIDI Setup.app     # 音频配置
    Bluetooth File Exchange.app  # 蓝牙传输
    Boot Camp Assistant.app  # 双系统引导
    ColorSync Utility.app    # 色彩管理
    Console.app              # 控制台
    Digital Color Meter.app  # 取色器
    Disk Utility.app         # 磁盘工具
    Feedback Assistant.app   # 反馈助手
    Font Book.app            # 字体册
    Grab.app                 # 截图工具(旧版)
    Image Capture.app        # 图像捕捉
    Installer.app            # 安装器
    Keychain Access.app      # 钥匙串访问
    Migration Assistant.app  # 迁移助理
    Network Utility.app      # 网络工具
    Notes.app                # 备忘录
    Photo Booth.app          #  photo booth
    Power Statistics.app     # 电源统计
    Preview.app              # 预览
    Print Dialog.app         # 打印
    Password Assistant.app   # 密码助手
    Reminders.app            # 提醒事项
    Screenshot.app           # 截图工具
    Stickies.app             # 便签
    System Information.app   # 系统信息
    System Preferences.app   # 系统设置(旧版)
    Terminal.app             # 终端
    TextEdit.app             # 文本编辑
    VoiceOver Utility.app    # VoiceOver
    Wallpaper.app            # 壁纸
```

---

## 八、安全机制

### 8.1 系统完整性保护 (SIP)
- **状态**: 已启用 (Enabled)
- **位置**: macOS恢复模式
- **作用**: 防止恶意软件修改系统文件
- **命令**: `csrutil status`

### 8.2 FileVault
- **状态**: 已启用 (On)
- **作用**: 全磁盘加密
- **命令**: `fdesetup status`

### 8.3 隐私与安全性设置
路径: 系统设置 → 隐私与安全性
- 位置服务
- 联系人、日历、提醒事项
- 照片、相机、麦克风
- 屏幕录制
- 自动化
- 辅助功能

### 8.4 Gatekeeper
- 作用: 验证下载的App来源
- 设置: 系统设置 → 隐私与安全性 → 安全性

---

## 九、窗口管理

### 9.1 蛋总的热角设置
```
左下角 → Desktop (值=14)
```

### 9.2  Spaces
- **状态**: 已禁用 (Spaces disabled)
- 用户不使用多桌面

### 9.3 分屏
- Option + 点击窗口绿色按钮 → 进入分屏
- Control + 上划 → Mission Control

---

## 十、命令行和Shell

### 10.1 当前Shell
```bash
echo $SHELL  # 当前shell
zsh --version  # Z Shell版本
```

### 10.2 Homebrew
```bash
# 检查是否安装
which brew || echo "Homebrew not installed"
```

### 10.3 Python
```bash
python3 --version  # Python 3.13.5
which python3       # /usr/local/bin/python3
```

### 10.4 Node
```bash
node --version  # Node版本 (v22.14.0)
which node       # Node路径
```

---

## 十一、实用技巧

### 11.1 快速操作
- 在Finder中按 ⌘ + Option + V 移动文件(不复制)
- 在任何输入框按 ⌘ + Shift + Delete 清空
- 双指轻点触控板可弹出右键菜单
- 三指查找：选中文字后三指轻点查词

### 11.2 终端技巧
- `clear` 或 ⌘ + K 清屏
- `exit` 或 ⌘ + D 关闭分屏窗口
- `history` 查看命令历史
- `!$` 使用上一个命令的最后一个参数

### 11.3 文件关联
```bash
# 查看文件类型
file /path/to/file

# 更改默认打开方式
defaults write com.apple.LaunchServices LSHandlers -array \
    -dict LSHandlerURLScheme http LSHandlerRoleViewer com.apple.Safari
```

### 11.4 强制退出
- Option + ⌘ + Escape → 强制退出菜单
- 或 Control + ⌘ + 电源按钮

---

## 十二、已知限制和注意事项

### 12.1 截图限制
- 游戏可能有硬件加速保护导致截图黑屏
- 需要在「屏幕录制」权限中允许对应应用

### 12.2 Rosetta 2
- Apple Silicon Mac可以运行x86_64应用
- 使用 `arch -x86_64 <command>` 强制x86模式

### 12.3 权限问题
- 某些系统操作需要用户确认
- 辅助功能权限用于自动化控制

---

## 十三、快捷键速查表

```
┌─────────────────────────────────────────────────────┐
│                    macOS 快捷键                      │
├──────────────┬──────────────────────────────────────┤
│ ⌘ = Command │                                      │
│ ⌥ = Option   │                                      │
│ ⌃ = Control   │                                      │
│ ⇧ = Shift     │                                      │
│ ⎋ = Escape    │                                      │
├──────────────┼──────────────────────────────────────┤
│ 文件操作                                                    │
│ ⌘+C/V/X     │ 复制/粘贴/剪切                          │
│ ⌘+Z         │ 撤销                                    │
│ ⌘+Shift+Z   │ 重做                                    │
│ ⌘+S         │ 保存                                    │
│ ⌘+O         │ 打开                                    │
│ ⌘+N         │ 新建                                    │
│ ⌘+W         │ 关闭窗口                                │
│ ⌘+Q         │ 退出应用                                │
├──────────────┼──────────────────────────────────────┤
│ 系统操作                                                    │
│ ⌘+Space     │ Spotlight搜索                           │
│ ⌘+Tab       │ 切换应用                                │
│ ⌘+,         │ 偏好设置                                │
│ ⌘+Option+Esc│ 强制退出                                 │
│ ⌘+Shift+Q   │ 退出登录                                │
│ Control+⌘+Q │ 锁屏                                    │
├──────────────┼──────────────────────────────────────┤
│ Finder                                                       │
│ ⌘+Shift+G   │ 前往文件夹                              │
│ ⌘+Up        │ 上级目录                                 │
│ ⌘+Delete    │ 移到废纸篹                              │
│ Space       │ 快速查看                                │
│ Return      │ 重命名                                   │
├──────────────┼──────────────────────────────────────┤
│ 截图                                                         │
│ ⌘+Shift+3   │ 全屏截图                                │
│ ⌘+Shift+4   │ 选择区域截图                            │
│ ⌘+Shift+5   │ 截图工具栏                              │
│ ⌘+Control+3 │ 全屏到剪贴板                            │
│ ⌘+Control+4 │ 选择到剪贴板                            │
└──────────────┴──────────────────────────────────────┘
```

---

*最后更新: 2026-04-02*
