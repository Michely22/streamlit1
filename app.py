import streamlit as st
import pandas as pd
import plotly.express as px
import kagglehub
import os

# 1. Configuración de la página
st.set_page_config(page_title="AI & Data Science Job Market Analysis", layout="wide")

# 2. Función de Carga y Limpieza de Datos
@st.cache_data
def load_data():
    try:
        # Descarga automática desde Kaggle
        path = kagglehub.dataset_download("shree0910/ai-and-data-science-job-market-dataset-20202026")
        csv_files = [f for f in os.listdir(path) if f.endswith('.csv')]
        
        if not csv_files:
            return None
            
        full_path = os.path.join(path, csv_files[0])
        df = pd.read_csv(full_path)
        
        # --- NORMALIZACIÓN DE COLUMNAS (Para evitar KeyErrors) ---
        # 1. Quitamos espacios y pasamos a minúsculas para comparar
        df.columns = [c.strip() for c in df.columns]
        raw_cols = {c.lower(): c for c in df.columns}
        
        # 2. Mapeo inteligente de nombres
        mapping = {}
        for low_name, original in raw_cols.items():
            if 'salary' in low_name: mapping[original] = 'Salary_USD'
            elif 'job' in low_name or 'role' in low_name: mapping[original] = 'Job_Title'
            elif 'exp' in low_name: mapping[original] = 'Experience_Level'
            elif 'year' in low_name: mapping[original] = 'Year'
            elif 'skill' in low_name: mapping[original] = 'Required_Skills'
            elif 'country' in low_name or 'location' in low_name: mapping[original] = 'Country'
        
        df = df.rename(columns=mapping)
        return df
    except Exception as e:
        st.error(f"Error al cargar datos: {e}")
        return None

df = load_data()

# 3. Navegación Lateral
st.sidebar.title("Navegación")
page = st.sidebar.radio("Ir a:", ["Inicio", "Dashboard"])

# --- PÁGINA DE INICIO ---
if page == "Inicio":
    st.title("🚀 Análisis del Mercado Laboral en IA y Data Science")
    
    # Imagen cargada desde el repositorio Git
    try:
        st.image("imagen1.png", use_container_width=True)
    except:
        st.info("💡 Para visualizar la imagen, asegúrate de subir 'imagen1.png' a tu repositorio.")

    st.markdown("""
    ### Proyecto Talento Tech
    Bienvenida al panel de control para el análisis de tendencias en Ciencia de Datos e IA (2020-202
