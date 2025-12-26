import streamlit as st
import pandas as pd

# -------------------------- 页面全局配置 --------------------------
# 设置宽布局，适配左右分栏
st.set_page_config(
    page_title="Excel数据筛选查询页面",
    layout="wide",
    page_icon="📄"
)

# -------------------------- 数据加载（缓存） --------------------------
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
        st.warning('Excel文件中未找到"日期"列，不影响数据展示')
    
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
        st.warning('Excel文件中未找到"时间"列，不影响数据展示')
    
    # 过滤无效数据
    df = df.dropna(subset=['订单号', '总价'])
    df = df[df['总价'] > 0]
    return df

# -------------------------- 异常捕获加载数据 --------------------------
try:
    df = load_data()
    st.success(f'')
except FileNotFoundError:
    st.error('❌ 错误：Excel文件未找到！')
    st.error('请确认：1. 文件路径为 D:/data.xlsx  2. 文件在D盘根目录  3. 文件名无错误')
    st.stop()
except ValueError as e:
    st.error(f'❌ 错误：{str(e)}')
    st.stop()
except Exception as e:
    st.error(f'❌ 读取失败：{str(e)}')
    st.info('建议检查：1. 第2行是否为列名  2. 文件为.xlsx格式')
    st.stop()

# -------------------------- 核心布局：左侧筛选 + 右侧数据展示 --------------------------
st.title('Excel原始数据筛选查询界面')
# 左右分栏：左侧1/3（筛选），右侧2/3（数据展示）
filter_col, data_col = st.columns([1, 2], gap="medium")

# -------------------------- 左侧：筛选条件区域 --------------------------
with filter_col:
    st.header('🔍 筛选条件')
    # 城市筛选
    cities = df['城市'].unique()
    selected_city = st.multiselect('城市', cities, default=cities, key="data_filter_city")
    
    # 顾客类型筛选
    customer_types = df['顾客类型'].unique()
    selected_customer = st.multiselect('顾客类型', customer_types, default=customer_types, key="data_filter_customer")
    
    # 性别筛选
    genders = df['性别'].unique()
    selected_gender = st.multiselect('性别', genders, default=genders, key="data_filter_gender")
    
    # 产品类型筛选
    product_types = df['产品类型'].unique()
    selected_product = st.multiselect('产品类型', product_types, default=product_types, key="data_filter_product")

# -------------------------- 右侧：Excel数据展示区域 --------------------------
with data_col:
    st.header('📄 筛选后Excel数据展示')
    
    # 多条件数据过滤
    filtered_data = df[
        (df['城市'].isin(selected_city)) &
        (df['顾客类型'].isin(selected_customer)) &
        (df['性别'].isin(selected_gender)) &
        (df['产品类型'].isin(selected_product))
    ]
    
    # 展示数据统计信息
    st.info(f'')
    
    # 交互式数据展示（隐藏辅助列、自定义格式）
    st.dataframe(
        filtered_data.drop(columns=['小时']),  # 隐藏辅助计算的"小时"列，仅展示原始Excel列
        use_container_width=True,
        hide_index=True,  # 隐藏行索引，贴近Excel样式
        column_config={
            "总价": st.column_config.NumberColumn("订单总价（RMB）", format="¥%.2f"),
            "评分": st.column_config.NumberColumn("顾客评分", format="%.1f★"),
            "日期": st.column_config.DateColumn("订单日期", format="YYYY-MM-DD"),
            "时间": st.column_config.TextColumn("订单时间"),
            "订单号": st.column_config.TextColumn("订单编号"),
            "城市": st.column_config.TextColumn("城市"),
            "顾客类型": st.column_config.TextColumn("顾客类型"),
            "性别": st.column_config.TextColumn("性别"),
            "产品类型": st.column_config.TextColumn("产品类型")
        }
    )
    
    # 数据导出功能
    csv_data = filtered_data.drop(columns=['小时']).to_csv(index=False, encoding='utf-8-sig')
    st.download_button(
        label="📥 导出筛选后数据为CSV",
        data=csv_data,
        file_name=f'Excel筛选数据_{pd.Timestamp.now().strftime("%Y%m%d%H%M%S")}.csv',
        mime='text/csv'
    )
