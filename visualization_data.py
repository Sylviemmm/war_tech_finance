import pandas as pd
import json
from collections import defaultdict

# 读取数据
df = pd.read_csv('processed_data/all_wars_merged.csv', encoding='utf-8-sig')

# 1. 按地区统计战争数量和死亡人数
region_stats = df.groupby('where_fought').agg({
    'war_id': 'count',
    'total_deaths': 'sum'
}).reset_index()
region_stats.columns = ['region', 'war_count', 'total_deaths']
region_stats = region_stats[region_stats['region'] != 'Unknown']

# 2. 按战争类型统计
war_type_stats = df.groupby('war_type').agg({
    'war_id': 'count',
    'total_deaths': 'sum'
}).reset_index()
war_type_stats.columns = ['war_type', 'count', 'deaths']

# 3. 按年份统计（每十年）
df['start_year'] = pd.to_datetime(df['start_date'], errors='coerce').dt.year
df['decade'] = (df['start_year'] // 10) * 10
decade_stats = df.groupby('decade').agg({
    'war_id': 'count',
    'total_deaths': 'sum'
}).reset_index()
decade_stats = decade_stats[decade_stats['decade'] >= 1800]

# 4. 按结果统计
outcome_stats = df[df['outcome'].notna()].groupby('outcome').size().reset_index(name='count')

# 5. 最致命的战争（前20）
deadliest_wars = df.nlargest(20, 'total_deaths')[['war_name', 'war_type', 'start_date', 'total_deaths', 'where_fought']]

# 6. 地理坐标映射（用于热力图）
region_coords = {
    '北美 (North America)': {'lat': 45, 'lon': -100, 'wars': 0, 'deaths': 0},
    '西欧 (Western Europe)': {'lat': 50, 'lon': 10, 'wars': 0, 'deaths': 0},
    '东欧 (Eastern Europe)': {'lat': 55, 'lon': 30, 'wars': 0, 'deaths': 0},
    '拉美 (Latin America)': {'lat': -15, 'lon': -60, 'wars': 0, 'deaths': 0},
    '撒哈拉以南非洲 (Sub-Saharan Africa)': {'lat': -5, 'lon': 20, 'wars': 0, 'deaths': 0},
    '中东/北非 (Middle East/North Africa)': {'lat': 30, 'lon': 35, 'wars': 0, 'deaths': 0},
    '亚洲 (Asia)': {'lat': 35, 'lon': 100, 'wars': 0, 'deaths': 0},
    '大洋洲 (Oceania)': {'lat': -25, 'lon': 135, 'wars': 0, 'deaths': 0},
    '跨地区 (Multi-regional)': {'lat': 0, 'lon': 0, 'wars': 0, 'deaths': 0}
}

for _, row in region_stats.iterrows():
    region = row['region']
    if region in region_coords:
        region_coords[region]['wars'] = int(row['war_count'])
        region_coords[region]['deaths'] = int(row['total_deaths'])

# 7. 战争持续时间分析
df['start_dt'] = pd.to_datetime(df['start_date'], errors='coerce')
df['end_dt'] = pd.to_datetime(df['end_date'], errors='coerce')
df['duration_days'] = (df['end_dt'] - df['start_dt']).dt.days
duration_stats = df[df['duration_days'].notna() & (df['duration_days'] > 0)]

# 8. 发起方统计（前15）
initiator_stats = df[df['initiator'].notna()].groupby('initiator').agg({
    'war_id': 'count',
    'total_deaths': 'sum'
}).reset_index()
initiator_stats.columns = ['initiator', 'war_count', 'total_deaths']
initiator_stats = initiator_stats.nlargest(15, 'war_count')

# 准备可视化数据
visualization_data = {
    'region_data': region_stats.to_dict('records'),
    'war_type_data': war_type_stats.to_dict('records'),
    'decade_data': decade_stats.to_dict('records'),
    'outcome_data': outcome_stats.to_dict('records'),
    'deadliest_wars': deadliest_wars.to_dict('records'),
    'heatmap_data': region_coords,
    'initiator_data': initiator_stats.to_dict('records'),
    'summary': {
        'total_wars': int(len(df)),
        'total_deaths': int(df['total_deaths'].sum()),
        'avg_deaths_per_war': int(df['total_deaths'].mean()),
        'date_range': f"{int(df['start_year'].min())}-{int(df['start_year'].max())}"
    }
}

# 保存为JSON
with open('visualization_data.json', 'w', encoding='utf-8') as f:
    json.dump(visualization_data, f, ensure_ascii=False, indent=2)

print("可视化数据准备完成！")
print(f"总计战争数: {visualization_data['summary']['total_wars']}")
print(f"总计死亡人数: {visualization_data['summary']['total_deaths']:,}")
print(f"时间跨度: {visualization_data['summary']['date_range']}")
