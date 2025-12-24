import streamlit as st
# 定义剧集数据（包含集数链接、介绍、演职人员）
series_data = {
    "熊出没": {
        "episodes": {
            "第1集": "https://upos-sz-mirrorcosov.bilivideo.com/upgcxcode/18/11/500001641981118/500001641981118-1-192.mp4?e=ig8euxZM2rNcNbRg7bdVhwdlhWNjhwdVhoNvNC8BqJIzNbfq9rVEuxTEnE8L5F6VnEsSTx0vkX8fqJeYTj_lta53NCM=&deadline=1766565450&platform=html5&nbs=1&gen=playurlv3&os=cosovbv&og=cos&oi=771356656&mid=0&trid=6956d3237c3f4795b7b425dc8615bd4h&uipk=5&upsig=5673e060b559d4a7990f1cc20b081aff&uparams=e,deadline,platform,nbs,gen,os,og,oi,mid,trid,uipk&bvc=vod&nettype=0&bw=1008573&f=h_0_0&agrr=1&buvid=&build=0&dl=0&orderid=0,1",
            "第2集": "https://upos-sz-mirrorcosov.bilivideo.com/upgcxcode/82/44/500001641984482/500001641984482-1-192.mp4?e=ig8euxZM2rNcNbR1hwdVhwdlhWRVhwdVhoNvNC8BqJIzNbfq9rVEuxTEnE8L5F6VnEsSTx0vkX8fqJeYTj_lta53NCM=&nbs=1&deadline=1766566207&os=cosovbv&og=ali&platform=html5&uipk=5&oi=771356656&gen=playurlv3&trid=0b05568cf55348ca9abeb9561b2fa2eh&mid=0&upsig=39ba2903fecbb82937775e4b52698737&uparams=e,nbs,deadline,os,og,platform,uipk,oi,gen,trid,mid&bvc=vod&nettype=0&bw=884509&f=h_0_0&agrr=1&buvid=&build=0&dl=0&orderid=0,1"
        },
            },
    "动物世界": {
        "episodes": {
            "第1集": "https://www.w3schools.com/html/movie.mp4"
        },
       
    }
}
# 初始化Session State（记录当前剧集和集数）
if "current_series" not in st.session_state:
    st.session_state.current_series = list(series_data.keys())[0]  # 默认第一个剧集
if "current_episode" not in st.session_state:
    # 默认当前剧集的第一个集数
    st.session_state.current_episode = list(series_data[st.session_state.current_series]["episodes"].keys())[0]
# 上一部/下一部 剧集切换按钮（循环切换+始终显示）
series_list = list(series_data.keys())
current_series_idx = series_list.index(st.session_state.current_series)
total_series = len(series_list)
col_prev, col_next = st.columns(2)
with col_prev:
    # 循环计算上一部索引：当前索引-1 取模总数量（负数取模会自动转为最后一个）
    prev_idx = (current_series_idx - 1) % total_series
    if st.button("上一部剧集", use_container_width=True):
        st.session_state.current_series = series_list[prev_idx]
        # 切换剧集后默认选中该剧集的第一个集数
        st.session_state.current_episode = list(series_data[st.session_state.current_series]["episodes"].keys())[0]
with col_next:
    # 循环计算下一部索引：当前索引+1 取模总数量
    next_idx = (current_series_idx + 1) % total_series
    if st.button("下一部剧集", use_container_width=True):
        st.session_state.current_series = series_list[next_idx]
        # 切换剧集后默认选中该剧集的第一个集数
        st.session_state.current_episode = list(series_data[st.session_state.current_series]["episodes"].keys())[0]
# 显示当前剧集标题
st.title(f"{st.session_state.current_series}-{st.session_state.current_episode}")
# 显示视频
current_video_url = series_data[st.session_state.current_series]["episodes"][st.session_state.current_episode]
st.video(current_video_url, format="video/mp4")


# 集数切换按钮（模仿图片样式，每行3个）
st.subheader("🔢 选择集数")
episodes = series_data[st.session_state.current_series]["episodes"]
cols = st.columns(min(3, len(episodes)))
for idx, ep in enumerate(episodes.keys()):
    with cols[idx % 3]:
        if st.button(ep, use_container_width=True):
            st.session_state.current_episode = ep
