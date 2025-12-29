import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor

# 页面配置
st.set_page_config(
    page_title="医疗费用预测系统",
    page_icon="🏥",
    layout="centered"
)

# 数据加载与预处理
@st.cache_data
def load_data():
    file_path = "insurance-chinese.csv"
    # 读取文件
    try:
        df = pd.read_csv(file_path, encoding='gbk')
    except:
        df = pd.read_csv(file_path, encoding='utf-8')
    # 修正列名
    df = df.iloc[:, :7].copy()
    df.columns = ["年龄", "性别", "BMI", "子女数量", "是否吸烟", "区域", "医疗费用"]
    # 数据清洗
    df["医疗费用"] = pd.to_numeric(df["医疗费用"], errors='coerce').fillna(df["医疗费用"].mean())
    df = df[df["医疗费用"] > 0].dropna(subset=["性别", "是否吸烟", "区域"])
    return df

# 模型训练
@st.cache_resource
def train_model(df):
    X = df.drop("医疗费用", axis=1)
    y = df["医疗费用"]
    X_train, _, y_train, _ = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 预处理+模型
    cat_feat = ["性别", "是否吸烟", "区域"]
    num_feat = ["年龄", "BMI", "子女数量"]
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), num_feat),
            ("cat", OneHotEncoder(drop="first", sparse_output=False), cat_feat)
        ])
    model = Pipeline(steps=[
        ("pre", preprocessor),
        ("reg", RandomForestRegressor(n_estimators=50, random_state=42))
    ])
    model.fit(X_train, y_train)
    return model

# 主页面
def main():
    nav = st.sidebar.radio("导航", ["简介", "预测医疗费用"])
    df = load_data()
    
    if nav == "简介":
        st.title("医疗费用预测系统")
        st.write("通过个人信息预测医疗费用，为保险定价提供参考")
    
    elif nav == "预测医疗费用":
        st.title("输入个人信息")
        # 输入表单
        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input("年龄", 0, 100, 30)
            gender = st.radio("性别", ["男性", "女性"])
            bmi = st.number_input("BMI", 18.5, 35.0, 22.0)
        with col2:
            children = st.number_input("子女数量", 0, 5, 0)
            smoking = st.radio("是否吸烟", ["是", "否"])
            region = st.selectbox("区域", ["东南部", "西南部", "东北部", "西北部"])
        
        # 预测
        if st.button("预测医疗费用", type="primary"):
            model = train_model(df)
            input_data = pd.DataFrame({
                "年龄": [age], "性别": [gender], "BMI": [bmi],
                "子女数量": [children], "是否吸烟": [smoking], "区域": [region]
            })
            pred = model.predict(input_data)[0]
            st.success(f"预计年度医疗费用：¥{pred:,.2f}")

if __name__ == "__main__":
    main()
