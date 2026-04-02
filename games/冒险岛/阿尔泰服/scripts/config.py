"""
配置文件 - 冒险岛: 阿尔泰服 (Artale) 脚本
"""

# ========== MuMu 模拟器配置 ==========
MUMU_BASE_PORT = 16384  # 实例0的ADB端口
DEVICE_COUNT = 1         # 默认单设备

# ========== 图像识别配置 ==========
SCREEN = {
    "template_match_threshold": 0.80,  # 模板匹配阈值
    "screenshot_interval": 0.1,         # 截图间隔(秒)
}

# ========== 防封配置 ==========
ANTIBAN = {
    "normal": {
        "min_action_delay": 0.8,
        "max_action_delay": 2.5,
    },
    "fast": {
        "min_action_delay": 0.2,
        "max_action_delay": 0.5,
    },
    "turbo": {
        "min_action_delay": 0.1,
        "max_action_delay": 0.2,
    },
}

# ========== 游戏分辨率 ==========
# MuMu模拟器默认分辨率
GAME_RESOLUTION = {
    "width": 960,
    "height": 540,
}

# ========== 常用坐标 (需要根据实际校准) ==========
# 这些坐标是相对于游戏窗口的百分比位置
UI_POSITIONS = {
    # 主界面
    "minimap": (50, 50),           # 小地图
    "player_hp_bar": (400, 510),   # 玩家血条
    "player_mp_bar": (400, 525),    # 玩家蓝条

    # 快捷栏
    "skill_slot_1": (200, 480),    # 技能槽1
    "skill_slot_2": (240, 480),     # 技能槽2
    "skill_slot_3": (280, 480),     # 技能槽3

    # 功能
    "pickup_btn": (400, 350),       # 捡物按钮
    "menu_btn": (920, 30),          # 菜单按钮
}

# ========== 支持的刷怪地图 ==========
SUPPORTED_MAPS = {
    "cloud_balcony": {
        "name": "云彩露台",
        "level_range": "1-30",
        "monsters": ["brown_windup_bear", "pink_windup_bear"],
    },
    "ant_cave": {
        "name": "蚂蚁洞",
        "level_range": "10-25",
        "monsters": ["zombie_mushroom", "spike_mushroom"],
    },
    "fire_forest": {
        "name": "火焰森林",
        "level_range": "25-40",
        "monsters": ["fire_pig", "black_axe_stump"],
    },
    "lost_time": {
        "name": "遗失的时间",
        "level_range": "40-60",
        "monsters": ["evolved_ghost"],
    },
    "dead_dragon_nest": {
        "name": "死龙巢穴",
        "level_range": "120-150",
        "monsters": ["dead_dragon"],
    },
}

# ========== 职业配置 ==========
CLASS_CONFIG = {
    "priest": {
        "heal_threshold": 0.3,      # 血量低于30%时治疗
        "heal_skill_slot": 2,        # 治疗技能键位
        "buff_skill_slot": 1,        # Buff技能键位
    },
    "bishop": {
        "heal_threshold": 0.3,
        "heal_skill_slot": 2,
        "buff_skill_slot": 1,
    },
    "冰雷": {
        "attack_skill_slot": 3,
        "heal_threshold": 0.2,
    },
    "黑骑士": {
        "attack_skill_slot": 4,
        "heal_threshold": 0.4,
    },
}
