import pandas as pd
import json
import numpy as np
from datetime import datetime

# 读取数据
df = pd.read_csv('processed_data/all_wars_merged.csv', encoding='utf-8-sig')

# 战争类型颜色映射
WAR_TYPE_COLORS = {
    1: '#ff6b6b',  # 国家间战争 - 红色系
    2: '#4ecdc4',  # 国家对外战争 - 青色系
    3: '#45b7d1',  # 国家对外战争 - 蓝色系
    4: '#96ceb4',  # 国内战争-中央政府 - 绿色系
    5: '#feca57',  # 国内战争-地方政府 - 黄色系
    6: '#ff9ff3',  # 国内战争-非政府 - 粉色系
    7: '#54a0ff',  # 国内战争-非政府 - 深蓝色
    8: '#5f27cd',  # 非国家战争 - 紫色
    9: '#ff6b6b'   # 未知类型 - 使用红色系
}

# 战争类型名称映射
WAR_TYPE_NAMES = {
    1: "Inter-State War",
    2: "Extra-State War",
    3: "Extra-State War",
    4: "Intra-State War (Central)",
    5: "Intra-State War (Local)",
    6: "Intra-State War (Non-Gov)",
    7: "Intra-State War (Non-Gov)",
    8: "Non-State War"
}

# 地理坐标映射（基于地区）
REGION_COORDS = {
    '北美 (North America)': {'lat': 40, 'lon': -100},
    '西欧 (Western Europe)': {'lat': 50, 'lon': 10},
    '东欧 (Eastern Europe)': {'lat': 55, 'lon': 30},
    '拉美 (Latin America)': {'lat': -15, 'lon': -60},
    '撒哈拉以南非洲 (Sub-Saharan Africa)': {'lat': -5, 'lon': 20},
    '中东/北非 (Middle East/North Africa)': {'lat': 30, 'lon': 35},
    '亚洲 (Asia)': {'lat': 35, 'lon': 100},
    '大洋洲 (Oceania)': {'lat': -25, 'lon': 135},
    '跨地区 (Multi-regional)': {'lat': 20, 'lon': 0}
}

# 为每个战争生成精确的地理坐标
def get_war_coordinates(row):
    """为战争生成精确的地理坐标"""
    region = row.get('where_fought', 'Unknown')
    
    if region in REGION_COORDS:
        base_coords = REGION_COORDS[region]
        
        # 添加一些随机偏移，使战争点不会完全重叠
        if region == '跨地区 (Multi-regional)':
            # 跨地区战争使用多个坐标点
            coords = []
            for i in range(min(3, len(row.get('belligerents_side1', '').split('; ')) + len(row.get('belligerents_side2', '').split('; ')))):
                coords.append({
                    'lat': base_coords['lat'] + np.random.uniform(-10, 10),
                    'lon': base_coords['lon'] + np.random.uniform(-20, 20)
                })
            return coords
        else:
            # 单一地区战争添加随机偏移
            return [{
                'lat': base_coords['lat'] + np.random.uniform(-5, 5),
                'lon': base_coords['lon'] + np.random.uniform(-10, 10)
            }]
    else:
        # 未知地区使用世界中心
        return [{'lat': 20, 'lon': 0}]

# 计算颜色深度（基于伤亡数）
def get_death_color(deaths, war_type_code):
    """根据伤亡数和战争类型计算颜色"""
    if pd.isna(deaths) or deaths == 0:
        return WAR_TYPE_COLORS[war_type_code] + '40'  # 透明
    
    # 计算颜色深度（0-1）
    max_deaths = df['total_deaths'].max()
    min_deaths = df[df['total_deaths'] > 0]['total_deaths'].min()
    
    if deaths <= min_deaths:
        depth = 0.3
    elif deaths >= max_deaths:
        depth = 1.0
    else:
        depth = 0.3 + 0.7 * (deaths - min_deaths) / (max_deaths - min_deaths)
    
    # 将深度转换为透明度
    alpha = int(40 + depth * 215)  # 40-255
    
    # 获取基础颜色
    base_color = WAR_TYPE_COLORS[war_type_code]
    
    # 转换为RGBA
    if base_color.startswith('#'):
        r = int(base_color[1:3], 16)
        g = int(base_color[3:5], 16)
        b = int(base_color[5:7], 16)
        return f'rgba({r}, {g}, {b}, {alpha/255})'
    
    return base_color

# 计算点大小（基于伤亡数）
def get_point_size(deaths):
    """根据伤亡数计算点大小"""
    if pd.isna(deaths) or deaths == 0:
        return 5
    
    max_deaths = df['total_deaths'].max()
    min_deaths = df[df['total_deaths'] > 0]['total_deaths'].min()
    
    if deaths <= min_deaths:
        size = 8
    elif deaths >= max_deaths:
        size = 25
    else:
        size = 8 + 17 * (deaths - min_deaths) / (max_deaths - min_deaths)
    
    return int(size)

# 准备战争点数据
war_points = []
for _, row in df.iterrows():
    coordinates = get_war_coordinates(row)
    
    for coord in coordinates:
        point = {
            'war_id': row.get('war_id', ''),
            'war_name': row.get('war_name', ''),
            'war_type_code': row.get('war_type_code', 1),
            'war_type': WAR_TYPE_NAMES.get(row.get('war_type_code', 1), 'Unknown'),
            'start_date': row.get('start_date', ''),
            'end_date': row.get('end_date', ''),
            'start_year': int(row.get('start_date', '').split('-')[0]) if row.get('start_date') else '',
            'total_deaths': int(row.get('total_deaths', 0)),
            'belligerents_side1': row.get('belligerents_side1', ''),
            'belligerents_side2': row.get('belligerents_side2', ''),
            'initiator': row.get('initiator', ''),
            'outcome': row.get('outcome', ''),
            'where_fought': row.get('where_fought', ''),
            'lat': coord['lat'],
            'lon': coord['lon'],
            'color': get_death_color(row.get('total_deaths', 0), row.get('war_type_code', 1)),
            'size': get_point_size(row.get('total_deaths', 0))
        }
        war_points.append(point)

# 统计数据
stats = {
    'total_wars': len(df),
    'total_deaths': int(df['total_deaths'].sum()),
    'avg_deaths_per_war': int(df['total_deaths'].mean()),
    'date_range': f"{int(df['start_date'].str.split('-').str[0].min())}-{int(df['start_date'].str.split('-').str[0].max())}",
    'war_types': WAR_TYPE_NAMES,
    'war_type_colors': WAR_TYPE_COLORS,
    'war_points': war_points,
    'region_stats': df.groupby('where_fought').agg({
        'war_id': 'count',
        'total_deaths': 'sum'
    }).reset_index().to_dict('records')
}

# 保存为JSON
with open('visualization_data_detailed.json', 'w', encoding='utf-8') as f:
    json.dump(stats, f, ensure_ascii=False, indent=2)

print("详细可视化数据准备完成！")
print(f"总计战争数: {stats['total_wars']}")
print(f"总计死亡人数: {stats['total_deaths']:,}")
print(f"时间跨度: {stats['date_range']}")
print(f"战争点数: {len(stats['war_points'])}")
