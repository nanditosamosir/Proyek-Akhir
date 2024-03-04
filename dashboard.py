import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np
from babel.numbers import format_currency
sns.set(style='dark')

st.set_option('deprecation.showPyplotGlobalUse', False)

# Import data
day_df = pd.read_csv("bike-sharing-dataset/day.csv")
hour_df = pd.read_csv("bike-sharing-dataset/hour.csv")

# Data Cleaning
day_df["dteday"] = pd.to_datetime(day_df["dteday"])
hour_df["dteday"] = pd.to_datetime(hour_df["dteday"])

# Sidebar
st.sidebar.title("Proyek Analisis Data: Bike Sharing Dataset")
st.sidebar.subheader("Nandito Yuda Samosir")

st.header("Bike Sharing Dashboard")

st.subheader("Monthly Users")

# 1
colors = ["#72BCD4", "#CC3433"]
for year in [0, 1]:
    filtered_df = day_df[day_df['yr'] == year]
    monthly_count_df = filtered_df.resample(rule='M', on='dteday').agg({
        "cnt": "sum"
    })
    monthly_count_df.index = monthly_count_df.index.strftime('%B')
    monthly_count_df = monthly_count_df.reset_index()
    monthly_count_df.rename(columns={
        "cnt": "revenue"
    }, inplace=True)
    
    st.caption(f"Total Peminjaman Perbulan ({'2011' if year == 0 else '2012'})")
    st.line_chart(monthly_count_df.set_index("dteday")["revenue"])
    
st.subheader("Season and Weather")

# 2
colors2 = ["#f6b8c4", "#f6ad7d", "#5ba5c8", "#a6cfe5"]
# Diagram Jumlah Penyewa Berdasarkan Musim
season_df = day_df.groupby(by=["season"]).cnt.sum().reset_index()
season_df.rename(columns={
    "cnt": "sum"
}, inplace=True)

season_mapping = {1: 'Springer', 2: 'Summer', 3: 'Fall', 4: 'Winter'}

season_chart = sns.barplot(
    y="sum",
    x="season",
    data=season_df.sort_values(by="sum", ascending=False),
    palette=colors2,
    order=season_df['season']
)

season_chart.set_title("Jumlah Penyewa Sepeda Berdasarkan Musim")
season_chart.set_ylabel("Jumlah Penyewa (Ratus Ribu)")
season_chart.set_xlabel("Musim")
st.pyplot()

# Diagram Jumlah Penyewa Berdasrkan Cuaca
weather_df = day_df.groupby(by=["weathersit"]).cnt.sum().reset_index()
weather_df.rename(columns={
    "cnt": "sum"
}, inplace=True)

weather_mapping = {1: 'Clear', 2: 'Cloudy', 3: 'Light Rain/Snow', 4: 'Heavy Rain'}

weather_chart = sns.barplot(
    y="sum",
    x="weathersit",
    data=weather_df.sort_values(by="sum", ascending=False),
    palette=colors2,
    order=weather_df['weathersit']
)

weather_chart.set_title("Jumlah Penyewa Sepeda Berdasarkan Cuaca")
weather_chart.set_ylabel("Jumlah Penyewa (Ratus Ribu)")
weather_chart.set_xlabel("Cuaca")
st.pyplot()

# 3
st.header("The Highest and Lowest Number")

highlow_df = day_df.groupby(by="mnth").cnt.sum().reset_index()
highlow_df.rename(columns={
    "cnt": "sum"
}, inplace=True)

max_index = highlow_df['sum'].idxmax()
min_index = highlow_df['sum'].idxmin()
colors3 =["#D3D3D3" if i != max_index and i != min_index else "#72BCD4" for i in range(len(highlow_df))]

highlow_chart = sns.barplot(
    x="mnth", 
    y="sum",
    data=highlow_df.sort_values(by="sum", ascending=False),
    palette=colors3
)

highlow_chart.set_title("Jumlah penyewa tertinggi")
highlow_chart.set_ylabel("Jumlah")
highlow_chart.set_xlabel("Bulan")
st.pyplot()

st.caption('Copyright (c) nanditosamosir 2024')
