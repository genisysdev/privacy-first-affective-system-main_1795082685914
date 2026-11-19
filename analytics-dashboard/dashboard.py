import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# --- Configuración de la Página ---
st.set_page_config(page_title="Dashboard Emocional AI", layout="wide")
st.title("🤖 Dashboard de Registro Emocional")

# --- Carga de Datos ---
# NOTA: Cuando conectes la RPi, cambiarás esta ruta por la de red (ej. r'\\asistente-pi\datos\registro.csv')
ARCHIVO_CSV = "data/registro_emociones_dummy.csv"

@st.cache_data # Cache para no recargar el CSV si no ha cambiado
def cargar_datos():
    try:
        df = pd.read_csv(ARCHIVO_CSV)
        # Convertir fecha a tipo datetime para poder filtrarla
        df['Fecha'] = pd.to_datetime(df['Fecha'])
        return df
    except FileNotFoundError:
        st.error(f"No se encontró el archivo: {ARCHIVO_CSV}. Verifica la ruta.")
        return pd.DataFrame() # Retorna dataframe vacío para no romper el script

df = cargar_datos()

if df.empty:
    st.stop() # Detiene la ejecución si no hay datos

# --- Barra Lateral (Filtros) ---
st.sidebar.header("Filtros")

# Filtro de Fechas
fecha_min = df['Fecha'].min().date()
fecha_max = df['Fecha'].max().date()
rango_fechas = st.sidebar.date_input("Selecciona rango de fechas", [fecha_min, fecha_max])

# Filtro de Día de la Semana
dias_disponibles = df['Día'].unique()
dias_seleccionados = st.sidebar.multiselect("Selecciona Días", dias_disponibles, dias_disponibles)

# Aplicar Filtros
try:
    mask_fecha = (df['Fecha'].dt.date >= rango_fechas[0]) & (df['Fecha'].dt.date <= rango_fechas[1])
    mask_dias = df['Día'].isin(dias_seleccionados)
    df_filtrado = df[mask_fecha & mask_dias]
except IndexError:
    st.warning("Selecciona un rango de fechas válido.")
    st.stop()

# --- Cuerpo Principal del Dashboard ---

# KPIs (Indicadores Clave)
col1, col2, col3 = st.columns(3)
col1.metric("Total Registros", len(df_filtrado))
top_emocion = df_filtrado['Emoción'].mode()
col2.metric("Emoción Predominante", top_emocion[0] if not top_emocion.empty else "N/A")
col3.metric("Días con Registros", df_filtrado['Fecha'].nunique())

st.divider()

# Fila 1 de Gráficos
col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    st.subheader("Distribución de Emociones")
    conteo_emociones = df_filtrado['Emoción'].value_counts().reset_index()
    conteo_emociones.columns = ['Emoción', 'Cantidad']
    fig_torta = px.pie(conteo_emociones, values='Cantidad', names='Emoción', hole=0.4)
    st.plotly_chart(fig_torta, use_container_width=True)

with col_graf2:
    st.subheader("Nube de Palabras: Motivos")
    # Unir todos los textos de la columna 'Motivo'
    textos_motivos = " ".join(motivo for motivo in df_filtrado['Motivo'].dropna())
    
    if textos_motivos:
        # Crear y mostrar la nube de palabras
        wordcloud = WordCloud(width=800, height=400, background_color='white', colormap='viridis').generate(textos_motivos)
        fig_wc, ax = plt.subplots()
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis("off")
        st.pyplot(fig_wc)
    else:
        st.info("No hay suficientes datos de motivos para generar la nube de palabras.")

# Fila 2: Tabla de Datos Recientes
st.subheader("Últimos Registros (Vista de Datos)")
st.dataframe(df_filtrado.sort_values(by=['Fecha', 'Hora'], ascending=False).head(10), use_container_width=True)