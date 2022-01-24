import streamlit as st
import st_filteretf
st.set_page_config(layout='wide')
PAGES = {
    "查找被动基金(指数基金)": st_filteretf,
    "查找主动基金": "TODO",
    "市场估值和温度": "TODO",
    "市场主流买什么(ETF净流入)": "TODO",
    "市场潜力(还能涨多少)": "TODO",
    "周期数据(发财密码)": "TODO",
    "牛市熊市买什么": "TODO",
    "品种回撤数据": "TODO", #最大回撤和最近新高回撤
}

st.sidebar.title("财富自由之路")

selection = st.sidebar.radio("老韭菜的工具盒子", list(PAGES.keys()))
page = PAGES[selection]
try:
    page.app()
except AttributeError:
    page.app()


# st.sidebar.radio("看教程塑三观",
#     [
#         "书单",
#         "理财基础",
#         "基础知识",
#         "如何选择基金",
#         "资产配置",
#         "决定买什么",
#         "如何买",
#         "坚定不移的持有",
#         "如何卖",
#         "如何获取超额收益",
#         "要不要做波段",
#         "打新",
#         "国债逆回购",
#         "可转债",
#         "Bitcoin",
#     ]
# )
