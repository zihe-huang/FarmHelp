import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="农场数据云终端", layout="centered")

# 1. 建立连接 (配置信息后续在云端 Secrets 设置)
conn = st.connection("gsheets", type=GSheetsConnection)

# 2. 读取数据
# ttl=0 确保每次刷新页面都从 Google Sheets 获取最新数据，不使用缓存
df = conn.read(ttl=0)

st.title("🚜 农场数据中心")

# 3. 侧边栏录入
with st.sidebar.form("input_form"):
    st.header("新增记录")
    user = st.selectbox("成员", ["朋友A", "朋友B", "我"])
    crop = st.text_input("作物", value="小麦")
    income = st.number_input("预计收益", value=0)
    submitted = st.form_submit_button("提交同步")

if submitted:
    new_row = {
        "时间": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "成员": user,
        "作物": crop,
        "收益": income
    }
    # 将新数据追加到现有的数据框并更新回 Sheets
    updated_df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    conn.update(data=updated_df)
    st.success("数据已同步至 Google Sheets！")
    st.rerun()

# 4. 数据展示
if not df.empty:
    st.metric("团队总收益", f"💰 {df['收益'].sum():,}")
    st.dataframe(df.sort_index(ascending=False), use_container_width=True)
else:
    st.info("暂无数据，请在侧边栏录入。")
