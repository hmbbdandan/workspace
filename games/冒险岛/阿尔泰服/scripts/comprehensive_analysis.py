"""
阿尔泰服 全面收益分析 v2
包含：经验、药水消耗、怪物掉落、物品价值
"""

# ========== 怪物详细数据 (来源: mapleartale.com) ==========
# 格式: (名称, 等级, 经验, HP, 防御, 元素弱点, 掉落价值/小时)
MONSTERS_FULL = {
    # 1-30级区
    "森林入口": {
        "怪物": [
            ("嫩寶", 1, 3, 8, 0, "无", 0),
            ("藍寶", 2, 4, 15, 0, "无", 0),
            ("菇菇仔", 2, 5, 20, 0, "无", 0),
            ("木妖", 4, 8, 40, 2, "无", 50),
            ("綠水靈", 6, 10, 50, 3, "无", 50),
        ],
        "药水/小时": 1000,  # 蓝红药水
    },
    "射手村": {
        "怪物": [
            ("綠菇菇", 15, 26, 250, 10, "火", 200),
            ("黑木妖", 10, 18, 250, 8, "无", 150),
        ],
        "药水/小时": 3000,
    },
    "魔法密林": {
        "怪物": [
            ("菇菇寶貝", 8, 15, 120, 5, "无", 100),
            ("小幽灵", 12, 20, 180, 8, "圣", 300),  # 牧师用圣光吸
        ],
        "药水/小时": 2000,
    },
    # 30-50级区
    "废弃都市": {
        "怪物": [
            ("殭屍蘑菇", 32, 55, 1200, 25, "圣", 500),
            ("大幽靈", 35, 70, 1800, 30, "圣", 800),  # 牧师回血吸
            ("殭屍猴子", 38, 80, 2000, 32, "圣", 600),
        ],
        "药水/小时": 5000,
        "牧师特色": "回血技能抵消药水消耗",
    },
    "蚂蚁洞": {
        "怪物": [
            ("刺菇菇", 28, 45, 800, 20, "火", 400),
            ("殭屍菇菇", 30, 50, 1000, 22, "圣", 500),
        ],
        "药水/小时": 4000,
    },
    # 50-70级区
    "火焰之地": {
        "怪物": [
            ("火肥肥", 45, 85, 2500, 35, "冰", 600),
            ("黑斧木妖", 48, 95, 3000, 40, "无", 700),
        ],
        "药水/小时": 8000,
    },
    "冰原雪域": {
        "怪物": [
            ("雪吉拉", 62, 150, 5000, 60, "火", 1000),
            ("冰巨人", 65, 180, 6000, 70, "火", 1200),
        ],
        "药水/小时": 10000,
    },
    "天空之城": {
        "怪物": [
            ("獨角獅", 55, 120, 4000, 50, "无", 900),
            ("青布丁", 58, 130, 4500, 55, "无", 1000),
        ],
        "药水/小时": 7000,
    },
    # 70-100级区
    "神木村": {
        "怪物": [
            ("進化妖魔", 72, 200, 8000, 75, "圣", 1500),
            ("巫婆", 75, 220, 10000, 80, "圣", 1800),
            ("黑暗羽毛", 78, 250, 12000, 85, "圣", 2000),
        ],
        "药水/小时": 15000,
        "牧师特色": "圣光技能高效",
    },
    "宁静沼泽": {
        "怪物": [
            ("土龍", 68, 180, 7000, 70, "无", 1400),
            ("蜥蜴王", 72, 210, 9000, 78, "无", 1700),
        ],
        "药水/小时": 12000,
    },
}

# ========== 职业详细数据 ==========
CLASSES_FULL = {
    "牧师": {
        "type": "magic",
        "primary": 800,       # INT
        "secondary": 400,     # LUK
        "attack": 120,         # 魔法攻击
        "mastery": 0.8,
        "aoe": 3,             # 圣光+治疗范围
        "skill_damage": 150,   # 圣光术基础伤害
        "heal_skill": True,   # 有回血技能
        "heal_amount": 3000,   # 每秒回血量
        "potion_reduce": 0.9, # 牧师回血可抵消90%药水消耗
        "survivability": 5,
        "potion_cost_base": 0.1,  # 药水成本系数（极低因为有回血）
        "equip_cost": 1.0,
        "skill_name": "圣光术/复活/治疗",
        "best_grind": {
            "1-30": "小幽灵(魔法密林)",
            "30-50": "大幽灵(废弃都市)",
            "50-70": "雪吉拉(冰原雪域)",
            "70-100": "巫婆/进化妖魔(神木村)",
        },
    },
    "火毒法师": {
        "type": "magic",
        "primary": 900,
        "secondary": 400,
        "attack": 150,
        "mastery": 0.8,
        "aoe": 8,             # 火流星+毒雾全屏
        "skill_damage": 200,
        "heal_skill": False,
        "potion_reduce": 0.0,
        "survivability": 2,
        "potion_cost_base": 0.6,  # 站桩输出容易掉血
        "equip_cost": 0.8,
        "skill_name": "火流星/毒雾",
        "best_grind": {
            "1-30": "绿菇菇(射手村)",
            "30-50": "刺菇菇(蚂蚁洞)",
            "50-70": "火肥肥(火焰之地)",
            "70-100": "土龙(宁静沼泽)",
        },
    },
    "冰雷法师": {
        "type": "magic",
        "primary": 850,
        "secondary": 450,
        "attack": 145,
        "mastery": 0.8,
        "aoe": 6,
        "skill_damage": 180,
        "heal_skill": False,
        "potion_reduce": 0.1,
        "survivability": 3,
        "potion_cost_base": 0.5,
        "equip_cost": 0.8,
        "skill_name": "冰冻结界/雷霆万钧",
        "best_grind": {
            "1-30": "绿菇菇(射手村)",
            "30-50": "刺菇菇(蚂蚁洞)",
            "50-70": "雪吉拉(冰原雪域)",
            "70-100": "蜥蜴王(宁静沼泽)",
        },
    },
    "黑骑士": {
        "type": "physical",
        "primary": 950,       # STR
        "secondary": 400,    # DEX
        "attack": 180,
        "mastery": 0.85,
        "aoe": 3,
        "skill_damage": 250,
        "heal_skill": False,
        "vampire": 0.15,      # 15%吸血
        "potion_reduce": 0.4,
        "survivability": 5,
        "potion_cost_base": 0.3,
        "equip_cost": 1.2,
        "skill_name": "暗蚀/仲裁",
        "best_grind": {
            "1-30": "木妖(森林入口)",
            "30-50": "僵尸蘑菇(废弃都市)",
            "50-70": "火肥肥(火焰之地)",
            "70-100": "土龙(宁静沼泽)",
        },
    },
    "神射手": {
        "type": "physical",
        "primary": 900,       # DEX
        "secondary": 450,
        "attack": 165,
        "mastery": 0.85,
        "aoe": 5,
        "skill_damage": 220,
        "heal_skill": False,
        "potion_reduce": 0.2,
        "survivability": 3,
        "potion_cost_base": 0.5,
        "equip_cost": 1.0,
        "skill_name": "暴风箭雨",
        "best_grind": {
            "1-30": "绿菇菇(射手村)",
            "30-50": "刺菇菇(蚂蚁洞)",
            "50-70": "独角狮(天空之城)",
            "70-100": "蜥蜴王(宁静沼泽)",
        },
    },
    "双刀": {
        "type": "physical",
        "primary": 850,       # LUK
        "secondary": 500,
        "attack": 160,
        "mastery": 0.85,
        "aoe": 4,
        "skill_damage": 200,
        "heal_skill": False,
        "stealth": True,     # 隐身保命
        "potion_reduce": 0.3,
        "survivability": 4,
        "potion_cost_base": 0.4,
        "equip_cost": 0.9,
        "skill_name": "撕裂/隐身",
        "best_grind": {
            "1-30": "绿菇菇(射手村)",
            "30-50": "大幽灵(废弃都市)",
            "50-70": "雪吉拉(冰原雪域)",
            "70-100": "巫婆(神木村)",
        },
    },
}

# ========== 药水价格 (枫币) ==========
POTION_PRICE = {
    "红药水(小)": 100,      # 恢复200HP
    "蓝药水(小)": 100,      # 恢复200MP
    "红药水(中)": 300,      # 恢复500HP
    "蓝药水(中)": 300,      # 恢复500MP
    "红药水(大)": 1000,     # 恢复1200HP
    "蓝药水(大)": 1000,     # 恢复1200MP
}

def calc_damage(class_data, monster_def):
    """计算每秒伤害"""
    if class_data["type"] == "magic":
        base = ((class_data["attack"]**2 / 1000 + class_data["attack"]) / 30 + class_data["primary"] / 200)
        damage = base * class_data["attack"] * class_data["mastery"]
    else:
        damage = (class_data["primary"] * class_data.get("coefficient", 4.0) + class_data["secondary"]) * class_data["attack"] / 100
    
    # 防御减免
    effective = max(damage - monster_def * 0.5, damage * 0.1)
    return effective

def calc_kill_time(class_data, monster_hp, monster_def, class_dps):
    """计算击杀时间(秒)"""
    damage_per_hit = calc_damage(class_data, monster_def)
    # 考虑攻速 (约1秒1次攻击)
    dps = damage_per_hit
    return monster_hp / dps

def analyze_comprehensive(level_range, class_name, class_data, location_name, location_data):
    """综合分析"""
    monsters = location_data["怪物"]
    base_potion_cost = location_data.get("药水/小时", 5000)
    
    # 计算职业实际药水消耗
    potion_reduce = class_data.get("potion_reduce", 0)
    actual_potion_cost = base_potion_cost * (1 - potion_reduce) * class_data.get("potion_cost_base", 0.5)
    
    # 计算掉落收益
    drop_value_per_hour = sum(m[6] for m in monsters) / len(monsters) * 60  # 简化估算
    
    # 计算EXP效率
    avg_exp = sum(m[2] for m in monsters) / len(monsters)
    kills_per_hour = 3600 / max(1, sum(calc_kill_time(class_data, m[3], m[4], class_data) for m in monsters) / len(monsters))
    exp_per_hour = avg_exp * kills_per_hour
    
    # 净收益 = 掉落价值 - 药水消耗
    net_profit = drop_value_per_hour - actual_potion_cost
    
    return {
        "class": class_name,
        "location": location_name,
        "level_range": level_range,
        "exp_per_hour": exp_per_hour,
        "kills_per_hour": kills_per_hour,
        "drop_value_per_hour": drop_value_per_hour,
        "potion_cost_per_hour": actual_potion_cost,
        "net_profit_per_hour": net_profit,
        "survivability": class_data["survivability"],
        "best_grind": class_data["best_grind"].get(level_range, ""),
    }

def run_full_analysis():
    print("=" * 80)
    print("阿尔泰服 全面收益分析 v2")
    print("包含: 经验效率 + 药水消耗 + 怪物掉落 + 净收益")
    print("=" * 80)
    
    results = []
    
    for level_range in ["1-30", "30-50", "50-70", "70-100"]:
        # 选择对应等级段的地图
        if level_range == "1-30":
            locations = [("魔法密林", MONSTERS_FULL["魔法密林"])]
        elif level_range == "30-50":
            locations = [("废弃都市", MONSTERS_FULL["废弃都市"])]
        elif level_range == "50-70":
            locations = [("冰原雪域", MONSTERS_FULL["冰原雪域"])]
        else:
            locations = [("神木村", MONSTERS_FULL["神木村"])]
        
        for loc_name, loc_data in locations:
            for class_name, class_data in CLASSES_FULL.items():
                r = analyze_comprehensive(level_range, class_name, class_data, loc_name, loc_data)
                results.append(r)
    
    # 按净收益排序
    results.sort(key=lambda x: x["net_profit_per_hour"], reverse=True)
    
    print("\n" + "=" * 80)
    print("📊 各职业综合收益对比 (按净收益排序)")
    print("=" * 80)
    
    for r in results:
        profit_sign = "+" if r["net_profit_per_hour"] > 0 else ""
        print(f"\n【{r['class']}】({r['level_range']}级 @ {r['location']})")
        print(f"  推荐练级点: {r['best_grind']}")
        print(f"  每小时EXP: {r['exp_per_hour']:,.0f}")
        print(f"  怪物掉落价值: {r['drop_value_per_hour']:,.0f}/h")
        print(f"  药水消耗成本: {r['potion_cost_per_hour']:,.0f}/h")
        print(f"  净收益: {profit_sign}{r['net_profit_per_hour']:,.0f}/h")
        print(f"  生存能力: {'★' * r['survivability']}{'☆' * (5 - r['survivability'])}")
    
    # 按等级段分组输出最优
    print("\n" + "=" * 80)
    print("🏆 每个等级段的最优选择")
    print("=" * 80)
    
    for level_range in ["1-30", "30-50", "50-70", "70-100"]:
        level_results = [r for r in results if r["level_range"] == level_range]
        level_results.sort(key=lambda x: x["net_profit_per_hour"], reverse=True)
        best = level_results[0]
        print(f"\n【{level_range}级】")
        print(f"  最佳职业: {best['class']} @ {best['location']}")
        print(f"  净收益: {best['net_profit_per_hour']:,.0f}/h | EXP: {best['exp_per_hour']:,.0f}/h")
        
        # 显示牧师的特别优势
        if best['class'] == '牧师':
            print(f"  ⚠️ 牧师回血技能可抵消{best['potion_cost_per_hour']:,.0f}药水消耗!")

if __name__ == "__main__":
    run_full_analysis()
