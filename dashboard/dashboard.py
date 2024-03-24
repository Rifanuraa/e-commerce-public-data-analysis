import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')


def create_daily_orders_df(df):
    daily_orders_df = df.resample(rule='D', on='order_purchase_timestamp').agg({
    
        "order_id": "nunique",
        "price": "sum"
    })
    daily_orders_df = daily_orders_df.reset_index()
    daily_orders_df.rename(columns={
        "order_id": "order_count",
        "price": "revenue"
    }, inplace=True)
    
    return daily_orders_df

def create_sum_order_items_df(df):
    sum_order_items_df = df.groupby("product_category_name").order_id.count().sort_values(ascending=False).reset_index()
    sum_order_items_df.rename(columns={
        "order_id": "order_count",
        "price": "revenue"
    }, inplace=True)
    return sum_order_items_df


def create_bystate_df(df):
    bystate_df = df.groupby(by="customer_state").customer_id.nunique().reset_index()
    bystate_df.rename(columns={
        "customer_id": "customer_count",
        "customer_state" : "state"
    }, inplace=True)
    
    return bystate_df

def create_price_df(df):
    price_df = df.groupby(by="customer_id", as_index=False).agg({
        "order_purchase_timestamp": "max", #mengambil tanggal order terakhir
        "order_id": "count",
        "price": "sum"
    }).sort_values(by="price", ascending=False)
    price_df.columns = ["customer_id", "max_order_timestamp", "frequency","monetary"]

    return price_df

#load all_data.csv
all_df = pd.read_csv("all_data.csv")




#mengurutkan DataFrame berdasarkan order_date serta memastikan kedua kolom tersebut bertipe datetime.
datetime_columns = ["order_purchase_timestamp", "order_delivered_carrier_date"]
all_df.sort_values(by="order_purchase_timestamp", inplace=True)
all_df.reset_index(inplace=True)
 
for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])


#filter 
min_date = all_df["order_purchase_timestamp"].min()
max_date = all_df["order_purchase_timestamp"].max()
 
with st.sidebar:
      #Menambahkan logo perusahaan
     st.image("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAOEAAADhCAMAAAAJbSJIAAAAeFBMVEUHBwj///8AAADZ2dmLi4vk5OSOjo7S0tKurq42Nje7u7v39/fExMRdXV2mpqbq6upvb29QUFFpaWmbm5vLy8uUlJTx8fGCgoJ6enq+vr7d3d1zc3MqKipJSUmzs7NaWloTExQnJyc7OzwbGxxLS0tCQkMfHx8xMTGxtj26AAAE4ElEQVR4nO2aaXuqMBBGZUBRoe5LXWqtrfr//+FlC5ks2uAtUPu851MLOskhMJkEOx0AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIAKkKTtrtQDzRZxwehvKlLPE2yF4d8aVgpKQ7/woeWooP/yBxRthuPy0PKPGnbLQz0YPgEwdA/0W/PvTxnSeTXOWM1/meKPGb6K7/SfwPCR2YL6z2Q4fREM3A39JzJ8pGojWj2T4SNh9l6bhvcGpKrhjVg0ac0w7c1gt+711ruBzbLSXZocOE7SWJM9O5l9cM4Mm5wZifbLMgUkDssPo9OWTDMaFmxmpASbDsunzVusO3ksOsXJR2X+7Ypvx/vaFZMuhZ7G4k11vD9b8PmQ3nwt1uEzPU1TvQ2BeyZ+WHBhazdWFJ1nfHYfSpZJrPYMaXar5Xc+Mo6GNLSG8tMbpSVDWt5q2PMCNjRuhjejbVszvCfIFd0M6XQr0ltbhrIQtlMmSUfD+EacaVvP4e1rLhCZ3MmQiH2zeziEUfH3jtrKpbRVmgrnQTBXJ46wkqGsWJLRT5lkDQTFbBFFkfxA+l9GnYa05jLDokg5KulwQhUM5UyRr6eSaMljMBcjTHxiGjVR0xC/pDPREvGh8MZVDOW1mZQP8JXvkZO8Q5qoSxUTXngpJ/JZ0c1ww0aoDKYUDg0bskdOfRlBB3lmU8FwxC+MzaBZQ575Iq0KVU5lR5wM+dwztz1gDRu+3BpCdRC/skzoZHhkhl5kcWzYkNXIesLmk1fgbNjRa/jhl+bYsCGbFcwVr6d2xdHw7GlsJy1mGtaauTHBuh+7G9rK3PELc2zYUK5gQ9PQV086r54sy0O20mzYUPZwYxrKrlQytNbyq3KfomFDWZTeHcNFJcMOfZgLjHIyathQJr6uaSj3kobVDJPJ9Gxsi/jtGLI5z5i3WC4dVTRMv33teyqigG/WkK0sZlpz/GnaVTbM1hEBL+vFc9Cw4ZvswEI3ZDuC1wcMM0f5A5WETl78NVx5y2fNO6t16Zc8M3avS7OjLMqeDeOpFUP2sGx56UGs88X61Xk+5D+t4ZXvNA8j66i4CcMBu4s2bFpWNpQ+qxgm2WvJA8lBLAzlRTXzdx2KfE9mUawESN0Djyus8fP0fJDvYj5knOIuZSVP/nzX+15GLZSz1U76ekhJgtfq+zTjL7EBw67gMTdkuwd+tinUP9erqE1bY98fq0fELyZcDOUS3w8Gx84gYJms+BJdePAw7BYFRX2GpAnpyN8hfm+ozg4aYvdc279Mqfk+vVh6I4k67oY8cZqByLwXlMtTo+I1snRI9Osq06LDGI5sMXLk5iIZ7Y1rTqo0WNm6lDX9wSZyl+dwbYuSwmZ3y8u8un+dSrdep2yUIsApl566tkDqPpc51HrJWIPizJJvuu8PvAMmWps3faSV9eY2wGftkz/RTnuRH070TTKZKEUxYv3VV7KmULPlamluKU6VoV681y6YdeyyHhZd2w7Xn2avLqdBgUg/dBVHThf2nBHte3GusApHU+u+ML0fsk9E28Nrp97ZgrfKuXv+ziEz1Pet/ajGt/xge9+HatgNAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgP/iH15tNJd0Li4eAAAAAElFTkSuQmCC")
    
     # Mengambil start_date & end_date dari date_input
     start_date, end_date = st.date_input(
         label='Rentang Waktu',min_value=min_date,
         max_value=max_date,
         value=[min_date, max_date]
     )

main_df = all_df[(all_df["order_purchase_timestamp"] >= str(start_date)) & 
                (all_df["order_purchase_timestamp"] <= str(end_date))]

daily_orders_df = create_daily_orders_df(main_df)
sum_order_items_df = create_sum_order_items_df(main_df)
bystate_df = create_bystate_df(main_df)
price_df = create_price_df(main_df)


#visualisasi
st.header('Brazilian E-Commerce Public Dataset by Olist Dashboard :sparkles:')
st.subheader('Daily Orders')
 
col1, col2 = st.columns(2)
 
with col1:
    total_orders = daily_orders_df.order_count.sum()
    st.metric("Total orders", value=total_orders)
 
with col2:
    total_revenue = format_currency(daily_orders_df.revenue.sum(), "AUD", locale='es_CO') 
    st.metric("Total Revenue", value=total_revenue)
 
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_orders_df["order_purchase_timestamp"],
    daily_orders_df["order_count"],
    marker='o', 
    linewidth=2,
    color= "#0000FF"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
 
st.pyplot(fig)

#peforma product
st.subheader("Best & Worst Performing Product")
 
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))
 
colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
 
sns.barplot(x="order_count", y="product_category_name", data=sum_order_items_df.head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Number of Sales", fontsize=30)
ax[0].set_title("Best Performing Product", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)
 
sns.barplot(x="order_count", y="product_category_name", data=sum_order_items_df.sort_values(by="order_count", ascending=True).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Number of Sales", fontsize=30)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Worst Performing Product", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)
 
st.pyplot(fig)

# costumer demographics
st.subheader("Customer Demographics")

fig, ax = plt.subplots(figsize=(20, 10))
colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
sns.barplot(
     x="customer_count", 
     y="state",
     data=bystate_df.sort_values(by="customer_count", ascending=False),
     palette=colors,
     ax=ax
 )
ax.set_title("Number of Customer by States", loc="center", fontsize=30)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)

st.subheader("Top order amount")

fig, ax = plt.subplots(figsize=(35, 15))
colors = ["#90CAF9", "#90CAF9", "#90CAF9", "#90CAF9", "#90CAF9"]
sns.barplot(y="monetary", x="frequency", data=price_df.sort_values(by="monetary", ascending=False).head(5), palette=colors)
plt.ylabel(None)
plt.xlabel(None) #("customer_id", fontsize=30)
plt.title("By Monetary", loc="center", fontsize=50)
plt.tick_params(axis='y', labelsize=30)
plt.tick_params(axis='x', labelsize=35)
 
st.pyplot(fig)

#review
st.subheader("Customer Review")

fig, ax = plt.subplots(figsize=(20, 10))

plt.hist(all_df['review_score'], bins=10, edgecolor='black')  
plt.xlabel('Review Score',  fontsize=30)
plt.ylabel('Frequency', fontsize=30)
plt.title('Distribution of Review Scores for Ordered Products', fontsize=30)
plt.tick_params(axis='y', labelsize=30)
plt.tick_params(axis='x', labelsize=30)
plt.grid(True)
plt.show()

st.pyplot(fig)
st.caption('Copyright (c) Dicoding 2023')