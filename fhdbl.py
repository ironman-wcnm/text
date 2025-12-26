import streamlit as st
from datetime import datetime
import pandas as pd

# 全局页面配置（仅需调用一次，放在最上方）
st.set_page_config(page_title="缝合多功能页面", page_icon="📚", layout="wide")

# ---------------------- 核心CSS样式（顶部导航栏+悬浮变色+移除圆圈） ----------------------
st.markdown("""
    <style>
    /* 1. 完全移除radio组件的原生圆圈（选中/未选中状态均隐藏） */
    .stRadio [role="radiogroup"] label > div:first-child {
        display: none !important;
    }

    /* 2. 顶部导航栏容器样式：横向排列+美化布局 */
    .stRadio [role="radiogroup"] {
        display: flex;
        flex-direction: row; /* 横向排列（核心：实现顶部导航） */
        gap: 8px; /* 导航选项之间的间距 */
        justify-content: center; /* 整体居中对齐 */
        padding: 10px 0 20px 0; /* 上下内边距，拉开与标题的距离 */
    }

    /* 3. 单个导航选项基础样式：美化按钮外观 */
    .stRadio [role="radiogroup"] label {
        padding: 10px 20px;
        border-radius: 6px;
        cursor: pointer;
        transition: all 0.2s ease-in-out; /* 悬浮过渡效果 */
        margin: 0; /* 去除默认外边距 */
        color: #333333; /* 默认文字颜色 */
        font-size: 14px;
        background-color: #f5f5f5; /* 默认背景色 */
    }

    /* 4. 鼠标悬浮变色效果：背景+文字同步变色 */
    .stRadio [role="radiogroup"] label:hover {
        background-color: #e6f7ff; /* 悬浮背景色（浅蓝色） */
        color: #1890ff; /* 悬浮文字色（深蓝色） */
    }

    /* 5. 选中项样式：突出显示当前页面 */
    .stRadio [role="radiogroup"] label[data-selected="true"] {
        background-color: #1890ff; /* 选中背景色 */
        color: #ffffff; /* 选中文字色 */
    }

    /* 6. 数字档案页面黑色主题样式（保留原有功能） */
    .dark-theme .stApp {
        background-color: #000000;
    }
    h1, h2, h3, h4, h5, h6 {
        text-align: center;
    }
    .dark-theme h1, .dark-theme h2, .dark-theme h3, .dark-theme h4, .dark-theme h5, .dark-theme h6 {
        color: #ffffff;
    }
    .dark-theme .stText, .dark-theme .stCaption, .dark-theme .stMarkdown {
        color: #ffffff;
    }
    .dark-theme .stMetric {
        background-color: #1a1a1a;
        padding: 10px;
        border-radius: 6px;
        text-align: center;
    }
    .dark-theme .stMetric label, .dark-theme .stMetric value {
        color: #ffffff;
    }
    .dark-theme .stProgress > div {
        background-color: #333333;
        height: 8px;
        border-radius: 4px;
    }
    .dark-theme .stDataFrame {
        color: #ffffff;
        background-color: #1a1a1a;
    }
    .dark-theme .stDataFrame th {
        background-color: #222222;
        color: #ffffff;
    }
    .dark-theme .stDataFrame td {
        color: #ffffff;
    }
    .dark-theme .stCode {
        background-color: #1e1e1e !important;
        color: #dcdcdc !important;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------- 顶部导航栏（替代原有侧边栏） ----------------------
# 顶部标题
st.title("📑 缝合多功能页面")
# 顶部radio导航（横向排列，实现顶部导航栏）
page = st.radio(
    "导航标签",
    ["主页", "个人简历生成器", "动物图鉴", "南宁美食数据", "数字档案"],
    index=0,  # 默认选中主页
    help="点击切换不同功能页面",
    label_visibility="collapsed"  # 隐藏radio的默认标签
)

# 顶部分隔线
st.divider()

# ---------------------- 1. 主页 ----------------------
if page == "主页":
    st.title("🏫 广西职业师范学院 - 主页介绍")
    st.divider()
    
    # 主页图片（使用网络示例图，可替换为实际图片）
    home_image_url = "https://gx211.cn/UploadImage/FckUpImg/2021031764.jpg"
    # 用三列布局实现图片居中：左右列占位，中间列放图片
    col_left, col_mid, col_right = st.columns([1, 2, 1])
    with col_mid:
        st.image(home_image_url, caption="广西职业师范学院校园风光")
    # 主页文字内容
    st.subheader("学校简介")
    st.markdown("""
    广西职业师范学院（原广西经济管理干部学院）坐落于广西南宁市风景秀丽的邕江之滨、相思湖畔，是自治区人民政府直属、自治区教育厅主管的公办全日制普通本科学校，致力于为我区经济社会发展培养所需的高素质应用型、技术技能型人才和职业教育师资。

    ### 历史沿革
    学校前身可追溯至1951年创办的广西省行政干部训练班。其后，为适应不同历史时期广西经济社会发展，学校历经了广西人民革命大学、广西行政干部学校、广西经济干部学校、广西经济管理干部学院等历史变迁，并于2019年经教育部批准改建为广西职业师范学院。

    ### 师资力量
    学校拥有一支结构优良、学术水平较高、教学经验丰富的专职教师队伍，其中，取得硕士、博士学位教师427人，拥有自治区级教学名师、国家级、自治区级成果奖的教师共获国家、自治区级各类奖项共120多项，其中广西高等学校教学成果奖特等奖1个。

    ### 专业设置
    学校现设11个二级学院（部），普通本科专业29个，涵盖经济学、管理学、工学、理学、教育学、文学、法学、艺术学等八个学科，紧密对接广西产业发展需求，培养复合型应用人才。
    """)
    st.divider()
   

# ---------------------- 2. 个人简历生成器 ----------------------
elif page == "个人简历生成器":
    # 初始化session_state存储表单数据
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
    st.divider()

    # 分左右两栏布局
    col1, col2 = st.columns(2, gap="large")

    # 左侧：个人信息表单
    with col1:
        st.subheader("📝 个人信息填写")
        st.divider()
        
        # 1. 姓名输入
        name = st.text_input("姓名", value=st.session_state.resume_data["姓名"], placeholder="请输入您的姓名")
        st.session_state.resume_data["姓名"] = name
        
        # 2. 职位输入
        job = st.text_input("应聘职位", value=st.session_state.resume_data["职位"], placeholder="请输入应聘职位")
        st.session_state.resume_data["职位"] = job
        
        # 3. 电话输入
        phone = st.text_input("联系电话", value=st.session_state.resume_data["电话"], placeholder="请输入手机号码")
        st.session_state.resume_data["电话"] = phone
        
        # 4. 邮箱输入
        email = st.text_input("电子邮箱", value=st.session_state.resume_data["邮箱"], placeholder="请输入常用邮箱")
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
        st.subheader("📋 简历实时预览")
        st.divider()
        
        # 基本信息展示
        st.write(f"**姓名：** {st.session_state.resume_data['姓名'] or '未填写'}")
        st.write(f"**应聘职位：** {st.session_state.resume_data['职位'] or '未填写'}")
        st.write(f"**联系电话：** {st.session_state.resume_data['电话'] or '未填写'}")
        st.write(f"**电子邮箱：** {st.session_state.resume_data['邮箱'] or '未填写'}")
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
        st.write("**掌握技能：**")
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

# ---------------------- 3. 动物图鉴（已更新老鹰图片链接） ----------------------
elif page == "动物图鉴":
    st.title("🌠 动物图鉴相册")
    st.divider()

    # 初始化图片索引
    if 'ind' not in st.session_state:
        st.session_state['ind'] = 0

    # 动物图片数据（老鹰链接已替换为指定地址）
    image_ua = [
        {
            'url': 'https://img95.699pic.com/photo/60030/1645.jpg_wh860.jpg',  # 指定老鹰图片链接
            'text': '老鹰'
        },
        {
            'url': 'https://tse1-mm.cn.bing.net/th/id/OIP-C.OgWV-ECz_rxqh1evJGciowHaE7?w=267&h=180&c=7&r=0&o=7&cb=ucfimg2&pid=1.7&rm=3&ucfimg=1',
            'text': '斑马'
        },
        {
            'url': 'https://tse4-mm.cn.bing.net/th/id/OIP-C.PJ9Wb-5cl0rYUlE2eaOw0AHaE8?w=241&h=180&c=7&r=0&o=7&cb=ucfimg2&pid=1.7&rm=3&ucfimg=1',
            'text': '老虎'
        },
    ]

    # 显示当前图片
    st.image(
        image_ua[st.session_state['ind']]['url'],
        caption=image_ua[st.session_state['ind']]['text'],
    )

    # 图片切换函数
    def nextImg():
        st.session_state['ind'] = (st.session_state['ind'] + 1) % len(image_ua)

    def prevImg():
        st.session_state['ind'] = (st.session_state['ind'] - 1) % len(image_ua)

    # 切换按钮布局
    c1, c2 = st.columns(2, gap="medium")
    with c1:
        st.button('⬅️ 上一张', use_container_width=True, on_click=prevImg)
    with c2:
        st.button('下一张 ➡️', use_container_width=True, on_click=nextImg)

    st.divider()
    st.caption(f"当前第 {st.session_state['ind']+1}/{len(image_ua)} 张图片")

# ---------------------- 4. 南宁美食数据 ----------------------
elif page == "南宁美食数据":
    st.title("🍜 南宁美食数据仪表盘")
    st.divider()

    # ---------------------- 数据定义 ----------------------
    # 南宁美食餐厅基础数据
    restaurants = pd.DataFrame({
        "餐厅": ["星艺会尝不忘", "高峰柠檬鸭", "复记老友粉", "好友缘", "西冷牛排店", "中山路老牌粉店"],
        "类型": ["中餐", "中餐", "快餐", "自助餐", "西餐", "快餐"],
        "评分": [4.2, 4.5, 4.0, 4.7, 4.3, 4.1],
        "人均消费(元)": [15, 20, 25, 35, 50, 18],
        "latitude": [22.853838, 22.965046, 22.812200, 22.809105, 22.839699, 22.845210],
        "longitude": [108.222177, 108.353921, 108.266629, 108.378664, 108.245804, 108.230102]
    })
    restaurants.index.name = "序号"

    # 12个月餐厅价格走势
    months = [f"{i:02d}月" for i in range(1, 13)]
    price_trend = pd.DataFrame({
        "月份": months,
        "星艺会尝不忘": [15, 16, 15, 17, 16, 15, 16, 17, 15, 16, 17, 15],
        "高峰柠檬鸭": [20, 21, 20, 22, 21, 20, 21, 22, 20, 21, 22, 20],
        "复记老友粉": [25, 26, 25, 27, 26, 25, 26, 27, 25, 26, 27, 25],
        "好友缘": [35, 36, 35, 37, 36, 35, 36, 37, 35, 36, 37, 35],
        "西冷牛排店": [50, 51, 50, 52, 51, 50, 51, 52, 50, 51, 52, 50]
    })

    peak_hours = pd.DataFrame({
        "时段": ["10:00", "11:00", "12:00", "13:00", "17:00", "18:00", "19:00", "20:00"],
        "客流量": [50, 120, 180, 80, 100, 200, 150, 90]
    })

    # ---------------------- 界面布局 ----------------------
    # 1. 美食店铺分布地图
    st.subheader("📍 南宁美食店铺分布")
    st.map(restaurants[["latitude", "longitude"]])

    # 2. 餐厅评分条形图
    st.subheader("⭐ 餐厅评分排行")
    st.bar_chart(restaurants, x="餐厅", y="评分", color="#FF6B6B")

    # 3. 不同类型餐厅人均价格
    st.subheader("💰 不同类型餐厅人均价格")
    type_avg_price = restaurants.groupby("类型")["人均消费(元)"].mean().reset_index()
    st.line_chart(type_avg_price, x="类型", y="人均消费(元)", color="#4ECDC4")

    # 4. 12个月餐厅价格走势
    st.subheader("📈 12个月餐厅价格走势")
    st.line_chart(
        price_trend,
        x="月份",
        y=["星艺会尝不忘", "高峰柠檬鸭", "复记老友粉", "好友缘", "西冷牛排店"],
        color=["#FF6B6B", "#FFA07A", "#FFD700", "#98FB98", "#87CEFA"]
    )

# ---------------------- 5. 数字档案 ----------------------
elif page == "数字档案":
    # 激活黑色主题
    st.markdown('<div class="dark-theme">', unsafe_allow_html=True)

    # 页面内容
    st.title("🎓 学生数字档案")
    st.divider()

    # 基础信息
    st.header("📝 基础信息")
    st.markdown("""
    - 学生ID：12565644 
    - 注册时间：2025-10-01 01:30:15 | **精神状态**：<span style="color:green">正常</span>  
    - 当前教室：实现楼101 | **安全等级**：<span style="color:green">高</span>  
    """, unsafe_allow_html=True)

    # 技能矩阵
    st.header("💻 技能矩阵")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric(label="C语言", value="95%", delta="+2%", delta_color="normal")
    with c2:
        st.metric(label="Python", value="87%", delta="-1%", delta_color="inverse")
    with c3:
        st.metric(label="Java", value="68%", delta="-10%", delta_color="inverse")

    # 综合进度
    st.header("📊 Streamlit课程进度")
    st.progress(33)
    st.caption("当前综合完成度：33%")

    # 任务日志（表格）
    st.header("📋 任务日志")
    task_data = {
        "日期": ["2023-10-01", "2023-10-05", "2023-10-12"],
        "任务": ["学生数字档案", "课程管理系统", "数据可视化"],
        "状态": ["<span style='color:green'>● 进行中</span>", "<span style='color:yellow'>● 待审核</span>", "<span style='color:red'>● 未完成</span>"],
        "难度": ["★★☆☆☆", "★★★☆☆", "★★★★☆"]
    }
    task_df = pd.DataFrame(task_data)
    st.markdown(task_df.to_html(escape=False, index=False), unsafe_allow_html=True)

    # 最新代码成果
    st.header("💾 最新代码成果")
    code_content = '''df = df[df['label'] == '正常']
with open('data.txt', 'w') as f:
    if detect_vulnerability(f.read()):
        f.write("ACCESS DENIED")
        return
save_to_db(code)'''
    st.code(code_content, language="python")

    # 系统消息
    st.markdown("""
    ---
    <span style="color:green">【SYSTEM MESSAGE】下一个任务已解锁。</span>  
    <span style="color:green">【系统管理】请管理系统。</span>  
    <span style="color:green">【CONTENT】2025-10-01 10:00:00</span>  
    <span style="color:green">系统状态：在线 | 连接状态：已加密</span>
    """, unsafe_allow_html=True)

    # 关闭黑色主题容器
    st.markdown('</div>', unsafe_allow_html=True)
