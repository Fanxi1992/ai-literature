
from streamlit_extras.let_it_rain import rain
from streamlit_extras.mention import mention
import streamlit as st
import dotenv
dotenv.load_dotenv()



# 设置页面配置为全屏布局
st.set_page_config(page_title='Academic Toolkits', layout="wide")

st.markdown('''
    <span style="color: red; font-size: 20px;">Streamlit</span>
    <span style="color: orange; font-size: 20px;">can</span>
    <span style="color: green; font-size: 20px;">write</span>
    <span style="color: blue; font-size: 20px;">text</span>
    <span style="color: violet; font-size: 20px;">in</span>
    <span style="color: gray; font-size: 20px;">pretty</span>
    <span style="color: rainbow; font-size: 20px; background-image: linear-gradient(to right, red, orange, yellow, green, blue, indigo, violet);">colors</span>.
    ''', unsafe_allow_html=True)


st.markdown("---")
st.markdown("---")

st.markdown("*Streamlit* is **really** ***cool***.")
st.markdown('''
    :red[Streamlit] :orange[can] :green[write] :blue[text] :violet[in]
    :gray[pretty] :rainbow[colors].''')
st.markdown("Here's a bouquet &mdash;\
            :tulip::cherry_blossom::rose::hibiscus::sunflower::blossom:")

multi = '''If you end a line with two spaces,
a soft return is used for the next line.

Two (or more) newline characters in a row will result in a hard return.
'''
st.markdown(multi)


rain(
    emoji="🌧️",
    font_size=30,
    falling_speed=8,
    animation_length="50",
)



with st.sidebar:
    with st.expander("🌈 More information"):
        st.write("更多功能正在开发中...")

st.markdown("---")
st.markdown("---")
