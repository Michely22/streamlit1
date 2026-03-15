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
        
        # --- ARREGLO DE COLUMNAS PARA EVITAR ERRORES ---
        # Limpiamos espacios y estandarizamos nombres para que px.box no falle
        df.columns = [c.strip().replace(' ', '_') for c in df.columns]
        
        # Mapeo de seguridad: asegura que los nombres coincidan con los gráficos
        rename_map = {}
        for col in df.columns:
            if 'Salary' in col: rename_map[col] = 'Salary_USD'
            if 'Job' in col or 'Role' in col: rename_map[col] = 'Job_Title'
            if 'Experience' in col: rename_map[col] = 'Experience_Level'
            if 'Skill' in col: rename_map[col] = 'Required_Skills'
            if 'Year' in col: rename_map[col] = 'Year'
            if 'Country' in col: rename_map[col] = 'Country'
        
        df.rename(columns=rename_map, inplace=True)
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
    * Visualizar la evolución salarial por roles.
    * Identificar las habilidades más demandadas en IA.
    * Analizar la distribución geográfica del empleo.
    
    *Utiliza el menú de la izquierda para explorar el Dashboard.*
    """)
    
    st.info("Dataset obtenido de Kaggle: AI & Data Science Job Market Dataset")

# --- DASHBOARD ---
elif page == "Dashboard":
    st.title("📊 Panel de Control de Datos")
    
    if df is not None:
        # Verificación de columnas mínimas para evitar errores de Plotly
        if 'Salary_USD' in df.columns and 'Job_Title' in df.columns:
            # Métricas rápidas
            col1, col2, col3 = st.columns(3)
            col1.metric("Total de Registros", len(df))
            col2.metric("Salario Promedio (USD)", f"${df['Salary_USD'].mean():,.0f}")
            col3.metric("Países representados", df['Country'].nunique() if 'Country' in df.columns else "N/A")

            st.divider()

            # Gráfico 1: Distribución de Salarios por Rol
            st.subheader("Distribución de Salarios por Rol")
            fig_salary = px.box(df, x='Job_Title', y='Salary_USD', 
                                color='Experience_Level' if 'Experience_Level' in df.columns else None,
                                title="Salarios por Título y Nivel de Experiencia")
            st.plotly_chart(fig_salary, use_container_width=True)

            # Gráfico 2: Evolución de Contrataciones (Timeline)
            if 'Year' in df.columns:
                st.subheader("Tendencia de Contratación (2020-2026)")
                df_year = df.groupby('Year').size().reset_index(name='Jobs')
                fig_trend = px.line(df_year, x='Year', y='Jobs', markers=True, 
                                    title="Crecimiento de Empleos en el Tiempo")
                st.plotly_chart(fig_trend, use_container_width=True)

            # Gráfico 3: Skills más demandados (Top 10)
            if 'Required_Skills' in df.columns:
                st.subheader("Habilidades más demandadas")
                top_skills = df['Required_Skills'].str.split(',').explode().str.strip().value_counts().head(10)
                fig_skills = px.bar(top_skills, x=top_skills.values, y=top_skills.index, orientation='h',
                                   labels={'x': 'Frecuencia', 'y': 'Habilidad'},
                                   color=top_skills.values, color_continuous_scale='Viridis')
                st.plotly_chart(fig_skills, use_container_width=True)
        else:
            st.error(f"Error de columnas. Se detectaron: {list(df.columns)}")
    else:
        st.error("No se pudo cargar el dataset. Verifica la conexión con Kaggle.")
