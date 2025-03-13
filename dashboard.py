import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

#create
def create_season_rentals_df(all_df):
    season_rentals_df = (all_df.groupby("season")["cnt"].sum().sort_values(ascending=False).reset_index())
    return season_rentals_df                  

#create_rfm_df
def create_monthly_orders_df(all_df):
    all_df['dteday'] = pd.to_datetime(all_df['dteday'])
    monthly_orders_df = all_df.resample(rule='ME', on='dteday').agg({
        "registered": "nunique",
        "casual":"nunique",
        "cnt": "sum"
    })
    monthly_orders_df.index = monthly_orders_df.index.strftime('%Y-%m')
    monthly_orders_df = monthly_orders_df.reset_index()
    monthly_orders_df.rename(columns={
        "registered": "Pengguna Terdaftar",
        "casual":"Pengguna Tidak Terdaftar",
        "cnt": "Total Peminjaman"
    }, inplace=True)
    monthly_orders_df.rename(columns={
        "dteday": "Bulan",
        "cnt": "Total Peminjaman"
    }, inplace=True)
    monthly_orders_df.head()
    return monthly_orders_df



all_df = pd.read_csv("all_data.csv")
all_df["dteday"] = pd.to_datetime(all_df["dteday"])

min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()

min_date = min_date.date()
max_date = max_date.date()

with st.sidebar:

    start_date, end_date = st.date_input(
        label ='Rentang Waktu', min_value = min_date, max_value= max_date,
        value = [min_date, max_date]
    )
main_df = all_df [ (all_df["dteday"] >= str(start_date)) &
                    (all_df["dteday"] <= str(end_date) ) ]

season_rentals_df = create_season_rentals_df(main_df)
monthly_orders_df = create_monthly_orders_df(main_df)

st.header('Data Penyewaan Sepeda :bike:')

st.subheader("Pengaruh Musim dalam Jumlah Penyewaan Sepeda")

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35,12))

colors = ["#FF69B4", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(x="cnt", y="season", data=season_rentals_df.head(4), palette=colors,hue="season", ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Jumlah Peminjaman", fontsize=18)
ax[0].set_title("Peminjaman Paling Banyak", loc="center", fontsize=20)
ax[0].tick_params(axis ='x', labelsize=12)
ax[0].tick_params(axis ='y', labelsize=12)

sns.barplot(x="cnt", y="season", data=season_rentals_df.sort_values(by="cnt", ascending=True).head(4), palette=colors, hue="season", ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Jumlah Peminjaman", fontsize=18)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Peminjaman Paling Sedikit", loc="center", fontsize=20)
ax[1].tick_params(axis='x', labelsize=12)
ax[1].tick_params(axis='y', labelsize=12)

st.pyplot(fig)

st.subheader("Total Peminjaman Sepeda per Bulan (2011-2012)")
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(monthly_orders_df["Bulan"], monthly_orders_df["Total Peminjaman"], marker='o', linewidth=2, color="#FF69B4")

ax.set_xlabel("Bulan", fontsize=12)
ax.set_ylabel("Total Peminjaman", fontsize=12)
plt.xticks(rotation=45)
ax.grid(True, linestyle="--", alpha=0.6)

st.pyplot(fig)
