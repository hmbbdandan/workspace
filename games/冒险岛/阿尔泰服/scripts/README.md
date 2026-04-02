# Artale 阿尔泰服脚本

> 基于开源项目 MapleStoryAutoLevelUp 思路，搭建的自动化脚本框架

## 环境准备

### 1. 安装依赖
```bash
cd scripts
pip install -r requirements.txt
```

### 2. 系统要求
- Windows 11（网页游戏，需要窗口模式）
- Python 3.12
- OpenCV 4.11

### 3. 游戏设置
- 游戏必须处于**窗口模式**
- 建议窗口尺寸调小（提高识别准确度）
- 浏览器推荐 Chrome（多开方便）

## 使用方法

### 基本命令
```bash
# 北部森林训练场2 刷绿蘑菇和刺蘑菇
python auto_levelup.py --map north_forst_training_ground_2 --monsters green_mushroom,spike_mushroom

# 火焰之地2 刷火肥肥
python auto_levelup.py --map fire_land_2 --monsters fire_pig

# 蚂蚁洞2 刷刺蘑菇和僵尸蘑菇
python auto_levelup.py --map ant_cave_2 --monsters spike_mushroom,zombie_mushroom
```

### 多开方案

**浏览器多开（最简单）：**
1. Chrome 多用户/多Profile
2. 每个Profile登录一个账号
3. 每个浏览器窗口运行一个脚本实例

**代理IP配置：**
- 每个浏览器实例配不同代理
- 避免同IP多账号被关联

## 目录结构
```
scripts/
├── config.py              # 配置文件
├── auto_levelup.py        # 主脚本
├── requirements.txt       # 依赖
├── core/
│   ├── screen_capture.py  # 屏幕捕获/图像识别
│   └── keyboard_controller.py  # 键盘控制
└── assets/
    ├── monsters/          # 怪物模板图
    └── maps/              # 地图配置
```

## 支持的地图和怪物

| 地图 | 怪物 |
|------|------|
| 北部森林训练场2 | 绿蘑菇、刺蘑菇 |
| 火焰之地2 | 火肥肥、黑斧木妖 |
| 蚂蚁洞2 | 刺蘑菇、僵尸蘑菇 |
| 云彩露台 | 褐色发条熊、粉色发条熊 |
| 遗失的时间1 | 进化妖魔 |

## 牧师专用配置

```python
# config.py 中的 PRIEST 配置
PRIEST = {
    "heal_hp_threshold": 0.3,  # 血量低于30%时治疗
    "heal_skill": "s",           # 治疗技能键
    "buff_skill": "q",           # Buff技能键
}
```

## ⚠️ 封号风险

- Artale 是 Nexon 官方平台
- 有实时检测 + 离线追封
- 使用第三方脚本有明确封号风险
- 建议：低多开数量 + 不同代理IP + 随机化操作

## 下一步

1. [ ] 获取游戏截图，制作怪物模板
2. [ ] 配置键盘映射（与你的技能键位一致）
3. [ ] 测试各地图识别效果
4. [ ] 配置牧师辅助逻辑
5. [ ] 添加更多地图支持

---

*基于 GitHub: KenYu910645/MapleStoryAutoLevelUp 的思路*
