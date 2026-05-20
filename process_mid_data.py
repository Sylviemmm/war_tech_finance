"""
MID数据集处理脚本
处理MID 5.0数据并合并坐标信息
"""

import pandas as pd
import numpy as np
import json
from datetime import datetime

# 数据文件路径
MIDA_FILE = 'war_data/MID-5-Data-and-Supporting-Materials/MIDA 5.0.csv'
MIDB_FILE = 'war_data/MID-5-Data-and-Supporting-Materials/MIDB 5.0.csv'
MIDI_FILE = 'war_data/MID-5-Data-and-Supporting-Materials/MIDI 5.0.csv'
MIDIP_FILE = 'war_data/MID-5-Data-and-Supporting-Materials/MIDIP 5.0.csv'
MIDLOCA_FILE = 'war_data/MIDLOC_2.1/MIDLOCA_2.1.csv'
MIDLOCI_FILE = 'war_data/MIDLOC_2.1/MIDLOCI_2.1.csv'

# 战争类型映射（基于hostlev和action字段）
def get_war_type(row):
    """根据MID数据确定战争类型"""
    hostlev = row.get('hostlev', 1)
    action = row.get('action', 0)
    
    # 根据hostlev（敌意等级）分类
    if hostlev >= 4:  # 战争级别
        return 1, "Inter-State War"
    elif hostlev == 3:  # 使用武力
        return 2, "Extra-State War"
    elif hostlev == 2:  # 威胁使用武力
        return 3, "Intra-State War"
    else:  # 无军事行动
        return 4, "Non-State Conflict"

# 伤亡等级映射
def get_fatality_level(fatality):
    """将伤亡代码转换为数值"""
    fatality_map = {
        0: 0,      # 无伤亡
        1: 1,      # 1-25人
        2: 25,     # 26-100人
        3: 100,    # 101-250人
        4: 250,    # 251-500人
        5: 500,    # 501-999人
        6: 1000    # 1000+人
    }
    return fatality_map.get(fatality, 0)

# 读取数据
print("读取MID数据文件...")
mida_df = pd.read_csv(MIDA_FILE, encoding='utf-8-sig')
midb_df = pd.read_csv(MIDB_FILE, encoding='utf-8-sig')
midi_df = pd.read_csv(MIDI_FILE, encoding='utf-8-sig')
midip_df = pd.read_csv(MIDIP_FILE, encoding='utf-8-sig')
midloca_df = pd.read_csv(MIDLOCA_FILE, encoding='latin-1')
midloci_df = pd.read_csv(MIDLOCI_FILE, encoding='latin-1')

print(f"MIDA: {len(mida_df)} 条记录")
print(f"MIDB: {len(midb_df)} 条记录")
print(f"MIDI: {len(midi_df)} 条记录")
print(f"MIDIP: {len(midip_df)} 条记录")
print(f"MIDLOCA: {len(midloca_df)} 条记录")
print(f"MIDLOCI: {len(midloci_df)} 条记录")

# 处理MIDA数据（争端级别）
print("\n处理争端数据...")
disputes = []

for _, row in mida_df.iterrows():
    dispnum = row['dispnum']
    
    # 获取战争类型
    war_type_code, war_type_name = get_war_type(row)
    
    # 处理日期
    try:
        start_year = int(row['styear']) if row['styear'] > 0 else None
        start_month = int(row['stmon']) if row['stmon'] > 0 else 1
        start_day = int(row['stday']) if row['stday'] > 0 else 1
        
        end_year = int(row['endyear']) if row['endyear'] > 0 else start_year
        end_month = int(row['endmon']) if row['endmon'] > 0 else start_month
        end_day = int(row['endday']) if row['endday'] > 0 else start_day
        
        start_date = f"{start_year:04d}-{start_month:02d}-{start_day:02d}" if start_year else None
        end_date = f"{end_year:04d}-{end_month:02d}-{end_day:02d}" if end_year else None
    except:
        start_date = None
        end_date = None
    
    # 伤亡数
    fatality = row.get('fatality', 0)
    total_deaths = get_fatality_level(fatality)
    
    dispute = {
        'dispnum': dispnum,
        'war_type_code': war_type_code,
        'war_type': war_type_name,
        'start_date': start_date,
        'end_date': end_date,
        'start_year': start_year,
        'end_year': end_year,
        'duration': row.get('maxdur', 0),
        'total_deaths': total_deaths,
        'fatality_code': fatality,
        'hostlev': row.get('hostlev', 1),
        'outcome': row.get('outcome', 0),
        'settle': row.get('settle', 0),
        'numa': row.get('numa', 0),
        'numb': row.get('numb', 0)
    }
    disputes.append(dispute)

disputes_df = pd.DataFrame(disputes)
print(f"处理完成: {len(disputes_df)} 个争端")

# 处理MIDB数据（参与者信息）
print("\n处理参与者数据...")
participants = {}

for _, row in midb_df.iterrows():
    dispnum = row['dispnum']
    
    if dispnum not in participants:
        participants[dispnum] = {
            'side_a': [],
            'side_b': [],
            'initiator': None
        }
    
    country = row['stabb']
    side_a = row['sidea']
    orig = row['orig']
    
    if side_a == 1:
        participants[dispnum]['side_a'].append(country)
    else:
        participants[dispnum]['side_b'].append(country)
    
    # 记录发起方
    if orig == 1:
        participants[dispnum]['initiator'] = country

# 处理MIDLOCA数据（坐标信息）
print("\n处理坐标数据...")
coordinates = {}

for _, row in midloca_df.iterrows():
    dispnum = row['dispnum']
    
    if dispnum not in coordinates:
        coordinates[dispnum] = {
            'locations': [],
            'lat': None,
            'lon': None,
            'location_name': None
        }
    
    lat = row.get('midloc2_ylatitude')
    lon = row.get('midloc2_xlongitude')
    location = row.get('midloc2_location', '')
    
    # 只使用有效的坐标
    if pd.notna(lat) and pd.notna(lon) and lat != -99 and lon != -99:
        coordinates[dispnum]['locations'].append({
            'lat': float(lat),
            'lon': float(lon),
            'name': location,
            'precision': row.get('midloc2_precision', 0)
        })
        
        # 使用第一个有效坐标作为主坐标
        if coordinates[dispnum]['lat'] is None:
            coordinates[dispnum]['lat'] = float(lat)
            coordinates[dispnum]['lon'] = float(lon)
            coordinates[dispnum]['location_name'] = location

# 合并所有数据
print("\n合并数据...")
war_points = []

for _, dispute in disputes_df.iterrows():
    dispnum = dispute['dispnum']
    
    # 获取参与者信息
    participant_info = participants.get(dispnum, {
        'side_a': [],
        'side_b': [],
        'initiator': None
    })
    
    # 获取坐标信息
    coord_info = coordinates.get(dispnum, {
        'lat': 20,
        'lon': 0,
        'location_name': 'Unknown'
    })
    
    # 如果坐标缺失，使用默认值
    if coord_info['lat'] is None:
        coord_info['lat'] = 20
        coord_info['lon'] = 0
        coord_info['location_name'] = 'Unknown'
    
    # 计算点大小和颜色
    size = max(5, min(25, 5 + dispute['total_deaths'] / 50))
    
    # 战争类型颜色
    WAR_TYPE_COLORS = {
        1: '#ff6b6b',  # Inter-State War - 红色
        2: '#4ecdc4',  # Extra-State War - 青色
        3: '#45b7d1',  # Intra-State War - 蓝色
        4: '#96ceb4'   # Non-State Conflict - 绿色
    }
    
    base_color = WAR_TYPE_COLORS.get(dispute['war_type_code'], '#ff6b6b')
    
    # 根据伤亡数调整颜色深度
    if dispute['total_deaths'] == 0:
        color = base_color + '40'  # 透明
    else:
        max_deaths = 1000
        depth = min(1.0, dispute['total_deaths'] / max_deaths)
        alpha = int(40 + depth * 215)
        r = int(base_color[1:3], 16)
        g = int(base_color[3:5], 16)
        b = int(base_color[5:7], 16)
        color = f'rgba({r}, {g}, {b}, {alpha/255})'
    
    war_point = {
        'dispnum': dispnum,
        'war_name': f"MID {dispnum}",
        'war_type_code': dispute['war_type_code'],
        'war_type': dispute['war_type'],
        'start_date': dispute['start_date'] or '',
        'end_date': dispute['end_date'] or '',
        'start_year': dispute['start_year'] or 0,
        'duration': dispute['duration'],
        'total_deaths': dispute['total_deaths'],
        'fatality_code': dispute['fatality_code'],
        'hostlev': dispute['hostlev'],
        'outcome': dispute['outcome'],
        'side_a': '; '.join(participant_info['side_a']),
        'side_b': '; '.join(participant_info['side_b']),
        'initiator': participant_info['initiator'] or 'Unknown',
        'numa': dispute['numa'],
        'numb': dispute['numb'],
        'lat': coord_info['lat'],
        'lon': coord_info['lon'],
        'location_name': coord_info['location_name'],
        'color': color,
        'size': size
    }
    
    war_points.append(war_point)

# 创建统计信息
stats = {
    'total_wars': len(war_points),
    'total_deaths': sum(wp['total_deaths'] for wp in war_points),
    'date_range': f"{min(wp['start_year'] for wp in war_points if wp['start_year'] > 0)}-{max(wp['start_year'] for wp in war_points if wp['start_year'] > 0)}",
    'war_types': {
        1: "Inter-State War",
        2: "Extra-State War",
        3: "Intra-State War",
        4: "Non-State Conflict"
    },
    'war_type_colors': {
        1: '#ff6b6b',
        2: '#4ecdc4',
        3: '#45b7d1',
        4: '#96ceb4'
    },
    'war_points': war_points
}

# 保存为JSON
output_file = 'mid_visualization_data.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(stats, f, ensure_ascii=False, indent=2)

print(f"\n数据处理完成！")
print(f"总计争端数: {stats['total_wars']}")
print(f"总计伤亡等级: {stats['total_deaths']}")
print(f"时间跨度: {stats['date_range']}")
print(f"数据已保存到: {output_file}")

# 保存为CSV便于查看
csv_file = 'mid_war_points.csv'
war_points_df = pd.DataFrame(war_points)
war_points_df.to_csv(csv_file, index=False, encoding='utf-8-sig')
print(f"CSV数据已保存到: {csv_file}")

# 显示战争类型分布
print("\n战争类型分布:")
type_counts = war_points_df['war_type'].value_counts()
for war_type, count in type_counts.items():
    print(f"  {war_type}: {count}")

# 显示地区分布（前10）
print("\n地区分布（前10）:")
location_counts = war_points_df['location_name'].value_counts().head(10)
for location, count in location_counts.items():
    print(f"  {location}: {count}")