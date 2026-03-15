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
        
        # NORMALIZACIÓN DE COLUMNAS
        df.columns = [c.strip() for c in df.columns]
        raw_cols = {c.lower(): c for c in df.columns}
        
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

# --- PÁGINA DE INICIO (LANDING PAGE) ---
if page == "Inicio":
    st.title("🚀 Análisis del Mercado Laboral en IA y Data Science")
    
    try:
        st.image("imagen1.png", use_container_width=True)
    except:
        st.info("💡 Sube 'imagen1.png' a tu repositorio para verla aquí.")

    # AQUÍ ESTABA EL ERROR: Aseguramos el cierre de las triples comillas
    st.markdown("""
    ### Proyecto Talento Tech
    Bienvenida al panel de control para el análisis de tendencias en Ciencia de Datos e IA (2020-2026).
    
    **Elaborado por:** Michely Muñoz  
    **Objetivo:** Analizar salarios, roles y habilidades más críticas en la industria actual mediante un entorno de producción real.
    """)
    
    st.success("Dataset cargado exitosamente desde KaggleHub.")

# --- DASHBOARD ---
elif page == "Dashboard":
    st.title("📊 Panel de Control de Datos")
    
    if df is not None:
        col1, col2, col3 = st.columns(3)
        
        if 'Salary_USD' in df.columns:
            avg_salary = df['Salary_USD'].mean()
            col1.metric("Salario Promedio", f"${avg_salary:,.0f} USD")
        
        if 'Job_Title' in df.columns:
            total_roles = df['Job_Title'].nunique()
            col2.metric("Roles Únicos", total_roles)
            
        col3.metric("Total de Registros", len(df))

        st.divider()

        if 'Salary_USD' in df.columns and 'Job_Title' in df.columns:
            st.subheader("Distribución de Salarios por Rol")
            fig_salary = px.box(df, x='Job_Title', y='Salary_USD', 
                                color='Experience_Level' if 'Experience_Level' in df.columns else None,
                                title="Análisis Salarial")
            st.plotly_chart(fig_salary, use_container_width=True)

        if 'Year' in df.columns:
            st.subheader("Evolución de Contrataciones")
            df_year = df.groupby('Year').size().reset_index(name='Cantidad')
            fig_trend = px.line(df_year, x='Year', y='Cantidad', markers=True)
            st.plotly_chart(fig_trend, use_container_width=True)

        if 'Required_Skills' in df.columns:
            st.subheader("Top 10 Habilidades Demandadas")
            skills = df['Required_Skills'].str.split(',').explode().str.strip().value_counts().head(10)
            fig_skills = px.bar(skills, x=skills.values, y=skills.index, orientation='h',
                               color=skills.values, color_continuous_scale='Bluered')
            st.plotly_chart(fig_skills, use_container_width=True)
    else:
        st.error("No se pudo cargar el dataset.")
