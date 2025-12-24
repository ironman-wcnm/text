import streamlit as st

# 页面配置
st.set_page_config(page_title="简易音乐播放器", page_icon="🎵")

# 音乐数据（包含封面、歌名、歌手、时长、音频链接）
music_list = [
    {
        "cover": "https://p1.music.126.net/M8P1hkIMBeN2JnoCqVoClQ==/109951163333239429.jpg?param=200y200", # 封面URL
        "title": "Bohemian Rhapsody",
        "singer": "Queen",
        "duration": "5:55",
        "audio_url": "https://music.163.com/song/media/outer/url?id=5257138.mp3"
    },
    {
        "cover": "https://p1.music.126.net/2rux5LnJey75tm9Md-9D-Q==/2890616070443534.jpg?param=200y200", # 可替换为其他歌曲封面
        "title": "两 难",
        "singer": "歌手名",
        "duration": "2:50",
        "audio_url": "https://music.163.com/song/media/outer/url?id=2163210456.mp3"
    },
    {
        "cover": "https://p1.music.126.net/c-u3kOlkVTUf4JdeDHDdEw==/109951163291871252.jpg?param=200y200",
        "title": "如果呢",
        "singer": "歌手名",
        "duration": "3:45",
        "audio_url": "https://music.163.com/song/media/outer/url?id=1842728629.mp3"
    }
]

# 初始化当前播放索引
if "current_ind" not in st.session_state:
    st.session_state.current_ind = 0

# 获取当前播放的音乐
current_music = music_list[st.session_state.current_ind]

# 页面标题
st.title("🎵 简易音乐播放器")
st.caption("使用Streamlit制作的简单音乐播放器，支持切换和基本播放控制")

# 布局：左封面 + 右歌曲信息
col1, col2 = st.columns([1, 2])

with col1:
    # 显示音乐封面
    st.image(current_music["cover"], caption="专辑封面",)

with col2:
    # 竖排显示歌曲信息
    st.markdown(f"### {current_music['title']}")
    st.markdown(f"**歌手：** {current_music['singer']}")
    st.markdown(f"**时长：** {current_music['duration']}")

# 上一首/下一首按钮
btn_col1, btn_col2 = st.columns(2)

def prev_song():
    # 上一首（循环）
    st.session_state.current_ind = (st.session_state.current_ind - 1) % len(music_list)

def next_song():
    # 下一首（循环）
    st.session_state.current_ind = (st.session_state.current_ind + 1) % len(music_list)

with btn_col1:
    st.button("◀ 上一首", use_container_width=True, on_click=prev_song)

with btn_col2:
    st.button("下一首 ▶", use_container_width=True, on_click=next_song)

# 播放进度条（用滑块模拟，实际播放需结合音频时长，这里默认总时长355秒对应Queen歌曲的5:55）




# 音频播放组件
st.audio(current_music["audio_url"], format="audio/mp3")
