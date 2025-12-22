import streamlit as st

st.set_page_config(page_title="相册网站", page_icon="🌠")

image_ua = [
    {
        'url': 'data:image/webp;base64,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',
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

# 将当前的索引存储到内存中，如果内存中没有ind，我才要0，如果有就不设置ind
if 'ind' not in st.session_state:
    st.session_state['ind'] = 0

st.image(image_ua[st.session_state['ind']]['url'], caption=image_ua[st.session_state['ind']]['text'])

# 课本73 分列容器
c1, c2 = st.columns(2)

def nextImg():
    # 下一张：索引+1，超出长度时回到0（循环）
    st.session_state['ind'] = (st.session_state['ind'] + 1) % len(image_ua)

def prevImg():
    # 上一张：索引-1，小于0时回到最后一张（循环）
    st.session_state['ind'] = (st.session_state['ind'] - 1) % len(image_ua)

with c1:
    # 课本122页 按钮 - 绑定上一张函数
    st.button('上一张', use_container_width=True, on_click=prevImg)

with c2:
    st.button('下一张', use_container_width=True, on_click=nextImg)