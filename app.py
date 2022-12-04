import pandas as pd
import streamlit as st
import plotly.express as px

@st.cache(allow_output_mutation=True)
def load_df(path):
    df = pd.read_csv(path)
    return df
    
@st.cache
def get_hour_df(df):
    hour_df = df.copy(deep=True)
    hour_df['hour'] = hour_df['started_at'].astype(str).str[10:13]
    hour_df.sort_values(by=['hour'],inplace=True)
    return hour_df

@st.cache
def get_fig1(hour_df):
    fig1 = px.histogram(hour_df['hour'], x='hour')
    return fig1

@st.cache
def get_fig2(hour_df):
    fig2 = px.scatter_mapbox(hour_df[hour_df['hour'].astype(int) == int(hourFilterValue)], lat="start_lat", lon="start_lng",zoom=12)
    fig2.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig2.update_layout(mapbox_style="open-street-map")
    return fig2


st.title('NYC App')

df = load_df('nyc.csv')
hour_df = get_hour_df(df)

fig1 = get_fig1(hour_df)

with st.sidebar:
    showRawData = st.checkbox('Mostrar datos')
    showPerHour = st.checkbox('Recorridos por hora')
    showMap = st.checkbox('Mostrar mapa')
    hourFilterValue = st.slider('Hora: ',0,24)

fig2 = get_fig2(hour_df)

if showRawData:
    st.subheader('Datos')
    st.write(df)

if showPerHour:
    st.write(fig1)

if showMap:
    st.write(fig2)