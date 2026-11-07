"""
=============================================================================
PROYECTO: SyncFit - Personal Workout & Fitness Web App
DESCRIPCIÓN: Aplicación web interactiva basada en arquitectura modular y 
             múltiples fuentes de datos CSV para gestión de rutinas, ejercicios,
             suscripciones, métricas y cumplimiento legal.
=============================================================================
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# =============================================================================
# 1. CONFIGURACIÓN INICIAL DE LA PÁGINA
# =============================================================================
st.set_page_config(
    page_title="SyncFit - Tu Entrenador y Gestor de Bienestar",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados (Dark Slate Theme & Neon Accents)
st.markdown("""
    <style>
    .main {
        background-color: #0F172A;
        color: #F8FAFC;
    }
    h1, h2, h3 {
        color: #10B981 !important;
        font-family: 'Inter', sans-serif;
    }
    .stMetric {
        background-color: #1E293B;
        border-radius: 12px;
        padding: 16px;
        border: 1px solid #334155;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    div[data-testid="stExpander"] {
        background-color: #1E293B;
        border: 1px solid #334155;
        border-radius: 10px;
    }
    .stButton>button {
        background-color: #10B981;
        color: #0F172A;
        font-weight: bold;
        border-radius: 8px;
        border: none;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #059669;
        color: #FFFFFF;
    }
    </style>
""", unsafe_allow_html=True)

# =============================================================================
# 2. CARGA Y VALIDACIÓN DE DATOS (LOS 5 ARCHIVOS CSV)
# =============================================================================
@st.cache_data
def cargar_datos_syncfit():
    try:
        df_modulos = pd.read_csv("SyncFit_1_Modulos_Web.csv")
        df_ejercicios = pd.read_csv("SyncFit_2_Base_Ejercicios.csv")
        df_planes = pd.read_csv("SyncFit_3_Planes_Suscripciones.csv")
        df_legal = pd.read_csv("SyncFit_4_Matriz_Legal.csv")
        df_kpis = pd.read_csv("SyncFit_5_Metricas_KPIs.csv")
        return df_modulos, df_ejercicios, df_planes, df_legal, df_kpis
    except FileNotFoundError as fnf_error:
        st.error(f"⚠️ Error crítico: Asegúrate de tener los 5 archivos CSV en la misma carpeta. Detalle: {fnf_error}")
        st.stop()
    except Exception as e:
        st.error(f"⚠️ Ocurrió un error inesperado al leer los archivos: {e}")
        st.stop()

df_modulos, df_ejercicios, df_planes, df_legal, df_kpis = cargar_datos_syncfit()

# =============================================================================
# 3. BARRA LATERAL (SIDEBAR) Y NAVEGACIÓN
# =============================================================================
st.sidebar.image("https://images.pexels.com/photos/1432039/pexels-photo-1432039.jpeg?auto=compress&cs=tinysrgb&w=400", use_container_width=True)
st.sidebar.title("⚡ SYNCFIT PORTAL")
st.sidebar.markdown(f"**Versión:** 2.5.0 Pro | **Estado:** Activo 🟢")
st.sidebar.markdown(f"**Fecha:** {datetime.now().strftime('%d/%m/%Y')}")
st.sidebar.markdown("---")

menu_opcion = st.sidebar.radio(
    "Navegación Principal:",
    [
        "🏠 Dashboard General",
        "🏋️ Biblioteca de Ejercicios",
        "🤖 Generador de Rutinas IA",
        "🚀 Planes & Suscripciones",
        "📈 Analíticas & KPIs",
        "🛡️ Matriz Legal & Salud",
        "📐 Arquitectura Web (Módulos)"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("💡 **Consejo Pro:** Usa los filtros interactivos en cada sección para personalizar tus entrenamientos.")

# =============================================================================
# 4. MÓDULO 1: DASHBOARD GENERAL
# =============================================================================
if menu_opcion == "🏠 Dashboard General":
    st.title("⚡ Panel de Control General - SyncFit")
    st.write("Bienvenido a tu centro de control integral de rendimiento físico, rutinas y analíticas de la plataforma.")
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Ejercicios Registrados", len(df_ejercicios), "+2 esta semana")
    c2.metric("Módulos Web Activos", len(df_modulos), "100% operativos")
    c3.metric("Planes Disponibles", len(df_planes), "Desde $0 MXN")
    c4.metric("Retención Promedio", "> 40%", "Meta superada 🟢")
    
    st.markdown("---")
    
    col_izq, col_der = st.columns(2)
    
    with col_izq:
        st.subheader("🏋️ Resumen de Grupos Musculares")
        if "Grupo_Muscular" in df_ejercicios.columns:
            conteo_musculos = df_ejercicios["Grupo_Muscular"].value_counts().reset_index()
            conteo_musculos.columns = ["Grupo Muscular", "Cantidad"]
            fig_bar = px.bar(
                conteo_musculos, 
                x="Grupo Muscular", 
                y="Cantidad", 
                color="Cantidad",
                color_continuous_scale="Greens",
                title="Distribución de Ejercicios por Músculo"
            )
            fig_bar.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="white")
            st.plotly_chart(fig_bar, use_container_width=True)
            
    with col_der:
        st.subheader("🚀 Niveles de Suscripción Activos")
        for _, plan in df_planes.iterrows():
            with st.expander(f"📌 Plan: {plan['Nivel_Plan']} (${plan['Precio_MXN_Mes']} MXN/mes)"):
                st.write(f"* **Límite:** {plan['Limite_Rutinas']}")
                st.write(f"* **Funciones:** {plan['Funcionalidades_Incluidas']}")

# =============================================================================
# 5. MÓDULO 2: BIBLIOTECA DE EJERCICIOS
# =============================================================================
elif menu_opcion == "🏋️ Biblioteca de Ejercicios":
    st.title("🏋️ Biblioteca Maestra de Ejercicios")
    st.write("Explora, filtra y consulta los detalles técnicos de cada movimiento disponible en la base de datos.")
    
    f1, f2, f3 = st.columns(3)
    with f1:
        filtro_musculo = st.multiselect("Filtrar por Grupo Muscular:", options=df_ejercicios["Grupo_Muscular"].unique())
    with f2:
        filtro_nivel = st.multiselect("Filtrar por Dificultad:", options=df_ejercicios["Dificultad"].unique())
    with f3:
        busqueda_texto = st.text_input("🔍 Buscar ejercicio por nombre:", "")
        
    df_filtrado = df_ejercicios.copy()
    if filtro_musculo:
        df_filtrado = df_filtrado[df_filtrado["Grupo_Muscular"].isin(filtro_musculo)]
    if filtro_nivel:
        df_filtrado = df_filtrado[df_filtrado["Dificultad"].isin(filtro_nivel)]
    if busqueda_texto:
        df_filtrado = df_filtrado[df_filtrado["Nombre_Ejercicio"].str.contains(busqueda_texto, case=False, na=False)]
        
    st.markdown(f"### Mostrando {len(df_filtrado)} ejercicios encontrados")
    
    for _, row in df_filtrado.iterrows():
        with st.expander(f"💪 {row['Nombre_Ejercicio']} | 🎯 Músculo: {row['Grupo_Muscular']} | ⚡ Dificultad: {row['Dificultad']}"):
            col_a, col_b, col_c, col_d = st.columns(4)
            col_a.metric("Series Sugeridas", row["Series_Sugeridas"])
            col_b.metric("Reps / Duración", row["Reps_Tiempo"])
            col_c.metric("Descanso", f"{row['Descanso_Seg']} seg")
            col_d.metric("Nivel", row["Dificultad"])
            st.markdown(f"🔧 **Equipamiento necesario:** `{row['Equipamiento']}`")

    st.markdown("---")
    with st.form("form_nuevo_ejercicio"):
        st.subheader("➕ Agregar Nuevo Ejercicio a la Sesión")
        nuevo_nombre = st.text_input("Nombre del Ejercicio")
        nuevo_musculo = st.text_input("Grupo Muscular")
        nuevo_equipo = st.text_input("Equipamiento")
        nuevo_dif = st.selectbox("Dificultad", ["Principiante", "Intermedio", "Avanzado"])
        btn_agregar = st.form_submit_button("Registrar Ejercicio")
        if btn_agregar and nuevo_nombre:
            st.success(f"¡Ejercicio '{nuevo_nombre}' agregado correctamente al flujo de trabajo temporal!")

# =============================================================================
# 6. MÓDULO 3: GENERADOR DE RUTINAS IA
# =============================================================================
elif menu_opcion == "🤖 Generador de Rutinas IA":
    st.title("🤖 Generador Inteligente de Rutinas (IA)")
    st.write("Configura tus parámetros personales para que nuestro algoritmo diseñe una sesión de entrenamiento a tu medida.")
    
    with st.form("config_ia"):
        col1, col2 = st.columns(2)
        with col1:
            meta_usuario = st.selectbox(
                "¿Cuál es tu objetivo principal?",
                ["Hipertrofia y Volumen", "Fuerza Máxima", "Pérdida de Grasa / Definición", "Resistencia y Acondicionamiento Core"]
            )
            dias_semana = st.slider("Días disponibles por semana:", min_value=2, max_value=6, value=4)
        with col2:
            nivel_experiencia = st.select_slider(
                "Tu nivel actual de experiencia:",
                options=["Principiante", "Intermedio", "Avanzado"]
            )
            tiempo_sesion = st.selectbox("Duración ideal por sesión:", ["45 minutos", "60 minutos", "75 minutos", "90 minutos"])
            
        boton_generar = st.form_submit_button("✨ Generar Rutina Personalizada con IA")
        
    if boton_generar:
        st.balloons()
        st.success(f"¡Rutina generada con éxito para objetivo: **{meta_usuario}** ({dias_semana} días/semana)!")
        
        st.markdown("### 📋 Estructura de tu Sesión Sugerida:")
        ejercicios_ia = df_ejercicios[df_ejercicios["Dificultad"] == nivel_experiencia]
        if ejercicios_ia.empty:
            ejercicios_ia = df_ejercicios.head(4)
            
        st.dataframe(
            ejercicios_ia[["ID_Ejercicio", "Nombre_Ejercicio", "Grupo_Muscular", "Equipamiento", "Series_Sugeridas", "Reps_Tiempo", "Descanso_Seg"]],
            use_container_width=True
        )
        
        st.info("💡 **Recomendación del Coach IA:** Mantén una correcta hidratación y registra cada serie completada para medir tu sobrecarga progresiva en la app.")

# =============================================================================
# 7. MÓDULO 4: PLANES Y SUSCRIPCIONES
# =============================================================================
elif menu_opcion == "🚀 Planes & Suscripciones":
    st.title("🚀 Modelos de Suscripción y Precios SyncFit")
    st.write("Elige el plan ideal para desbloquear todo el potencial de nuestra plataforma de entrenamiento.")
    
    cols_planes = st.columns(len(df_planes))
    for i, (_, plan) in enumerate(df_planes.iterrows()):
        with cols_planes[i]:
            st.markdown(f"### 🏷️ {plan['Nivel_Plan']}")
            st.markdown(f"## **${plan['Precio_MXN_Mes']}** `MXN/mes`")
            st.markdown("---")
            st.write(f"🔒 **Límite:** {plan['Limite_Rutinas']}")
            st.write(f"☁️ **Respaldo:** {plan['Copia_Seguridad']}")
            st.write(f"💬 **Soporte:** {plan['Tipo_Soporte']}")
            st.success(f"✨ **Beneficios:** {plan['Funcionalidades_Incluidas']}")
            
            if st.button(f"Suscribirme a {plan['Nivel_Plan']}", key=f"plan_btn_{i}"):
                st.toast(f"¡Has seleccionado el plan {plan['Nivel_Plan']}! Redirigiendo a pasarela segura...", icon="🚀")

# =============================================================================
# 8. MÓDULO 5: ANALÍTICAS & KPIS
# =============================================================================
elif menu_opcion == "📈 Analíticas & KPIs":
    st.title("📈 Dashboard de Métricas y KPIs de la App")
    st.write("Seguimiento analítico del rendimiento de usuarios, tasas de retención y conversión comercial.")
    
    k1, k2, k3, k4 = st.columns(4)
    for idx, (_, kpi) in enumerate(df_kpis.iterrows()):
        if idx == 0:
            k1.metric(kpi["KPI_Metrica"], kpi["Objetivo_Meta"], f"Freq: {kpi['Frecuencia_Medicion']}")
        elif idx == 1:
            k2.metric(kpi["KPI_Metrica"], kpi["Objetivo_Meta"], f"Freq: {kpi['Frecuencia_Medicion']}")
        elif idx == 2:
            k3.metric(kpi["KPI_Metrica"], kpi["Objetivo_Meta"], f"Freq: {kpi['Frecuencia_Medicion']}")
        elif idx == 3:
            k4.metric(kpi["KPI_Metrica"], kpi["Objetivo_Meta"], f"Freq: {kpi['Frecuencia_Medicion']}")
            
    st.markdown("---")
    st.subheader("📋 Detalle de Estrategias y Métodos de Medición")
    st.dataframe(df_kpis, use_container_width=True)
    
    st.subheader("📊 Gráfica de Proyección de Crecimiento Activo (DAU/MAU)")
    df_chart_sim = pd.DataFrame({
        "Mes": ["Mes 1", "Mes 2", "Mes 3", "Mes 4", "Mes 5", "Mes 6"],
        "Usuarios Activos": [120, 350, 780, 1420, 2600, 4800]
    })
    fig_line = px.line(df_chart_sim, x="Mes", y="Usuarios Activos", markers=True, title="Crecimiento Proyectado de Usuarios Activos")
    fig_line.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="white")
    st.plotly_chart(fig_line, use_container_width=True)

# =============================================================================
# 9. MÓDULO 6: MATRIZ LEGAL & SALUD
# =============================================================================
elif menu_opcion == "🛡️ Matriz Legal & Salud":
    st.title("🛡️ Matriz de Cumplimiento Legal y Salud")
    st.write("Descargos de responsabilidad, políticas de privacidad biométrica y normativas aplicadas en la plataforma.")
    
    for _, leg in df_legal.iterrows():
        with st.expander(f"⚖️ Área: {leg['Area_Riesgo']} | Requerimiento: {leg['Requerimiento_Legal']}"):
            st.warning(f"**Cláusula Oficial:** {leg['Texto_Clausula_Sugerida']}")
            st.caption(f"📖 **Fundamento Legal / Referencia:** `{leg['Norma_Ley_Referencial']}`")

# =============================================================================
# 10. MÓDULO 7: ARQUITECTURA WEB (MÓDULOS)
# =============================================================================
elif menu_opcion == "📐 Arquitectura Web (Módulos)":
    st.title("📐 Arquitectura y Estructura del Sitio Web")
    st.write("Mapa completo de pantallas, componentes visuales, llamadas a la acción (CTA) y estatus de desarrollo.")
    st.dataframe(df_modulos, use_container_width=True)

# =============================================================================
# PIE DE PÁGINA GLOBAL
# =============================================================================
st.markdown("---")
st.markdown("<p style='text-align: center; color: #94A3B8;'>SyncFit Web App © 2026 | Desarrollado con Python, Streamlit y Pandas para máxima potencia y rendimiento.</p>", unsafe_allow_html=True)