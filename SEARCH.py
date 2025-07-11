#!/usr/bin/env python
# coding: utf-8

# In[2]:


import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv("famimart_cleaned.csv")

df["簡易エリア"] = df["エリア"].str.extract(r"(石川県金沢市.*?)(?:[0-9０-９\-ー丁目\s].*)?$")[0]
df["簡易エリア"] = df["簡易エリア"].fillna(df["エリア"])

area_list = sorted(df["簡易エリア"].dropna().unique())

selected_area = st.selectbox("エリアを選択してください", ["すべて"] + area_list)

if selected_area == "すべて":
    filtered_df = df.copy()
else:
    filtered_df = df[df["簡易エリア"] == selected_area]

st.write(f"選択されたエリア: {selected_area}")
st.write(f"店舗数: {len(filtered_df)} 件")

st.dataframe(
    filtered_df[["タイトル", "エリア", "cz_sp_table_URL"]]
    .rename(columns={"cz_sp_table_URL": "連絡先"})
    .set_index(pd.Series(range(1, len(filtered_df) + 1)))
)

area_counts = filtered_df["簡易エリア"].value_counts().sort_values(ascending=False)

if not area_counts.empty:
    fig = px.bar(
        x=area_counts.index,
        y=area_counts.values,
        labels={"x": "エリア", "y": "店舗数"},
        title=f"{selected_area} の店舗数",
    )
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig)
else:
    st.warning("該当するデータがありません。")


# In[ ]:




