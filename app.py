import streamlit as st
import pandas as pd
import os
import time
from datetime import datetime

# --- 配置 ---
DB_FILE = "farm_master_data.csv"

def load_data():
    if not os.path.exists(DB_FILE):
        return pd.DataFrame(columns=["时间", "成员", "作物", "数量", "收益", "状态"])
    return pd.read_csv(DB_FILE)

def add_entry(user, crop, num, gold):
    new_data = {
        "时间": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
        "成员": [user],
        "作物": [crop],
        "数量": [num],
        "收益": [gold],
        "状态": ["已入库"]
    }
    new_df = pd.DataFrame(new_data)
    # 采用追加模式，encoding='utf-8-sig' 确保 Excel 直接打开不乱码
    new_df.to_csv(DB_FILE, mode='a', header=not os.path.exists(DB_FILE), index=False, encoding='utf-8-sig')

# --- 界面 ---
st.set_page_config(page_title="农场数据中转站", page_icon="🌽")

st.title("🚜 农场内部数据中心 (本地版)")

# 侧边栏：录入
with st.sidebar:
    st.header("📥 快速录入")
    name = st.selectbox("成员姓名", ["朋友A", "朋友B", "我"])
    crop = st.text_input("作物/任务名称", "黄金小麦")
    num = st.number_input("数量", value=1)
    gold = st.number_input("预估收益", value=0)
    
    if st.button("提交到服务器"):
        with st.spinner('正在同步数据...'):
            add_entry(name, crop, num, gold)
            time.sleep(0.5) # 给硬盘一点反应时间
            st.success("数据存入本地硬盘！")

# 主界面：显示
df = load_data()

st.subheader("📊 全局统计")
if not df.empty:
    c1, c2, c3 = st.columns(3)
    c1.metric("累计任务数", len(df))
    c2.metric("全员总收益", f"{df['收益'].sum():,}")
    c3.metric("最新贡献者", df.iloc[-1]['成员'])

    st.divider()
    st.dataframe(df.sort_index(ascending=False), use_container_width=True)
else:
    st.info("目前还没有数据，等待大家录入...")