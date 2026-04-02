"""
阿尔泰服 升级效率分析
计算各职业升级效率和金币成本
"""

# ========== 经验表 (Artale 官方数据) ==========
EXP_TABLE = {
    1: 15, 2: 34, 3: 57, 4: 92, 5: 135,
    6: 372, 7: 560, 8: 840, 9: 1242, 10: 1716,
    11: 2360, 12: 3216, 13: 4200, 14: 5460, 15: 7050,
    16: 8840, 17: 11040, 18: 13716, 19: 16680, 20: 20216,
    21: 24402, 22: 28980, 23: 34320, 24: 40512, 25: 47216,
    26: 54900, 27: 63666, 28: 73080, 29: 83720, 30: 95700,
    31: 108480, 32: 122760, 33: 138666, 34: 155540, 35: 174216,
    36: 194832, 37: 216600, 38: 240500, 39: 266682, 40: 294216,
    41: 324240, 42: 356916, 43: 391160, 44: 428280, 45: 468450,
    46: 510420, 47: 555680, 48: 604416, 49: 655200, 50: 709716,
    # 51-100 每级约 +5%
    51: 748608, 52: 789631, 53: 832902, 54: 878545, 55: 926689,
    56: 977471, 57: 1031036, 58: 1087536, 59: 1147132, 60: 1209994,
    61: 1276301, 62: 1346242, 63: 1420016, 64: 1497832, 65: 1579913,
    66: 1666492, 67: 1757815, 68: 1854143, 69: 1955750, 70: 2062925,
    71: 2175973, 72: 2295216, 73: 2420993, 74: 2553663, 75: 2693603,
    76: 2841212, 77: 2996910, 78: 3161140, 79: 3334370, 80: 3517093,
    81: 3709829, 82: 3913127, 83: 4127566, 84: 4353756, 85: 4592341,
    86: 4844001, 87: 5109452, 88: 5389449, 89: 5684790, 90: 5996316,
    91: 6324914, 92: 6671519, 93: 7037118, 94: 7422752, 95: 7829518,
    96: 8258575, 97: 8711144, 98: 9188514, 99: 9692044, 100: 10223168,
}

# ========== 关键练级地点怪物数据 (来源: mapleartale.com) ==========
# 格式: (怪物名, 等级, 经验, HP, 防御)
MONSTERS = {
    # 1-30级 常见练级区
    "森林入口": [
        ("嫩寶", 1, 3, 8, 0),
        ("藍寶", 2, 4, 15, 0),
        ("菇菇仔", 2, 5, 20, 0),
        ("木妖", 4, 8, 40, 2),
        ("綠水靈", 6, 10, 50, 3),
    ],
    "射手村": [
        ("綠菇菇", 15, 26, 250, 10),
        ("黑木妖", 10, 18, 250, 8),
    ],
    "魔法密林": [
        ("菇菇寶貝", 8, 15, 120, 5),
    ],
    # 30-50级
    "蚂蚁洞": [
        ("刺菇菇", 28, 45, 800, 20),
        ("殭屍菇菇", 30, 50, 1000, 22),
    ],
    "废弃都市": [
        ("殭屍蘑菇", 32, 55, 1200, 25),
    ],
    # 50-70级
    "火焰之地": [
        ("火肥肥", 45, 85, 2500, 35),
        ("黑斧木妖", 48, 95, 3000, 40),
    ],
    "北部森林": [
        ("褐菇菇", 35, 60, 1500, 28),
    ],
    # 61-70级
    "天空之城": [
        ("獨角獅", 55, 120, 4000, 50),
        ("青布丁", 58, 130, 4500, 55),
    ],
    "冰原雪域": [
        ("雪吉拉", 62, 150, 5000, 60),
    ],
    # 70-100级
    "神木村": [
        ("進化妖魔", 72, 200, 8000, 75),
        ("巫婆", 75, 220, 10000, 80),
    ],
    "宁静沼泽": [
        ("土龍", 68, 180, 7000, 70),
    ],
}

# ========== 职业属性 (典型满级配点, 非极限) ==========
# 格式: (主属性, 魔攻/物攻, 武器系数, 武器类型, AOE范围, 装备成本系数)
CLASSES = {
    "火毒法师": {
        "type": "magic",
        "primary": 900,      # INT
        "secondary": 400,    # LUK
        "attack": 150,       # 魔法攻击
        "coefficient": 1.0,  # 魔法公式系数
        "aoe": 8,            # 可攻击怪物数
        "survivability": 3,  # 生存能力 1-5
        "equip_cost": 0.8,   # 装备成本系数
        "potion_cost": 0.3, # 药水成本系数
        "skill_name": "火流星/毒雾",
    },
    "冰雷法师": {
        "type": "magic",
        "primary": 850,
        "secondary": 450,
        "attack": 145,
        "coefficient": 1.0,
        "aoe": 6,
        "survivability": 3,
        "equip_cost": 0.8,
        "potion_cost": 0.4,
        "skill_name": "冰冻结界/雷霆万钧",
    },
    "黑骑士": {
        "type": "physical",
        "primary": 950,      # STR
        "secondary": 400,    # DEX
        "attack": 180,       # 武器攻击
        "coefficient": 4.8,   # 双手斧系数
        "aoe": 3,
        "survivability": 5,  # 高血量+吸血
        "equip_cost": 1.2,
        "potion_cost": 0.2,
        "skill_name": "暗蚀/仲裁",
    },
    "神射手": {
        "type": "physical",
        "primary": 900,      # DEX
        "secondary": 450,    # STR
        "attack": 165,
        "coefficient": 3.4,  # 弓系数
        "aoe": 5,
        "survivability": 3,
        "equip_cost": 1.0,
        "potion_cost": 0.5,
        "skill_name": "暴风箭雨",
    },
    "双刀": {
        "type": "physical",
        "primary": 850,      # LUK
        "secondary": 500,    # STR+DEX
        "attack": 160,
        "coefficient": 3.6,  # 飞侠系数
        "aoe": 4,
        "survivability": 4,  # 隐身保命
        "equip_cost": 0.9,
        "potion_cost": 0.4,
        "skill_name": "撕裂/隐身",
    },
    "主教": {
        "type": "magic",
        "primary": 800,
        "secondary": 600,    # 较高的LUK
        "attack": 130,
        "coefficient": 1.0,
        "aoe": 5,
        "survivability": 3,
        "equip_cost": 1.0,
        "potion_cost": 0.6,  # 治疗需求高
        "skill_name": "圣光/复活",
    },
}

def calc_magic_damage(int_val, magic_atk, mastery=0.8):
    """计算法师伤害 (简化公式)"""
    base = ((magic_atk**2 / 1000 + magic_atk) / 30 + int_val / 200)
    return base * magic_atk * mastery

def calc_physical_damage(str_val, dex_val, wep_atk, coefficient):
    """计算物理伤害"""
    return (str_val * coefficient + dex_val) * wep_atk / 100

def calc_exp_per_hour(class_name, class_data, monster_hp, monster_exp, monster_def, kills_per_minute=30):
    """计算每小时经验"""
    # 基础伤害计算
    if class_data["type"] == "magic":
        damage = calc_magic_damage(class_data["primary"], class_data["attack"], 0.8)
    else:
        damage = calc_physical_damage(
            class_data["primary"], class_data["secondary"],
            class_data["attack"], class_data["coefficient"]
        )
    
    # 防御减免 (简化)
    effective_damage = max(damage - monster_def * 0.5, damage * 0.1)
    
    # 实际击杀速度 (考虑走位、AOE等因素)
    if class_data["aoe"] > 1:
        # AOE职业: 每次攻击处理多个怪物
        kills_per_minute = kills_per_minute * class_data["aoe"] * 0.6
    else:
        kills_per_minute = kills_per_minute * 0.8
    
    exp_per_hour = monster_exp * kills_per_minute * 60
    
    return exp_per_hour, effective_damage

def calc_gold_cost_per_level(class_name, class_data, level):
    """估算每级金币成本"""
    # 装备强化成本 (随等级增加)
    equip_base = 10000 * (level ** 1.5)
    equip_cost = equip_base * class_data["equip_cost"]
    
    # 药水成本
    potion_base = 500 * level * class_data["potion_cost"]
    potion_cost = potion_base * 60  # 假设每级需要60分钟的药水
    
    # 冲卷/技能成本 (粗略估算)
    scroll_cost = 50000 * level * class_data["equip_cost"]
    
    return equip_cost + potion_cost + scroll_cost

def analyze_leveling_efficiency(start_level, end_level):
    """分析升级效率"""
    print(f"\n{'='*60}")
    print(f"阿尔泰服 升级效率分析 ({start_level}-{end_level}级)")
    print(f"{'='*60}")
    
    # 选择关键练级地点 (根据等级段)
    if end_level <= 30:
        location = "森林/射手村"
        monsters = MONSTERS["森林入口"] + MONSTERS["射手村"]
    elif end_level <= 50:
        location = "蚂蚁洞/废弃都市"
        monsters = MONSTERS["蚂蚁洞"] + MONSTERS["废弃都市"]
    elif end_level <= 70:
        location = "火焰之地/冰原雪域"
        monsters = MONSTERS["火焰之地"] + MONSTERS["天空之城"]
    else:
        location = "神木村/宁静沼泽"
        monsters = MONSTERS["神木村"] + MONSTERS["宁静沼泽"]
    
    # 取代表性怪物
    avg_monster = monsters[len(monsters)//2]
    monster_name, monster_lv, monster_exp, monster_hp, monster_def = avg_monster
    
    print(f"\n参考地图: {location}")
    print(f"代表怪物: {monster_name} (Lv.{monster_lv}, EXP:{monster_exp}, HP:{monster_hp}, DEF:{monster_def})")
    
    # 计算升级所需总经验
    total_exp_needed = sum(EXP_TABLE.get(l, EXP_TABLE[100] * (1.05 ** (l - 100))) 
                           for l in range(start_level, end_level))
    
    print(f"\n{start_level}-{end_level}级 总需经验: {total_exp_needed:,}")
    
    # 计算每职业
    results = []
    for class_name, class_data in CLASSES.items():
        exp_per_hour, damage = calc_exp_per_hour(
            class_name, class_data, monster_hp, monster_exp, monster_def
        )
        
        hours_needed = total_exp_needed / exp_per_hour if exp_per_hour > 0 else 999
        
        # 金币成本
        gold_cost = sum(calc_gold_cost_per_level(class_name, class_data, l) 
                        for l in range(start_level, end_level))
        
        results.append({
            "class": class_name,
            "exp_per_hour": exp_per_hour,
            "hours_needed": hours_needed,
            "gold_cost": gold_cost,
            "damage": damage,
            "aoe": class_data["aoe"],
            "survivability": class_data["survivability"],
            "skill": class_data["skill_name"],
        })
    
    # 按经验效率排序
    results.sort(key=lambda x: x["exp_per_hour"], reverse=True)
    
    print(f"\n{'职业':<12} {'每小时EXP':>12} {'升级时间':>10} {'金币成本':>15} {'DPS':>10} {'AOE':>5}")
    print("-" * 70)
    
    for r in results:
        print(f"{r['class']:<12} {r['exp_per_hour']:>12,.0f} {r['hours_needed']:>9.1f}h {r['gold_cost']:>14,.0f} {r['damage']:>10,.0f} {r['aoe']:>5}")
    
    # 最佳选择
    best_exp = results[0]
    best_gold = min(results, key=lambda x: x["gold_cost"])
    
    print(f"\n🏆 经验效率最佳: {best_exp['class']} (每小时 {best_exp['exp_per_hour']:,.0f} EXP)")
    print(f"💰 金币成本最低: {best_gold['class']} (总计 {best_gold['gold_cost']:,.0f} 金币)")
    
    # 综合推荐
    print(f"\n{'='*60}")
    print("📊 综合推荐:")
    
    for r in results:
        score = (r["exp_per_hour"] / best_exp["exp_per_hour"]) * 0.4 + \
                (1 - r["gold_cost"] / best_exp["gold_cost"]) * 0.3 + \
                (r["aoe"] / max(x["aoe"] for x in results)) * 0.15 + \
                (r["survivability"] / 5) * 0.15
        r["score"] = score
    
    results.sort(key=lambda x: x["score"], reverse=True)
    
    for i, r in enumerate(results[:3], 1):
        print(f"  {i}. {r['class']} (综合得分: {r['score']:.2f})")
        print(f"     技能: {r['skill']}")
        print(f"     效率: {r['exp_per_hour']:,.0f} EXP/h | 成本: {r['gold_cost']:,.0f} 金币")

if __name__ == "__main__":
    # 分析各等级段
    for start, end in [(1, 30), (30, 70), (70, 100), (1, 100)]:
        analyze_leveling_efficiency(start, end)
