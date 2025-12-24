import streamlit as st
from datetime import datetime

# 页面配置
st.set_page_config(page_title="个人简历生成器", page_icon="📄", layout="wide")

# 初始化session_state存储表单数据，避免刷新丢失（修正缩进）
if 'resume_data' not in st.session_state:
    st.session_state.resume_data = {
        "姓名": "",
        "职位": "",
        "电话": "",
        "邮箱": "",
        "出生日期": datetime(1990, 1, 1),
        "性别": "男",
        "学历": "本科",
        "语言能力": "",
        "技能": [],
        "工作经验": 0,
        "期望薪资": (1000, 2000),
        "个人简介": "这个人很神秘，没有留下任何介绍...",
        "最佳联系时间": "09:00",
        "个人照片": None
    }

# 页面标题
st.title("📄 个人简历生成器")

# 分左右两栏布局
col1, col2 = st.columns(2, gap="large")

# 左侧：个人信息表单
with col1:
    st.subheader("个人信息表单")
    st.divider()
    
    # 1. 姓名输入
    name = st.text_input("姓名", value=st.session_state.resume_data["姓名"])
    st.session_state.resume_data["姓名"] = name
    
    # 2. 职位输入
    job = st.text_input("职位", value=st.session_state.resume_data["职位"])
    st.session_state.resume_data["职位"] = job
    
    # 3. 电话输入
    phone = st.text_input("电话", value=st.session_state.resume_data["电话"])
    st.session_state.resume_data["电话"] = phone
    
    # 4. 邮箱输入
    email = st.text_input("邮箱", value=st.session_state.resume_data["邮箱"])
    st.session_state.resume_data["邮箱"] = email
    
    # 5. 出生日期选择
    birth_date = st.date_input("出生日期", value=st.session_state.resume_data["出生日期"])
    st.session_state.resume_data["出生日期"] = birth_date
    
    # 6. 性别单选
    gender = st.radio("性别", ["男", "女", "其他"], horizontal=True, index=["男", "女", "其他"].index(st.session_state.resume_data["性别"]))
    st.session_state.resume_data["性别"] = gender
    
    # 7. 学历下拉选择
    edu_options = ["高中", "专科", "本科", "硕士", "博士"]
    education = st.selectbox("学历", edu_options, index=edu_options.index(st.session_state.resume_data["学历"]))
    st.session_state.resume_data["学历"] = education
    
    # 8. 语言能力下拉选择
    lang_options = ["", "英语四级", "英语六级", "日语N1", "日语N2", "普通话二甲"]
    language = st.selectbox("语言能力", lang_options, index=lang_options.index(st.session_state.resume_data["语言能力"]))
    st.session_state.resume_data["语言能力"] = language
    
    # 9. 技能多选
    skill_options = ["Python", "Java", "SQL", "前端", "后端", "数据分析"]
    skills = st.multiselect("技能（可多选）", skill_options, default=st.session_state.resume_data["技能"])
    st.session_state.resume_data["技能"] = skills
    
    # 10. 工作经验（年）数字输入
    work_exp = st.number_input("工作经验（年）", min_value=0, max_value=50, value=st.session_state.resume_data["工作经验"])
    st.session_state.resume_data["工作经验"] = work_exp
    
    # 11. 期望薪资滑块
    salary = st.slider("期望薪资范围（元）", min_value=1000, max_value=50000, value=st.session_state.resume_data["期望薪资"], step=100)
    st.session_state.resume_data["期望薪资"] = salary
    
    # 12. 个人简介文本域
    intro = st.text_area("个人简介", placeholder="请简要介绍你的专业背景、职业目标和个人特点...", value=st.session_state.resume_data["个人简介"], height=100)
    st.session_state.resume_data["个人简介"] = intro
    
    # 13. 每日最佳联系时间
    time_options = ["09:00", "10:00", "14:00", "16:00", "19:00"]
    contact_time = st.selectbox("每日最佳联系时间段", time_options, index=time_options.index(st.session_state.resume_data["最佳联系时间"]))
    st.session_state.resume_data["最佳联系时间"] = contact_time
    
    # 14. 上传个人照片
    photo = st.file_uploader("上传个人照片", type=["png", "jpg", "jpeg"])
    if photo:
        st.session_state.resume_data["个人照片"] = photo

# 右侧：简历实时预览
with col2:
    st.subheader("简历实时预览")
    st.divider()
    
    # 基本信息展示
    st.write(f"**姓名：** {st.session_state.resume_data['姓名'] or '未填写'}")
    st.write(f"**职位：** {st.session_state.resume_data['职位'] or '未填写'}")
    st.write(f"**电话：** {st.session_state.resume_data['电话'] or '未填写'}")
    st.write(f"**邮箱：** {st.session_state.resume_data['邮箱'] or '未填写'}")
    st.write(f"**出生日期：** {st.session_state.resume_data['出生日期'].strftime('%Y/%m/%d')}")
    
    # 右侧侧边信息（性别、学历等）
    col2_1, col2_2 = st.columns(2)
    with col2_1:
        st.write(f"**性别：** {st.session_state.resume_data['性别']}")
        st.write(f"**学历：** {st.session_state.resume_data['学历']}")
        st.write(f"**工作经验：** {st.session_state.resume_data['工作经验']}年")
        st.write(f"**期望薪资：** {st.session_state.resume_data['期望薪资'][0]}-{st.session_state.resume_data['期望薪资'][1]}元")
        st.write(f"**最佳联系时间：** {st.session_state.resume_data['最佳联系时间']}")
        st.write(f"**语言能力：** {st.session_state.resume_data['语言能力'] or '未填写'}")
    
    with col2_2:
        # 展示个人照片
        if st.session_state.resume_data["个人照片"]:
            st.image(st.session_state.resume_data["个人照片"], width=150, caption="个人照片")
    
    # 技能展示
    st.divider()
    st.write("**技能：**")
    if st.session_state.resume_data["技能"]:
        st.write(", ".join(st.session_state.resume_data["技能"]))
    else:
        st.write("未填写")
    
    # 个人简介展示
    st.divider()
    st.subheader("个人简介")
    st.write(st.session_state.resume_data["个人简介"])
    
    # 页脚标语
    st.divider()
    st.caption("*代码改变世界，你改变代码*")
