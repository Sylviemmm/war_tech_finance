import pandas as pd
import os
from datetime import datetime

# 数据文件路径
data_dir = "E:\\工作学习文档\\网研所INS\\研一\\研一S2\\vibe coding\\数据文档\\战争-来源：correlatesofwar"
output_dir = "d:\\工作学习文档\\网研所INS\\研一\\研一S2\\vibe coding\\processed_data"

# 创建输出目录
os.makedirs(output_dir, exist_ok=True)

# 战争类型映射
war_type_mapping = {
    1: "Inter-State War (国家间战争)",
    2: "Extra-State War (国家对外战争)",
    3: "Extra-State War (国家对外战争)",
    4: "Intra-State War (国内战争-中央政府)",
    5: "Intra-State War (国内战争-地方政府)",
    6: "Intra-State War (国内战争-非政府)",
    7: "Intra-State War (国内战争-非政府)",
    8: "Non-State War (非国家战争)"
}

# 结果映射
outcome_mapping = {
    1: "胜利 (Victory)",
    2: "失败 (Defeat)",
    3: "妥协 (Compromise)",
    4: "转型 (Transformed)",
    5: "继续 (Ongoing)",
    6: "僵局 (Stalemate)",
    7: "释放 (Released)",
    8: "未知 (Unknown)"
}

# 地理区域映射
where_fought_mapping = {
    1: "北美 (North America)",
    2: "西欧 (Western Europe)",
    3: "东欧 (Eastern Europe)",
    4: "拉美 (Latin America)",
    5: "撒哈拉以南非洲 (Sub-Saharan Africa)",
    6: "中东/北非 (Middle East/North Africa)",
    7: "亚洲 (Asia)",
    8: "大洋洲 (Oceania)",
    9: "跨地区 (Multi-regional)"
}

def parse_date(year, month, day):
    """解析日期，处理缺失值"""
    try:
        if pd.isna(year) or year == -8 or year == -9:
            return None
        year = int(year)
        month = int(month) if not pd.isna(month) and month not in [-8, -9] else 1
        day = int(day) if not pd.isna(day) and day not in [-8, -9] else 1
        # 处理无效日期
        if month < 1 or month > 12:
            month = 1
        if day < 1 or day > 31:
            day = 1
        return f"{year:04d}-{month:02d}-{day:02d}"
    except:
        return None

def process_inter_state_wars():
    """处理国家间战争数据"""
    print("处理国家间战争数据 (Inter-State War)...")
    df = pd.read_csv(os.path.join(data_dir, "Inter-StateWarData_v4.0.csv"), encoding='latin-1')
    
    # 按战争编号分组，获取每场的唯一信息
    wars = []
    for war_num, group in df.groupby('WarNum'):
        war_info = {
            'war_id': f"IS{war_num}",
            'war_name': group['WarName'].iloc[0],
            'war_type': war_type_mapping.get(group['WarType'].iloc[0], "Unknown"),
            'war_type_code': int(group['WarType'].iloc[0]),
            'start_date': parse_date(
                group['StartYear1'].iloc[0],
                group['StartMonth1'].iloc[0],
                group['StartDay1'].iloc[0]
            ),
            'end_date': parse_date(
                group['EndYear1'].iloc[0] if group['EndYear1'].iloc[0] != -8 else None,
                group['EndMonth1'].iloc[0] if group['EndMonth1'].iloc[0] != -8 else None,
                group['EndDay1'].iloc[0] if group['EndDay1'].iloc[0] != -8 else None
            ),
            'belligerents_side1': [],
            'belligerents_side2': [],
            'initiator': None,
            'outcome': None,
            'total_deaths': 0,
            'where_fought': where_fought_mapping.get(group['WhereFought'].iloc[0], "Unknown"),
            'source_file': 'Inter-StateWarData_v4.0.csv'
        }
        
        # 收集参与方
        for _, row in group.iterrows():
            country = row['StateName']
            side = row['Side']
            deaths = row['BatDeath'] if row['BatDeath'] not in [-8, -9] else 0
            
            if side == 1:
                war_info['belligerents_side1'].append(country)
                if row['Initiator'] == 1:
                    war_info['initiator'] = country
                if row['Outcome'] in [1, 2, 3, 4, 5, 6, 7, 8]:
                    war_info['outcome'] = outcome_mapping.get(row['Outcome'], "Unknown")
            else:
                war_info['belligerents_side2'].append(country)
                if row['Initiator'] == 2:
                    war_info['initiator'] = country
            
            if deaths > 0:
                war_info['total_deaths'] += deaths
        
        war_info['belligerents_side1'] = '; '.join(war_info['belligerents_side1'])
        war_info['belligerents_side2'] = '; '.join(war_info['belligerents_side2'])
        wars.append(war_info)
    
    result_df = pd.DataFrame(wars)
    result_df.to_csv(os.path.join(output_dir, "inter_state_wars_processed.csv"), index=False, encoding='utf-8-sig')
    print(f"  处理了 {len(wars)} 场国家间战争")
    return result_df

def process_extra_state_wars():
    """处理国家对外战争数据"""
    print("处理国家对外战争数据 (Extra-State War)...")
    df = pd.read_csv(os.path.join(data_dir, "Extra-StateWarData_v4.0.csv"), encoding='latin-1')
    
    wars = []
    for war_num, group in df.groupby('WarNum'):
        war_info = {
            'war_id': f"ES{war_num}",
            'war_name': group['WarName'].iloc[0],
            'war_type': war_type_mapping.get(group['WarType'].iloc[0], "Unknown"),
            'war_type_code': int(group['WarType'].iloc[0]),
            'start_date': parse_date(
                group['StartYear1'].iloc[0],
                group['StartMonth1'].iloc[0],
                group['StartDay1'].iloc[0]
            ),
            'end_date': parse_date(
                group['EndYear1'].iloc[0] if group['EndYear1'].iloc[0] != -8 else None,
                group['EndMonth1'].iloc[0] if group['EndMonth1'].iloc[0] != -8 else None,
                group['EndDay1'].iloc[0] if group['EndDay1'].iloc[0] != -8 else None
            ),
            'belligerents_side1': [],
            'belligerents_side2': [],
            'initiator': None,
            'outcome': None,
            'total_deaths': 0,
            'non_state_deaths': 0,
            'where_fought': where_fought_mapping.get(group['WhereFought'].iloc[0], "Unknown"),
            'source_file': 'Extra-StateWarData_v4.0.csv'
        }
        
        for _, row in group.iterrows():
            side_a = row['SideA'] if pd.notna(row['SideA']) and row['SideA'] != -8 else None
            side_b = row['SideB'] if pd.notna(row['SideB']) and row['SideB'] != -8 else None
            
            if side_a:
                war_info['belligerents_side1'].append(side_a)
            if side_b:
                war_info['belligerents_side2'].append(side_b)
            
            deaths = row['BatDeath'] if row['BatDeath'] not in [-8, -9] else 0
            non_state_deaths = row['NonStateDeaths'] if row['NonStateDeaths'] not in [-8, -9] else 0
            
            war_info['total_deaths'] += deaths
            war_info['non_state_deaths'] += non_state_deaths
            
            if row['Initiator'] == 1:
                war_info['initiator'] = side_a
            elif row['Initiator'] == 2:
                war_info['initiator'] = side_b
            
            if row['Outcome'] in [1, 2, 3, 4, 5, 6, 7, 8]:
                war_info['outcome'] = outcome_mapping.get(row['Outcome'], "Unknown")
        
        war_info['belligerents_side1'] = '; '.join(war_info['belligerents_side1'])
        war_info['belligerents_side2'] = '; '.join(war_info['belligerents_side2'])
        wars.append(war_info)
    
    result_df = pd.DataFrame(wars)
    result_df.to_csv(os.path.join(output_dir, "extra_state_wars_processed.csv"), index=False, encoding='utf-8-sig')
    print(f"  处理了 {len(wars)} 场国家对外战争")
    return result_df

def process_intra_state_wars():
    """处理国内战争数据"""
    print("处理国内战争数据 (Intra-State War)...")
    df = pd.read_csv(os.path.join(data_dir, "Intra-StateWarData_v4.1.csv"), encoding='latin-1')
    
    wars = []
    for war_num, group in df.groupby('WarNum'):
        war_info = {
            'war_id': f"IN{war_num}",
            'war_name': group['WarName'].iloc[0],
            'war_type': war_type_mapping.get(group['WarType'].iloc[0], "Unknown"),
            'war_type_code': int(group['WarType'].iloc[0]),
            'start_date': parse_date(
                group['StartYear1'].iloc[0],
                group['StartMonth1'].iloc[0],
                group['StartDay1'].iloc[0]
            ),
            'end_date': parse_date(
                group['EndYear1'].iloc[0] if group['EndYear1'].iloc[0] != -8 else None,
                group['EndMonth1'].iloc[0] if group['EndMonth1'].iloc[0] != -8 else None,
                group['EndDay1'].iloc[0] if group['EndDay1'].iloc[0] != -8 else None
            ),
            'belligerents_side1': [],
            'belligerents_side2': [],
            'initiator': None,
            'outcome': None,
            'side_a_deaths': 0,
            'side_b_deaths': 0,
            'total_deaths': 0,
            'where_fought': where_fought_mapping.get(group['WhereFought'].iloc[0], "Unknown"),
            'source_file': 'Intra-StateWarData_v4.1.csv'
        }
        
        for _, row in group.iterrows():
            side_a = row['SideA'] if pd.notna(row['SideA']) and row['SideA'] != -8 else None
            side_b = row['SideB'] if pd.notna(row['SideB']) and row['SideB'] != -8 else None
            
            if side_a:
                war_info['belligerents_side1'].append(side_a)
            if side_b:
                war_info['belligerents_side2'].append(side_b)
            
            side_a_deaths = int(str(row['SideADeaths']).replace(',', '')) if pd.notna(row['SideADeaths']) and row['SideADeaths'] not in [-8, -9] else 0
            side_b_deaths = int(str(row['SideBDeaths']).replace(',', '')) if pd.notna(row['SideBDeaths']) and row['SideBDeaths'] not in [-8, -9] else 0
            
            war_info['side_a_deaths'] += side_a_deaths
            war_info['side_b_deaths'] += side_b_deaths
            war_info['total_deaths'] += (side_a_deaths + side_b_deaths)
            
            if row['Initiator'] == 1:
                war_info['initiator'] = side_a
            elif row['Initiator'] == 2:
                war_info['initiator'] = side_b
            
            if row['Outcome'] in [1, 2, 3, 4, 5, 6, 7, 8]:
                war_info['outcome'] = outcome_mapping.get(row['Outcome'], "Unknown")
        
        war_info['belligerents_side1'] = '; '.join(war_info['belligerents_side1'])
        war_info['belligerents_side2'] = '; '.join(war_info['belligerents_side2'])
        wars.append(war_info)
    
    result_df = pd.DataFrame(wars)
    result_df.to_csv(os.path.join(output_dir, "intra_state_wars_processed.csv"), index=False, encoding='utf-8-sig')
    print(f"  处理了 {len(wars)} 场国内战争")
    return result_df

def process_non_state_wars():
    """处理非国家战争数据"""
    print("处理非国家战争数据 (Non-State War)...")
    df = pd.read_csv(os.path.join(data_dir, "Non-StateWarData_v4.0.csv"), encoding='latin-1')
    
    wars = []
    for war_num, group in df.groupby('WarNum'):
        war_info = {
            'war_id': f"NS{war_num}",
            'war_name': group['WarName'].iloc[0],
            'war_type': war_type_mapping.get(group['WarType'].iloc[0], "Unknown"),
            'war_type_code': int(group['WarType'].iloc[0]),
            'start_date': parse_date(
                group['StartYear'].iloc[0],
                group['StartMonth'].iloc[0],
                group['StartDay'].iloc[0]
            ),
            'end_date': parse_date(
                group['EndYear'].iloc[0] if group['EndYear'].iloc[0] != -9 else None,
                group['EndMonth'].iloc[0] if group['EndMonth'].iloc[0] != -9 else None,
                group['EndDay'].iloc[0] if group['EndDay'].iloc[0] != -9 else None
            ),
            'belligerents_side1': [],
            'belligerents_side2': [],
            'initiator': None,
            'outcome': None,
            'side_a_deaths': 0,
            'side_b_deaths': 0,
            'total_deaths': 0,
            'where_fought': where_fought_mapping.get(group['WhereFought'].iloc[0], "Unknown"),
            'source_file': 'Non-StateWarData_v4.0.csv'
        }
        
        for _, row in group.iterrows():
            side_a1 = row['SideA1'] if pd.notna(row['SideA1']) and row['SideA1'] != -8 else None
            side_a2 = row['SideA2'] if pd.notna(row['SideA2']) and row['SideA2'] != -8 else None
            side_b1 = row['SideB1'] if pd.notna(row['SideB1']) and row['SideB1'] != -8 else None
            side_b2 = row['SideB2'] if pd.notna(row['SideB2']) and row['SideB2'] != -8 else None
            side_b3 = row['SideB3'] if pd.notna(row['SideB3']) and row['SideB3'] != -8 else None
            side_b4 = row['SideB4'] if pd.notna(row['SideB4']) and row['SideB4'] != -8 else None
            side_b5 = row['SideB5'] if pd.notna(row['SideB5']) and row['SideB5'] != -8 else None
            
            if side_a1:
                war_info['belligerents_side1'].append(side_a1)
            if side_a2:
                war_info['belligerents_side1'].append(side_a2)
            if side_b1:
                war_info['belligerents_side2'].append(side_b1)
            if side_b2:
                war_info['belligerents_side2'].append(side_b2)
            if side_b3:
                war_info['belligerents_side2'].append(side_b3)
            if side_b4:
                war_info['belligerents_side2'].append(side_b4)
            if side_b5:
                war_info['belligerents_side2'].append(side_b5)
            
            side_a_deaths = row['SideADeaths'] if row['SideADeaths'] not in [-8, -9] else 0
            side_b_deaths = row['SideBDeaths'] if row['SideBDeaths'] not in [-8, -9] else 0
            
            war_info['side_a_deaths'] += max(0, side_a_deaths)
            war_info['side_b_deaths'] += max(0, side_b_deaths)
            war_info['total_deaths'] += max(0, side_a_deaths + side_b_deaths)
            
            initiator = row['Initiator']
            if initiator == 'A' or initiator == 'a':
                war_info['initiator'] = war_info['belligerents_side1'][0] if war_info['belligerents_side1'] else None
            elif initiator == 'B' or initiator == 'b':
                war_info['initiator'] = war_info['belligerents_side2'][0] if war_info['belligerents_side2'] else None
            
            if row['Outcome'] in [1, 2, 3, 4, 5, 6, 7, 8]:
                war_info['outcome'] = outcome_mapping.get(row['Outcome'], "Unknown")
        
        war_info['belligerents_side1'] = '; '.join(war_info['belligerents_side1'])
        war_info['belligerents_side2'] = '; '.join(war_info['belligerents_side2'])
        wars.append(war_info)
    
    result_df = pd.DataFrame(wars)
    result_df.to_csv(os.path.join(output_dir, "non_state_wars_processed.csv"), index=False, encoding='utf-8-sig')
    print(f"  处理了 {len(wars)} 场非国家战争")
    return result_df

def merge_all_wars():
    """合并所有战争数据"""
    print("\n合并所有战争数据...")
    
    inter_state = process_inter_state_wars()
    extra_state = process_extra_state_wars()
    intra_state = process_intra_state_wars()
    non_state = process_non_state_wars()
    
    # 标准化列名
    columns = ['war_id', 'war_name', 'war_type', 'war_type_code', 'start_date', 'end_date',
               'belligerents_side1', 'belligerents_side2', 'initiator', 'outcome',
               'total_deaths', 'where_fought', 'source_file']
    
    all_wars = []
    
    for df in [inter_state, extra_state, intra_state, non_state]:
        # 选择共同列
        available_cols = [col for col in columns if col in df.columns]
        df_subset = df[available_cols].copy()
        all_wars.append(df_subset)
    
    merged_df = pd.concat(all_wars, ignore_index=True)
    
    # 按开始日期排序
    merged_df = merged_df.sort_values('start_date')
    
    # 保存合并后的数据
    merged_df.to_csv(os.path.join(output_dir, "all_wars_merged.csv"), index=False, encoding='utf-8-sig')
    
    print(f"\n总共处理了 {len(merged_df)} 场战争")
    print(f"\n战争类型分布:")
    print(merged_df['war_type'].value_counts())
    print(f"\n地理分布:")
    print(merged_df['where_fought'].value_counts())
    
    # 统计信息
    print(f"\n数据统计:")
    print(f"  有明确开始日期的战争: {merged_df['start_date'].notna().sum()}")
    print(f"  有明确结束日期的战争: {merged_df['end_date'].notna().sum()}")
    print(f"  有伤亡数据的战争: {(merged_df['total_deaths'] > 0).sum()}")
    print(f"  总伤亡人数: {merged_df['total_deaths'].sum():,.0f}")
    
    return merged_df

if __name__ == "__main__":
    print("=" * 60)
    print("COW战争数据处理工具")
    print("=" * 60)
    
    merged_data = merge_all_wars()
    
    print("\n" + "=" * 60)
    print("处理完成！输出文件:")
    print(f"  - {os.path.join(output_dir, 'inter_state_wars_processed.csv')}")
    print(f"  - {os.path.join(output_dir, 'extra_state_wars_processed.csv')}")
    print(f"  - {os.path.join(output_dir, 'intra_state_wars_processed.csv')}")
    print(f"  - {os.path.join(output_dir, 'non_state_wars_processed.csv')}")
    print(f"  - {os.path.join(output_dir, 'all_wars_merged.csv')}")
    print("=" * 60)
