# MEMORY.md - 长期记忆

## 关于我 (AI助手)
- **名字**: 脚脚 🦶
- **创建日期**: 2026-04-02
- **性格**: 直接、有想法、靠谱
- **原则**: 实事求是，有就是有，没有就是没有

## 关于蛋总 (余坦)
- **称呼**: 蛋总
- **设备**: MacBook Pro (Apple M1 Pro, 14核)
- **主屏**: MacBook Pro内置 Liquid Retina XDR (3024x1964 Retina, 1512x982逻辑)
- **副屏**: Samsung QHD 2560x1440 @ 75Hz，位于主屏右侧
- **语言**: 中文
- **时区**: Asia/Shanghai (GMT+8)

## 蛋总的Mac配置要点

### 显示器
- 主屏: 1512x982 (逻辑分辨率)
- 副屏(D2): 2560x1440, X偏移=1512 (紧贴主屏右侧)
- 游戏窗口通常在副屏运行

### 系统安全
- FileVault: 已启用
- SIP: 已启用
- 触控板轻点点击: 已关闭(用力点按模式)

### 已安装的关键应用
- 微信、QQ、钉钉、飞书、Telegram
- Safari (26.4)、Chrome
- Xcode (15.5)
- Python 3.13.5
- Node.js v22.14.0
- 梦幻西游.app
- iShot (截图工具)

## 重要路径
- 桌面: `/Users/yutan/Desktop/`
- 下载: `/Users/yutan/Downloads/`
- 文档: `/Users/yutan/Documents/`
- Workspace: `/Users/yutan/.openclaw/workspace/`
- 截图临时目录: `/tmp/`
- 梦幻西游手游脚本: `/Users/yutan/.openclaw/workspace/games/梦幻西游手游/scripts/`

## macOS 知识
详细知识体系已保存在: `memory/macOS知识体系.md`

### 关键要点
1. **截图命令**: `/usr/sbin/screencapture -x -D 2` 截副屏
2. **坐标系统**: Retina屏幕逻辑坐标=物理像素/2
3. **Spotlight搜索**: `⌘ + Space`
4. **强制退出**: `Option + ⌘ + Escape`
5. **锁屏**: `Control + ⌘ + Q`

## 项目记录

### 梦幻西游手游脚本
- 路径: `workspace/games/梦幻西游手游/scripts/`
- 技术: Python + ADB (ppadb) + OpenCV
- 状态: 框架已搭建，待完善截图素材
- 问题: 
  1. 截图位置确定（需要模板图片）
  2. 操作速度（已添加turbo模式优化）
- 解决方案:
  - 使用 `cc.set_speed_mode("turbo")` 可大幅提升速度
  - 使用 `cc.tap_game(x, y)` 进行游戏内坐标点击
  - 详细见 `core/coordinate_manager.py` 和 `core/antiban.py`

## 待完成的任务
1. [ ] 梦幻西游手游脚本 - 需要蛋总提供截图素材
2. [ ] 完善截图功能（可能需要处理屏幕录制权限）
3. [ ] Windows Agent方案 - 待蛋总回到Windows前准备

## Windows Agent 自动化方案（待执行）

### 背景问题
- 蛋总2-3天不在Windows电脑前
- 需要自动化测试和调试
- GitHub在国内不稳定，路由器NAT

### 方案设计：Git轮询模式

```
我(Mac/飞书) ←→ GitHub ←→ Windows Agent（后台轮询）
```

### 目录结构
```
workspace/
├── commands/          # 我放命令到这里
│   └── 01_xxx.sh
├── results/           # Agent执行结果
│   └── 01_xxx.json
├── windows-agent/     # Windows客户端
│   ├── agent.py       # 主程序
│   └── config.yaml    # 配置
└── games/
```

### Agent功能
1. 每30秒 git pull 一次
2. 发现命令 → 执行 → git push 结果
3. 断网恢复后自动同步
4. 自动安装 Python / ADB

### 蛋总只需做一次
1. Windows装Python（国内镜像）
2. git clone 代码
3. 双击 agent.py 启动

### 前提确认
- ✅ GitHub可访问（不稳定，需重试机制）
- ✅ 路由器NAT上网
- ❌ 蛋总暂不在Windows前

### 状态
待蛋总回到Windows前开始部署

## 经验教训
- Mac截图可能因硬件加速保护导致黑屏
- Apple Silicon Mac使用arm64架构，但可以运行x86_64程序
- Python 3.13比较新，某些包可能还没支持

---

*最后更新: 2026-04-02*
