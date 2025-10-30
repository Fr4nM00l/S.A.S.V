"""
Punto de entrada de la app Streamlit.
"""

import streamlit as st
import sys, os
from PIL import Image 
from pathlib import Path
sys.path.append(os.path.dirname(__file__))

from app.data_loader import cargar_datos
from app.mapa import crear_mapa_argentina_interactivo, crear_mapa_de_calor
from app.estadisticas import mostrar_estadisticas_detalladas
from app.comparativo import mostrar_analisis_comparativo
from app.registro_nuevo_incidente import mostrar_formulario_registro
from app.prediccion_ml import mostrar_interfaz_prediccion
from app.graficos import (
    crear_graficos_tipo_lugar,
    crear_graficos_victima_vehiculo,
    crear_graficos_inculpado_vehiculo,
    crear_graficos_modo_produccion_hecho
)
from streamlit_folium import st_folium

# --- Estilos CSS personalizados ---
st.markdown("""
<style>
/* === FONDO GENERAL === */
body {
    background: radial-gradient(circle at top left, #101010, #0b0b0b);
    color: #e5e5e5;
    font-family: 'Segoe UI', sans-serif;
}

.sidebar {
    background-color: #0f0f0f;
    width: 280px;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: 25px 20px;
    color: #ddd;
    box-shadow: 3px 0 8px rgba(0, 0, 0, 0.6);
    transition: width 0.3s ease;
    overflow-y: auto;
}

/* === LOGO Y TÍTULO === */
.sidebar-logo {
    display: flex;
    align-items: center;
    justify-content: flex-start;
    margin-bottom: 30px;
}

.sidebar-logo img {
    width: 70px;
    height: 70px;
    margin-right: 10px;
}

.sidebar-logo h1 {
    font-size: 1.6rem;
    color: #ff7b00;
    font-weight: bold;
    letter-spacing: 1px;
    margin: 0;
}

/* === PANEL DE ANÁLISIS === */
.sidebar-section {
    margin-top: 20px;
}

.sidebar-section h3 {
    font-size: 1rem;
    color: #ffc107;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 6px;
}

.sidebar-section h3::before {
    content: "📂";
}

.sidebar-options {
    display: flex;
    flex-direction: column;
    gap: 8px;
    padding-left: 5px;
}

/* === BOTONES === */
.sidebar-button {
    display: flex;
    align-items: center;
    gap: 10px;
    background-color: #1a1a1a;
    border: 1px solid #2d2d2d;
    color: #ccc;
    padding: 10px 15px;
    font-size: 0.95rem;
    border-radius: 10px;
    transition: all 0.2s ease;
    cursor: pointer;
}

.sidebar-button:hover {
    background-color: #2a2a2a;
    color: #fff;
    border-color: #ff7b00;
    transform: scale(1.03);
}

.sidebar-button.active {
    background-color: #ff7b00;
    color: #000;
    font-weight: bold;
    border: none;
}

/* === SCROLLBAR PERSONALIZADA === */
.sidebar::-webkit-scrollbar {
    width: 8px;
}

.sidebar::-webkit-scrollbar-thumb {
    background: #333;
    border-radius: 10px;
}

.sidebar::-webkit-scrollbar-thumb:hover {
    background: #555;
}

/* === PEQUEÑOS AJUSTES RESPONSIVOS === */
@media (max-width: 900px) {
    .sidebar {
        width: 220px;
        padding: 20px 10px;
    }
    .sidebar-button {
        font-size: 0.85rem;
        padding: 8px 10px;
    }
    .sidebar-logo img {
        width: 55px;
        height: 55px;
    }
    .sidebar-logo h1 {
        font-size: 1.3rem;
    }
}

/* === PANEL DE CONTROL === */
.sidebar-panel-control {
    text-align: center;
    padding: 10px;
    border-radius: 12px;
    background: rgba(255, 130, 0, 0.15);
    color: #ffa94d !important;
    border: 1px solid rgba(255, 130, 0, 0.3);
    backdrop-filter: blur(6px);
    box-shadow: 0 0 10px rgba(0,0,0,0.3);
}

/* === ENCABEZADO PRINCIPAL === */
.header-container {
    text-align: center;
    padding: 40px 20px;
    border-radius: 20px;
    background: rgba(255, 255, 255, 0.06);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 130, 0, 0.3);
    box-shadow: 0 0 25px rgba(255, 130, 0, 0.2);
    margin-bottom: 25px;
}

/* Títulos */
.header-container h1 {
    font-size: 3em;
    margin: 0;
    color: #ffa94d;
    letter-spacing: 2px;
    text-shadow: 2px 2px 10px rgba(0,0,0,0.4);
}
.header-container h2, 
.header-container h3 {
    color: #f0f0f0;
    font-weight: 400;
    margin-top: 8px;
}

/* === SELECTBOX === */
div[data-baseweb="select"] {
    background-color: rgba(20,20,20,0.8) !important;
    color: #fff !important;
    border-radius: 8px;
    border: 1px solid rgba(255, 130, 0, 0.3);
}

/* === BOTONES === */
.stDownloadButton button, .stButton button {
    background: linear-gradient(135deg, #ff8800, #ff5e00);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 0.6em 1.2em;
    font-weight: 600;
    box-shadow: 0 2px 10px rgba(0,0,0,0.3);
    transition: all 0.2s ease-in-out;
}
.stDownloadButton button:hover, .stButton button:hover {
    background: linear-gradient(135deg, #ffa64d, #ff7a00);
    transform: scale(1.03);
}

/* === LEYENDA DEL MAPA === */
.block-container h3, .block-container h2, .block-container h4 {
    color: #f5f5f5;
}
            /* === Ajustes visuales del sidebar === */
.sidebar-logo {
    display: flex;
    align-items: center;
    justify-content: flex-start;
    margin-bottom: 20px;
}

.sidebar-logo img {
    width: 70px;
    height: 70px;
    margin-right: 10px;
}

.sidebar-logo h1 {
    color: #ff7b00;
    font-size: 1.8rem;
    font-weight: bold;
    margin: 0;
}
</style>

""", unsafe_allow_html=True)
# --- Configuración de la página
st.set_page_config(
    page_title="KUNTUR - Análisis y Predicción",
    page_icon="🦅", # Icono de Condor
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Encabezado principal
# Usamos un st.container para aplicar la clase CSS y los títulos


def main():
    # --- Configuración del Sidebar ---
    st.sidebar.markdown(f"""
        <div class="sidebar-logo">
            <img src="https://res.cloudinary.com/dttrc6k57/image/upload/v1761797590/kuntur_logo_dgmz25.png" alt="Logo KUNTUR">
            <h1>KUNTUR</h1>
        </div>
        <hr style="border: 1px solid rgba(255, 130, 0, 0.4); margin: 10px 0;">
        <h3 style="color: #ffc107; margin-bottom: 10px;">📂 Panel de análisis</h3>
        """, unsafe_allow_html=True)

    # --- Cargar los datos ---
    
    with st.spinner("🔄 Cargando datos de muertes viales..."):
        df = cargar_datos()

    # Si hubo error al cargar los datos, detener ejecución
    if df is None:
        st.error("❌ No se pudieron cargar los datos. Verifica que el archivo CSV esté en `data/MUERTES_VIALES.csv`.")
        return

    # --- Menú principal ---
    menu_items = {
        "🗺️ Mapa Interactivo": "mapa",
        "🔥 Mapa de Calor": "calor",
        "📊 Estadísticas por Provincia": "estadisticas",
        "📈 Análisis Comparativo": "comparativo",
        "🔍 Explorador de Datos": "explorador",
        "🛣️ Análisis por Tipo de Lugar": "tipo_lugar",
        "🚗 Vehículo de la Víctima": "victima",
        "🚙 Vehículo del Inculpado": "inculpado",
        "🚨 Modo de Producción del Hecho": "modo",
        "➕ Registrar nuevo incidente": "registro",
        "🔮 Módulo de Predicción": "prediccion"
    }

    opcion = st.sidebar.radio("Selecciona una opción:", list(menu_items.keys()))

    # --- Navegación entre opciones ---
    if opcion == "🗺️ Mapa Interactivo":
        st.markdown("### 📊 Leyenda del Mapa")
        col1, col2, col3, col4 = st.columns(4)
        with col1: st.markdown("🔴 **Rojo**: > 5,000 muertes")
        with col2: st.markdown("🟠 **Naranja**: 2,000 - 5,000 muertes")
        with col3: st.markdown("🟡 **Amarillo**: 500 - 2,000 muertes")
        with col4: st.markdown("🟢 **Verde**: < 500 muertes")

        st.markdown("---")
        st.markdown("### 🗺️ Mapa Interactivo de Argentina")
        st.markdown("**Haz clic en los círculos de colores para ver información detallada de cada provincia.**")

        mapa = crear_mapa_argentina_interactivo(df)
        st_folium(mapa, width=800, height=600)

    elif opcion == "🔥 Mapa de Calor":
        crear_mapa_de_calor(df)

    elif opcion == "📊 Estadísticas por Provincia":
        provincias = sorted(df['provincia_nombre'].unique())
        provincia_seleccionada = st.selectbox(
            "Selecciona una provincia para ver estadísticas detalladas:",
            provincias
        )
        mostrar_estadisticas_detalladas(df, provincia_seleccionada)

    elif opcion == "📈 Análisis Comparativo":
        mostrar_analisis_comparativo(df)

    elif opcion == "🔍 Explorador de Datos":
        col1, col2 = st.columns(2)

        with col1:
            anio_min = int(df['anio'].dropna().min())
            anio_max = int(df['anio'].dropna().max())
            anio_seleccionado = st.slider(
                "Año:",
                min_value=anio_min,
                max_value=anio_max,
                value=(anio_min, anio_max)
            )
        with col2:
            provincias_seleccionadas = st.multiselect(
                "Provincias:",
                options=sorted(df['provincia_nombre'].unique()),
                default=sorted(df['provincia_nombre'].unique())[:5]
            )

        df_filtrado = df[
            (df['anio'].between(anio_seleccionado[0], anio_seleccionado[1])) &
            (df['provincia_nombre'].isin(provincias_seleccionadas))
        ]

        st.markdown(f"#### 📊 Datos Filtrados: {len(df_filtrado):,} registros")
        st.dataframe(df_filtrado.head(100), use_container_width=True)

        # Botón de descarga
        csv = df_filtrado.to_csv(index=False)
        st.download_button(
            label="📥 Descargar datos filtrados (CSV)",
            data=csv,
            file_name=f"muertes_viales_filtrado_{anio_seleccionado[0]}_{anio_seleccionado[1]}.csv",
            mime="text/csv"
        )

    elif opcion == "🛣️ Análisis por Tipo de Lugar":
        crear_graficos_tipo_lugar(df)

    elif opcion == "🚗 Vehículo de la Víctima":
        crear_graficos_victima_vehiculo(df)

    elif opcion == "🚙 Vehículo del Inculpado":
        crear_graficos_inculpado_vehiculo(df)

    elif opcion == "🚨 Modo de Producción del Hecho":
        crear_graficos_modo_produccion_hecho(df)

    elif opcion == "➕ Registrar nuevo incidente":
        mostrar_formulario_registro()

    elif opcion == "🔮 Módulo de Predicción":
        mostrar_interfaz_prediccion(df)

if __name__ == "__main__":
    main()