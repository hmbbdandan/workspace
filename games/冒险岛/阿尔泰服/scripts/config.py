"""
配置文件 - Artale 阿尔泰服脚本
"""

# ========== 游戏窗口设置 ==========
GAME_WINDOW = {
    "title": "MapleStory Worlds",  # 窗口标题
    "min_width": 800,
    "min_height": 600,
}

# ========== 屏幕识别设置 ==========
SCREEN = {
    "screenshot_interval": 0.1,  # 截图间隔(秒)
    "template_match_threshold": 0.80,  # 模板匹配阈值
}

# ========== 键盘设置 ==========
KEYBOARD = {
    # 移动键
    "move_left": "left",
    "move_right": "right",
    "jump": "up",
    # 攻击键（根据个人设置调整）
    "attack": "ctrl",
    "skill1": "a",  # 技能1
    "skill2": "s",  # 技能2
    "skill3": "d",  # 技能3
    "skill4": "f",  # 技能4
    # 功能键
    "pickup": "z",  # 捡物
    "sit": "h",     # 坐下
    "buff": "q",    #  Buff技能
}

# ========== 角色设置 ==========
CHARACTER = {
    "name_tag_template": "assets/player_name.png",  # 角色名牌模板
    "hp_bar_template": "assets/hp_bar.png",          # 血条模板
    "mp_bar_template": "assets/mp_bar.png",          # 蓝条模板
}

# ========== 牧师辅助设置 ==========
PRIEST = {
    "heal_hp_threshold": 0.3,  # 血量低于30%时治疗
    "heal_skill": "s",           # 治疗技能键
    "buff_skill": "q",           # Buff技能键
    "resurrection_skill": "f",   # 复活技能键
}

# ========== 防封设置 ==========
ANTIBAN = {
    "min_action_delay": 1.0,   # 最小操作延迟(秒)
    "max_action_delay": 3.0,   # 最大操作延迟(秒)
    "random_pickup_delay": 0.5,  # 捡物随机延迟
    "random_movement": True,     # 随机移动
}

# ========== 支持的地图 ==========
SUPPORTED_MAPS = {
    "north_forst_training_ground_2": {
        "name": "北部森林训练场2",
        "monsters": ["green_mushroom", "spike_mushroom"],
    },
    "fire_land_2": {
        "name": "火焰之地2",
        "monsters": ["fire_pig", "black_axe_stump"],
    },
    "ant_cave_2": {
        "name": "蚂蚁洞2",
        "monsters": ["spike_mushroom", "zombie_mushroom"],
    },
    "cloud_balcony": {
        "name": "云彩露台",
        "monsters": ["brown_windup_bear", "pink_windup_bear"],
    },
    "lost_time_1": {
        "name": "遗失的时间1",
        "monsters": ["evolved_ghost"],
    },
}
