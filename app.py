import streamlit as st
import pandas as pd
import plotly.express as px
import kagglehub
import os

# Configuración de la página
st.set_page_config(page_title="AI & Data Science Job Market Analysis", layout="wide")

# --- CARGA DE DATOS ---
@st.cache_data
def load_data():
    # Descarga del dataset desde Kaggle
    path = kagglehub.dataset_download("shree0910/ai-and-data-science-job-market-dataset-20202026")
    
    # Buscamos el archivo CSV en la ruta descargada
    csv_files = [f for f in os.listdir(path) if f.endswith('.csv')]
    if csv_files:
        full_path = os.path.join(path, csv_files[0])
        df = pd.read_csv(full_path)
        
        # ARREGLO PARA COLUMNAS: Limpia espacios y asegura que 'Salary_USD' sea reconocido
        df.columns = [c.strip() for c in df.columns]
        if 'Salary_USD' not in df.columns:
            # Si el nombre es ligeramente distinto, intentamos encontrarlo
            col_salario = [c for c in df.columns if 'Salary' in c]
            if col_salario:
                df.rename(columns={col_salario[0]: 'Salary_USD'}, inplace=True)
                
        return df
    return None

df = load_data()

# --- NAVEGACIÓN ---
st.sidebar.title("Navegación")
page = st.sidebar.radio("Ir a:", ["Inicio", "Dashboard"])

# --- PÁGINA DE INICIO (LANDING PAGE) ---
if page == "Inicio":
    st.title("🚀 Análisis del Mercado Laboral en IA y Data Science (2020–2026)")
    
    # Imagen de inicio
    try:
        st.image("imagen1.png", use_container_width=True)
    except:
        st.warning("Archivo 'imagen1.png' no encontrado en el repositorio. Asegúrate de cargarlo en Git.")

    st.markdown("""
    ### Bienvenida al Proyecto de Análisis de Datos
    Este tablero interactivo ha sido desarrollado para el curso **Talento Tech** con el fin de explorar las tendencias, 
    habilidades y salarios en el sector tecnológico global.
    
    **Objetivos del Proyecto:**
