#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import streamlit as st

st.set_page_config(page_title="ファミマ店舗分析", layout="wide")

df = pd.read_csv("famimart_cleaned.csv")

df["簡易エリア"] = df["エリア"].apply(lambda x: x.split()[-2] if isinstance(x, str) and len(x.split()) >= 2 else x)

area_list = sorted(df["簡易エリア"].dropna().unique())
selected_area = st.sidebar.selectbox("エリアを選択してください", ["すべて"] + area_list)

if selected_area == "すべて":
    filtered_df = df.copy()
else:
    filtered_df = df[df["簡易エリア"] == selected_area]

st.write(f"### 選択されたエリア: {selected_area}")
st.write(f"店舗数: {len(filtered_df)} 件")

filtered_df = filtered_df.rename(columns={"cz_sp_table_URL": "連絡先"})

st.dataframe(filtered_df[["タイトル", "エリア", "連絡先"]])

area_counts = filtered_df["簡易エリア"].value_counts().sort_values(ascending=False)

if area_counts.empty:
    st.warning("該当するデータがありません。")
else:
    fig, ax = plt.subplots(figsize=(14,6))
    fontprop = fm.FontProperties(fname="C:/Windows/Fonts/meiryo.ttc")
    ax.bar(area_counts.index, area_counts.values, color="skyblue")
    ax.set_xlabel("エリア", fontproperties=fontprop)
    ax.set_ylabel("店舗数", fontproperties=fontprop)
    ax.set_title(f"{selected_area} の店舗数", fontproperties=fontprop)
    plt.xticks(rotation=60, ha="right", fontproperties=fontprop)
    st.pyplot(fig)


# In[ ]:




