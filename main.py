"""
Punto de entrada de la app Streamlit.
"""

import streamlit as st
import sys, os
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

st.markdown("""
<style>
    div[data-baseweb="select"] li {
        white-space: normal !important;
        overflow: visible !important;
        text-overflow: unset !important;
    }
</style>
""", unsafe_allow_html=True)

# Configuración de la página
st.set_page_config(
    page_title="S.A.S.V",
    page_icon="🇦🇷",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Encabezado principal
st.markdown("""
<div style="text-align: center; padding: 20px; background: linear-gradient(90deg, #1f77b4, #ff7f0e); border-radius: 10px; margin-bottom: 20px;">
    <h1 style="color: white; margin: 0;">Sistema de Análisis de Siniestros Viales</h1>
    <h2 style="color: #FFD700; margin: 10px 0 0 0; font-size: 1.5em;">Análisis de Muertes Viales por Provincia</h2>
</div>
""", unsafe_allow_html=True)


def main():
    # Sidebar
    st.sidebar.markdown("""
    <div style="text-align: center; padding: 10px; background: linear-gradient(90deg, #1f77b4, #ff7f0e); border-radius: 5px; margin-bottom: 20px;">
        <h3 style="color: white; margin: 0;">🎛️ Panel de Control</h3>
    </div>
    """, unsafe_allow_html=True)

    # Cargar datos
    with st.spinner("🔄 Cargando datos de muertes viales..."):
        df = cargar_datos() # lee data/MUERTES_VIALES.csv por defecto

    if df is None:
        st.error("❌ No se pudieron cargar los datos. Verifica que el archivo CSV esté en 'data/MUERTES_VIALES.csv'.")
        return

    st.sidebar.success(f"✅ Datos cargados: {len(df):,} registros")

    # --- INICIO DE MODIFICACIÓN: st.sidebar.selectbox cambiado a st.sidebar.radio ---
    
    # Menú principal - Usando Radio buttons para mostrar todas las opciones a la vista
    opcion = st.sidebar.selectbox(
        "Selecciona una opción de análisis:",
        [
            "🗺️ Mapa Interactivo",          
            "📊 Estadísticas por Provincia",
            "🔥 Mapa de Calor",
            "📈 Análisis Comparativo",
            "🔍 Explorador de Datos",
            "🛣️ Análisis por Tipo de Lugar",
            "🚗 Análisis por Vehículo de la Víctima",
            "🚙 Análisis por Vehículo del Inculpado",
            "🚨 Análisis por Modo de Producción del Hecho",
            "➕ Registrar nuevo incidente",
            "🔮 Módulo de Predicción"
        ]
    )
    
    # --- FIN DE MODIFICACIÓN ---

    # Navegación entre opciones
    if opcion == "🗺️ Mapa Interactivo":
        st.markdown("### 🗺️ Mapa Interactivo de Argentina")
        st.markdown("**Haz clic en los círculos de colores para ver información detallada de cada provincia.**")
        mapa = crear_mapa_argentina_interactivo(df)
        st_folium(mapa, width=800, height=600)

        # Leyenda
        st.markdown("---")
        st.markdown("### 📊 Leyenda del Mapa")
        col1, col2, col3, col4 = st.columns(4)
        with col1: st.markdown("🔴 **Rojo**: > 5,000 muertes")
        with col2: st.markdown("🟠 **Naranja**: 2,000 - 5,000 muertes")
        with col3: st.markdown("🟡 **Amarillo**: 500 - 2,000 muertes")
        with col4: st.markdown("🟢 **Verde**: < 500 muertes")

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

        # Filtros
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

        # Botón para exportar
        csv = df_filtrado.to_csv(index=False)
        st.download_button(
            label="📥 Descargar datos filtrados (CSV)",
            data=csv,
            file_name=f"muertes_viales_filtrado_{anio_seleccionado[0]}_{anio_seleccionado[1]}.csv",
            mime="text/csv"
        )

    elif opcion == "🛣️ Análisis por Tipo de Lugar":
        crear_graficos_tipo_lugar(df)

    elif opcion == "🚗 Análisis por Vehículo de la Víctima":
        crear_graficos_victima_vehiculo(df)

    elif opcion == "🚙 Análisis por Vehículo del Inculpado":
        crear_graficos_inculpado_vehiculo(df)

    elif opcion == "🚨 Análisis por Modo de Producción del Hecho":
        crear_graficos_modo_produccion_hecho(df)
    elif opcion == "➕ Registrar nuevo incidente":
        
        mostrar_formulario_registro()
    elif opcion == "🔮 Módulo de Predicción":
        
        mostrar_interfaz_prediccion(df)

if __name__ == "__main__":
    main()
