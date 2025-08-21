import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# URL del dataset (Johns Hopkins 18-04-2022)
url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/04-18-2022.csv"

# ==========================================
# 1. LECTURA DEL DATASET
# ==========================================
st.title("Análisis COVID-19 (18/04/2022)")

df = pd.read_csv(url)

# a) Mostrar las 10 primeras líneas, info y valores faltantes
st.subheader("Primeras 10 filas del dataset")
st.dataframe(df.head(10))

st.subheader("Información general del dataset")
buffer = []
df.info(buf=buffer)
s = "\n".join(buffer)
st.text(s)

st.subheader("Valores nulos por columna")
st.write(df.isnull().sum())

# b) Casos confirmados, fallecidos, recuperados y activos por país
st.subheader("Totales por país")
totales_pais = df.groupby("Country_Region")[["Confirmed", "Deaths", "Recovered", "Active"]].sum()
st.dataframe(totales_pais)

# ==========================================
# 2. ANÁLISIS Y GRÁFICAS
# ==========================================

# a) Mostrar todas las filas
st.subheader("Mostrar todas las filas")
if st.checkbox("Ver todas las filas"):
    st.dataframe(df)
else:
    st.dataframe(df.head())

# b) Mostrar todas las columnas
st.subheader("Mostrar todas las columnas")
if st.checkbox("Ver todas las columnas"):
    st.write(list(df.columns))
else:
    st.write("Muestra de columnas:", list(df.columns[:5]))

# c) Gráfica de líneas (países con fallecidos > 2500)
st.subheader("Gráfica de líneas (países con fallecidos > 2500)")
mayores_2500 = totales_pais[totales_pais["Deaths"] > 2500]
fig, ax = plt.subplots()
mayores_2500[["Confirmed", "Deaths", "Recovered", "Active"]].plot(kind="line", ax=ax)
plt.xticks(rotation=90)
st.pyplot(fig)

# d) Gráfica de barras (fallecidos en Estados de EE.UU.)
st.subheader("Fallecidos en estados de EE.UU.")
usa_states = df[df["Country_Region"] == "US"].groupby("Province_State")["Deaths"].sum()
fig, ax = plt.subplots()
usa_states.sort_values(ascending=False).plot(kind="bar", ax=ax)
plt.xticks(rotation=90)
st.pyplot(fig)

# e) Pie chart de fallecidos en países específicos
st.subheader("Fallecidos en países de LATAM")
paises = ["Colombia", "Chile", "Peru", "Argentina", "Mexico"]
latam = totales_pais.loc[paises]["Deaths"]

fig, ax = plt.subplots()
latam.plot(kind="pie", autopct="%1.1f%%", ax=ax)
ax.set_ylabel("")
st.pyplot(fig)

# f) Histograma de fallecidos por país
st.subheader("Histograma de fallecidos por país")
fig, ax = plt.subplots()
totales_pais["Deaths"].plot(kind="hist", bins=30, ax=ax)
st.pyplot(fig)

# g) Boxplot de Confirmed, Deaths, Recovered, Active
st.subheader("Boxplot de Confirmed, Deaths, Recovered y Active")
fig, ax = plt.subplots()
totales_pais[["Confirmed", "Deaths", "Recovered", "Active"]].plot(kind="box", ax=ax)
st.pyplot(fig)
