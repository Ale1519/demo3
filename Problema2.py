import pandas as pd
import streamlit as st
import plotly.express as px
import io

# ===================================================
# LECTURA DEL DATASET
# ===================================================
url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/04-18-2022.csv"
df = pd.read_csv(url)

st.title("Análisis COVID-19 (18/04/2022)")

# ===================================================
# 1.a) Primeras filas, info, valores nulos
# ===================================================
st.subheader("Primeras 10 filas")
st.dataframe(df.head(10))

st.subheader("Información general del dataset")
buffer = io.StringIO()
df.info(buf=buffer)
s = buffer.getvalue()
st.text(s)

st.subheader("Valores nulos por columna")
st.write(df.isnull().sum())

# ===================================================
# 1.b) Totales por país
# ===================================================
st.subheader("Totales por país")
totales_pais = df.groupby("Country_Region")[["Confirmed","Deaths","Recovered","Active"]].sum().reset_index()
st.dataframe(totales_pais)

# ===================================================
# 2.a) Mostrar todas las filas
# ===================================================
st.subheader("Mostrar todas las filas")
if st.checkbox("Ver todas las filas"):
    st.dataframe(df)
else:
    st.dataframe(df.head())

# ===================================================
# 2.b) Mostrar todas las columnas
# ===================================================
st.subheader("Mostrar todas las columnas")
if st.checkbox("Ver todas las columnas"):
    st.write(list(df.columns))
else:
    st.write("Muestra de columnas:", list(df.columns[:5]))

# ===================================================
# 2.c) Gráfica de líneas (muertos > 2500)
# ===================================================
st.subheader("Gráfica de líneas (países con fallecidos > 2500)")
mayores_2500 = totales_pais[totales_pais["Deaths"] > 2500]
fig_line = px.line(
    mayores_2500,
    x="Country_Region",
    y=["Confirmed","Deaths","Recovered","Active"],
    title="Casos por país (muertos > 2500)"
)
st.plotly_chart(fig_line)

# ===================================================
# 2.d) Barras fallecidos en estados de EE.UU.
# ===================================================
st.subheader("Fallecidos en estados de EE.UU.")
usa_states = df[df["Country_Region"]=="US"].groupby("Province_State")["Deaths"].sum().reset_index()
fig_bar = px.bar(usa_states, x="Province_State", y="Deaths", title="Fallecidos en EE.UU.")
st.plotly_chart(fig_bar)

# ===================================================
# 2.e) Pie chart fallecidos LATAM
# ===================================================
st.subheader("Fallecidos en países de LATAM")
paises = ["Colombia", "Chile", "Peru", "Argentina", "Mexico"]
latam = totales_pais[totales_pais["Country_Region"].isin(paises)]
fig_pie = px.pie(latam, names="Country_Region", values="Deaths", title="Fallecidos LATAM")
st.plotly_chart(fig_pie)

# ===================================================
# 2.f) Histograma fallecidos por país
# ===================================================
st.subheader("Histograma de fallecidos por país")
fig_hist = px.histogram(totales_pais, x="Deaths", nbins=30, title="Distribución de fallecidos por país")
st.plotly_chart(fig_hist)

# ===================================================
# 2.g) Boxplot Confirmed, Deaths, Recovered, Active
# ===================================================
st.subheader("Boxplot casos confirmados, fallecidos, recuperados y activos")
fig_box = px.box(
    totales_pais,
    y=["Confirmed","Deaths","Recovered","Active"],
    title="Boxplot casos COVID-19"
)
st.plotly_chart(fig_box)

