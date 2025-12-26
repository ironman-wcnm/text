import streamlit as st
import pandas as pd

# 页面标题（与Excel标题一致）
st.title('2022年前3个月销售数据')

# 1. 数据加载（优化时间列解析，从第二行读取）
@st.cache_data
def load_data():
    excel_path = 'data.xlsx'
    df = pd.read_excel(excel_path, header=1, parse_dates=False)
    
    # 验证核心列
    required_cols = ['订单号', '城市', '顾客类型', '性别', '产品类型', '总价', '评分', '时间']
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        raise ValueError(f'Excel文件缺少必要列：{", ".join(missing_cols)}')
    
    # 处理日期列
    if '日期' in df.columns:
        try:
            df['日期'] = pd.to_datetime(df['日期'], errors='coerce')
        except:
            df['日期'] = df['日期']
    else:
        st.warning('Excel文件中未找到"日期"列，不影响销售数据统计')
    
    # 优化时间列解析（兼容多种格式）
    if '时间' in df.columns:
        df['时间'] = df['时间'].astype(str).str.strip().str.replace(' ', '').str.replace('：', ':')
        time_formats = ['%H:%M', '%H:%M:%S', '%I:%M %p', '%H-%M', '%H.%M', '%I-%M %p']
        df['小时'] = None
        
        for fmt in time_formats:
            try:
                parsed_time = pd.to_datetime(df['时间'], format=fmt, errors='coerce')
                df.loc[df['小时'].isna(), '小时'] = parsed_time.dt.hour
            except:
                continue
        
        # 提取数字 fallback
        if df['小时'].isna().any():
            import re
            def extract_hour(time_str):
                nums = re.findall(r'\d+', time_str)
                if nums:
                    hour = int(nums[0])
                    return hour if 0 <= hour <= 23 else None
                return None
            df.loc[df['小时'].isna(), '小时'] = df.loc[df['小时'].isna(), '时间'].apply(extract_hour)
        
        df['小时'] = df['小时'].fillna(0).astype(int)
    else:
        raise ValueError('Excel文件缺少"时间"列，无法生成小时销售额图表')
    
    # 过滤无效数据
    df = df.dropna(subset=['订单号', '总价'])
    df = df[df['总价'] > 0]
    return df

# 异常捕获
try:
    df = load_data()
    st.success('')
    valid_hour_count = df[df['小时'] >= 0].shape[0]
    st.info('')
except FileNotFoundError:
    st.error('❌ 错误：Excel文件未找到！')
    st.error('请确认：1. 文件路径为 D:/data.xlsx  2. 文件在D盘根目录  3. 文件名无错误')
except ValueError as e:
    st.error(f'❌ 错误：{str(e)}')
except Exception as e:
    st.error(f'❌ 读取失败：{str(e)}')
    st.info('建议检查：1. 第2行是否为列名  2. 时间列格式（如20:33、8:30）  3. 文件为.xlsx格式')
    st.stop()

# 2. 筛选组件
st.sidebar.header('筛选条件')
cities = df['城市'].unique()
selected_city = st.sidebar.multiselect('请选择城市', cities, default=cities)
customer_types = df['顾客类型'].unique()
selected_customer = st.sidebar.multiselect('请选择顾客类型', customer_types, default=customer_types)
genders = df['性别'].unique()
selected_gender = st.sidebar.multiselect('请选择性别', genders, default=genders)

# 3. 数据过滤
filtered_df = df[
    (df['城市'].isin(selected_city)) &
    (df['顾客类型'].isin(selected_customer)) &
    (df['性别'].isin(selected_gender))
]

# 4. 核心指标计算
total_sales = filtered_df['总价'].sum()
avg_rating = filtered_df['评分'].dropna().mean()
avg_order_sales = filtered_df['总价'].mean()

# 5. 核心指标展示
st.subheader('核心销售指标')
col1, col2, col3 = st.columns(3)
with col1:
    st.metric('总销售额', f'RMB¥{total_sales:,.0f}')
with col2:
    st.metric('顾客评分平均值', f'{avg_rating:.1f}★')
with col3:
    st.metric('每单平均销售额', f'RMB¥{avg_order_sales:.2f}')

# 6. 销售分布图表（扩大图形大小，优化布局）
st.subheader('销售分布分析')

# 增加图表高度，确保尺寸充足
col_chart1, col_chart2 = st.columns(2, gap="large")  # 增加列间距，视觉更舒适

# 6.1 产品类型销售额（横向柱状图，设置高度扩大尺寸）
with col_chart1:
    st.subheader('按产品类型划分的销售额')
    product_sales = filtered_df.groupby('产品类型')['总价'].sum().sort_values(ascending=True)
    product_df = product_sales.reset_index()
    product_df.columns = ['产品类型', '销售额（RMB）']
    # 关键优化2：通过 height 参数设置图表高度，扩大图形尺寸
    st.bar_chart(
        product_df, 
        x='产品类型', 
        y='销售额（RMB）', 
        horizontal=True, 
        use_container_width=True,
        height=300  # 自定义高度，根据需求调整（推荐300-500）
    )

# 6.2 小时销售额（柱形图，设置高度扩大尺寸）
with col_chart2:
    st.subheader('按小时数划分的销售额')
    hourly_sales = filtered_df.groupby('小时')['总价'].sum()
    hourly_df = pd.DataFrame(index=range(24), columns=['销售额（RMB）'])
    hourly_df['销售额（RMB）'] = hourly_df.index.map(lambda x: hourly_sales.get(x, 0))
    hourly_df.reset_index(inplace=True)
    hourly_df.rename(columns={'index': '小时数'}, inplace=True)
    
    #设置 height 参数扩大图表高度
    st.bar_chart(
        hourly_df, 
        x='小时数', 
        y='销售额（RMB）', 
        use_container_width=True,
        height=300
    )
    
    # 补充说明
    non_zero_hours = hourly_df[hourly_df['销售额（RMB）'] > 0].shape[0]
    st.text(f'📊 有销售额的时段：{non_zero_hours} 个小时')


