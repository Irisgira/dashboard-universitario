# app.py
# Dashboard Analítico - Universidad
# Integrantes: [Nombre 1], [Nombre 2], [Nombre 3]

import streamlit as st
import pandas as pd
import plotly.express as px

# ---- CONFIGURACIÓN DE LA PÁGINA ----
st.set_page_config(
    page_title="Dashboard Universitario",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 Dashboard Analítico Universitario")
st.markdown("Análisis de admisiones, retención y satisfacción estudiantil.")

# ---- CARGA DEL DATASET ----
@st.cache_data
def cargar_datos():
    url = 'https://drive.google.com/uc?id=1V6Isem3ymsAPBo5DNlHIuTbm6flYU12Y'
    return pd.read_csv(url)

data = cargar_datos()

# ---- SIDEBAR: FILTROS INTERACTIVOS ----
st.sidebar.header("🔍 Filtros de Análisis")

años = sorted(data['Year'].unique())
filtro_años = st.sidebar.multiselect(
    "Selecciona los Años:",
    options=años,
    default=años
)

terms = data['Term'].unique().tolist()
filtro_term = st.sidebar.radio(
    "Selecciona el Semestre:",
    options=["Todos"] + terms
)

# ---- FILTRADO DINÁMICO ----
df = data[data['Year'].isin(filtro_años)]
if filtro_term != "Todos":
    df = df[df['Term'] == filtro_term]

# ---- SECCIÓN 1: KPIs ----
st.subheader("📌 Indicadores Clave")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Matriculados", f"{df['Enrolled'].sum():,}")
with col2:
    st.metric("Total Aspirantes", f"{df['Applications'].sum():,}")
with col3:
    st.metric("Retención Media", f"{round(df['Retention Rate (%)'].mean(), 1)}%")
with col4:
    st.metric("Satisfacción Media", f"{round(df['Student Satisfaction (%)'].mean(), 1)}%")

st.divider()

# ---- SECCIÓN 2: GRÁFICO DE LÍNEAS ----
st.subheader("📈 Evolución de Aspirantes y Admitidos por Año")
df_linea = df.groupby('Year')[['Applications', 'Admitted', 'Enrolled']].sum().reset_index()
fig_linea = px.line(
    df_linea, x='Year',
    y=['Applications', 'Admitted', 'Enrolled'],
    markers=True,
    title="Tendencia de Aspirantes, Admitidos y Matriculados"
)
st.plotly_chart(fig_linea, use_container_width=True)

# ---- SECCIÓN 3: GRÁFICO DE BARRAS (Facultades) ----
st.subheader("🏢 Estudiantes Matriculados por Facultad")
facs = {
    'Ingeniería': df['Engineering Enrolled'].sum(),
    'Negocios': df['Business Enrolled'].sum(),
    'Artes': df['Arts Enrolled'].sum(),
    'Ciencias': df['Science Enrolled'].sum()
}
df_facs = pd.DataFrame(list(facs.items()), columns=['Facultad', 'Cantidad'])
fig_barras = px.bar(
    df_facs, x='Facultad', y='Cantidad',
    color='Facultad',
    title="Distribución por Facultad"
)
st.plotly_chart(fig_barras, use_container_width=True)

# ---- SECCIÓN 4: GRÁFICO DE TORTA (Spring vs Fall) ----
st.subheader("🔄 Comparación Spring vs Fall")
df_term = data.groupby('Term')['Enrolled'].sum().reset_index()
fig_pie = px.pie(
    df_term, names='Term', values='Enrolled',
    title="Distribución de Matriculados por Semestre",
    color_discrete_sequence=px.colors.qualitative.Set2
)
st.plotly_chart(fig_pie, use_container_width=True)

# ---- FOOTER ----
st.divider()
st.caption("📊 Proyecto de Minería de Datos | Universidad de la Costa | 2025")