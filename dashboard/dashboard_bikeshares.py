import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.express as px


#' ' ' Menyiapkan komponen untuk data yang ditampilkan di dashboard ' ' '

st.set_page_config(page_title="Bikes-Sharing Dashboard",
                   page_icon="bar_chart:",
                   layout="wide")

#Input data harian ke src
df_day = pd.read_csv("https://raw.githubusercontent.com/dinata16/Analisi-Data-Python/main/datasets/alldata_bikeshare.csv")
df_day['dteday'] = pd.to_datetime(df_day['dteday'])

#Hapus kolom yang tidak perlu
drop_col = ['windspeed']

for i in df_day.columns:
  if i in drop_col:
    df_day.drop(labels=i, axis=1, inplace=True)

# Sesuaikan nama kolom
df_day.rename(columns={
    'dteday': 'dateday',
    'yr': 'year',
    'mnth': 'month',
    'weathersit': 'weather_cond',
    'cnt': 'count'
}, inplace=True)

# ubah data bulan
df_day['weather_cond'] = df_day['weather_cond'].map({
    1: 'Clear/Partly Cloudy',
    2: 'Misty/Cloudy',
    3: 'Light Snow/Rain',
    4: 'Severe Weather'
})

df_day['workingday'] = df_day['workingday'].map({
    0:'Not Workingday',
    1:'Workingday',

})


# Menyiapkan data sewa harian
def create_daily_rent(df):
    df_daily_rent = df.groupby(by='dateday').agg({'count': 'sum'}).reset_index()
    return df_daily_rent

# Menyiapkan sewa casual
def create_daily_casual(df):
    df_daily_casual_rent = df.groupby(by='dateday').agg({'casual': 'sum'}).reset_index()
    return df_daily_casual_rent

# Menyiapkan sewa registered
def create_daily_registered(df):
    df_daily_registered_rent = df.groupby(by='dateday').agg({'registered': 'sum'}).reset_index()
    return df_daily_registered_rent
    
# Menyiapkan sewa berdasarkan cuaca
def create_season_rent(df):
    df_season_rent = df.groupby(by='season')[['registered', 'casual']].sum().reset_index()

    df_season_rent = pd.melt(df_season_rent,
                                      id_vars=['season'],
                                      value_vars=['casual','registered'],
                                      var_name='type_of_rides',
                                      value_name='count')

    df_season_rent['season'] = pd.Categorical(df_season_rent['season'],
                                    categories=['Spring', 'Summer', 'Fall', 'Winter'])
 
    df_season_rent= df_season_rent.sort_values('season')
    return df_season_rent

# Menyiapkan sewa tiap bulan
def create_monthly_rent(df):
    df_monthly_rent = df.resample(rule='M', on='dateday').agg({
        "casual": "sum",
        "registered": "sum",
        "count": "sum"
    })
    df_monthly_rent.index = df_monthly_rent.index.strftime('%b-%y')
    df_monthly_rent = df_monthly_rent.reset_index()
    
    return df_monthly_rent

# Menyiapkan sewa berdasarkan weekday
def create_weekdays_rent(df):
    df_weekday_rent = df.groupby('weekday').agg({
        'count': 'sum',
        "casual": "sum",
        "registered": "sum",
        })
    df_weekday_rent = df_weekday_rent.reset_index()
    df_weekday_rent = pd.melt(df_weekday_rent,
                                      id_vars=['weekday'],
                                      value_vars=['count'],
                                      var_name='type_of_rides',
                                      value_name='count')

    df_weekday_rent['weekday'] = pd.Categorical(df_weekday_rent['weekday'],
                                    categories=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
 
    df_weekday_rent= df_weekday_rent.sort_values('weekday')
    return df_weekday_rent

# Menyiapkan berdasarkan workingday
def create_workingday_rent(df):
    df_workingday_rent = df.groupby(by='workingday').agg({'count': 'sum','casual': 'sum', 'registered': 'sum'}).reset_index()
    df_workingday_rent = pd.melt(df_workingday_rent,
                                      id_vars=['workingday'],
                                      value_vars=['casual','registered'],
                                      var_name='type_of_rides',
                                      value_name='count')

    df_workingday_rent['workingday'] = pd.Categorical(df_workingday_rent['workingday'],
                                    categories=['Not Workingday', 'Workingday'])    
    return df_workingday_rent

# Menyiapkan sewa berdasarkan cuaca
def create_weather_rent(df):
    df_weather_rent = df.groupby(by='weather_cond').agg({'count': 'sum'}).reset_index()
    return df_weather_rent

#Menyiapkan data sewa berdasarkan jam
def create_hourly_rent(df):
    df_hourly= df.groupby('hr').agg({
        'count': 'sum',
        'casual': 'sum',
        'registered': 'sum',
    })
    df_hourly=df_hourly.reset_index()
    return df_hourly

# Membuat filter berdasarkan date
min_date = df_day["dateday"].min()
max_date = df_day["dateday"].max()

with st.sidebar:
    st.image("https://raw.githubusercontent.com/dinata16/Analisi-Data-Python/main/image/pngwing.com.png")
    
    start_date, end_date = st.date_input(
        label='Select Time Range: ',
        min_value= min_date,
        max_value= max_date,
        value=[min_date, max_date]
    )

df_maindt = df_day[(df_day['dateday'] >= str(start_date)) & 
                (df_day['dateday'] <= str(end_date))]

# Meembuat dataframe baru untuk dashboard
df_daily_rent = create_daily_rent(df_maindt)
df_daily_casual_rent = create_daily_casual(df_maindt)
df_daily_registered_rent = create_daily_registered(df_maindt)

df_season_rent = create_season_rent(df_maindt)
df_monthly_rent = create_monthly_rent(df_maindt)
df_weekday_rent = create_weekdays_rent(df_maindt)
df_workingday_rent = create_workingday_rent(df_maindt)
df_weather_rent = create_weather_rent(df_maindt)

df_hourly= create_hourly_rent(df_maindt)



# ' ' ' Membuat Tampilan Dashboard ' ' '

# Judul
st.header('📈 Bikes-Sharing Dashboard ')

# Membuat jumlah penyewaan harian
st.subheader('Daily Rentals')
col1, col2, col3 = st.columns(3)

with col1:
    daily_rent_registered = df_daily_registered_rent['registered'].sum()
    st.metric('Registered User', value= daily_rent_registered)

with col2:
    daily_rent_casual = df_daily_casual_rent['casual'].sum()
    st.metric('Casual User', value= daily_rent_casual)
 
with col3:
    daily_rent_total = df_daily_rent['count'].sum()
    st.metric('Total User', value= daily_rent_total)

st.markdown('---')

# Membuat jumlah penyewaan bulanan
fig = px.line(
    df_monthly_rent,
    x='dateday',
    y='count',
    markers=True,
    color_discrete_sequence=['darkorange'],
    title="Monthly Count of Bikeshares").update_layout(xaxis_title='', yaxis_title='Count')
st.plotly_chart(fig, use_container_width=True)

# Membuat jumlah penyewaan berdasarkan season
fig = px.bar(
    df_season_rent,
    x='season',
    y=['count'],
    color='type_of_rides',
    color_discrete_sequence=['darkorange','blue'],
    title="Seasonly Count of Bikeshares").update_layout(xaxis_title='', yaxis_title='Count')
st.plotly_chart(fig, use_container_width=True)

# Membuah jumlah penyewaan berdasarkan kondisi cuaca
fig = px.bar(
    df_weather_rent,
    x='weather_cond',
    y=['count'],
    color= 'weather_cond',
    title="Count of Bikeshares by Weather Condition").update_layout(xaxis_title='', yaxis_title='Count')
st.plotly_chart(fig, use_container_width=True)

# Membuat jumlah penyewaan berdasarkan weekday, working dan holiday

fig1 = px.bar(
    df_weekday_rent,
    x='weekday',
    y=['count'],
    color='weekday',
    title="Count of Bikeshares by Weekday").update_layout(xaxis_title='', yaxis_title='Count')

fig2 = px.bar(
    df_workingday_rent,
    x='workingday',
    y=['count'],
    color='type_of_rides',
    color_discrete_sequence=['darkorange','blue'],
    title="Count of Bikeshares by Workingday").update_layout(xaxis_title='', yaxis_title='Count')

left_column, right_column= st.columns(2)
left_column.plotly_chart(fig1, use_container_width=True)
right_column.plotly_chart(fig2, use_container_width=True)

fig = px.line(
    df_hourly,
    x='hr',
    y=['count','casual', 'registered'],
    markers=True,
    color_discrete_sequence=['skyblue','orange','green'],
    title="Hourly Count of Bikeshares").update_layout(xaxis_title='', yaxis_title='Count')
st.plotly_chart(fig, use_container_width=True)

st.caption('Copyright(©) Rizki Dinata 2023')