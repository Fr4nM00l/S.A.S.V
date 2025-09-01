#!/usr/bin/env python3
"""
Mapa Interactivo de Argentina - Análisis de Muertes Viales
Aplicación web que se inicia automáticamente sin prompts
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import folium
from streamlit_folium import st_folium
import warnings
warnings.filterwarnings('ignore')

# Configuración de la página
st.set_page_config(
    page_title="S.A.S.V",
    page_icon="🇦🇷",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título principal con diseño mejorado
st.markdown("""
<div style="text-align: center; padding: 20px; background: linear-gradient(90deg, #1f77b4, #ff7f0e); border-radius: 10px; margin-bottom: 20px;">
    <h1 style="color: white; margin: 0;">🇦🇷 Sistema de Análisis de Siniestros Viales</h1>
    <h2 style="color: white; margin: 10px 0 0 0; font-size: 1.5em;">Análisis de Muertes Viales por Provincia</h2>
</div>
""", unsafe_allow_html=True)

@st.cache_data
def cargar_datos():
    """Cargar y procesar los datos"""
    try:
        # Cargar datos
        df = pd.read_csv(
            "MUERTES_VIALES.csv",
            sep=";",
            encoding="utf-8",
            low_memory=False
        )
        
        # Función para limpiar edades (tomada de Aprendiendo6.py)
        def limpiar_edad(valor):
            if isinstance(valor, str):
                valor = valor.strip().lower()

                # Rango X-Y
                if "-" in valor:
                    try:
                        partes = valor.split("-")
                        return (float(partes[0]) + float(partes[1])) / 2
                    except:
                        return np.nan

                # Menos de N
                if "menos de" in valor:
                    try:
                        num = float(valor.replace("menos de", "").strip())
                        return num / 2
                    except:
                        return np.nan

                # Número directo
                if valor.isdigit():
                    return float(valor)

                return np.nan

            if isinstance(valor, (int, float)):
                return float(valor)

            return np.nan
        
        # Limpiar datos básicos - mantener todos los registros
        df = df[df['provincia_nombre'] != 'Desconocido']
        df = df[df['provincia_nombre'].notna()]
        
        # Convertir coordenadas a numérico
        df['latitud'] = pd.to_numeric(df['latitud'], errors='coerce')
        df['longitud'] = pd.to_numeric(df['longitud'], errors='coerce')
        
        # Limpiar edades usando la función correcta
        df['victima_tr_edad'] = df['victima_tr_edad'].apply(limpiar_edad)
        
        # Convertir año a numérico
        df['anio'] = pd.to_numeric(df['anio'], errors='coerce')
        
        # Convertir mes a numérico
        df['mes'] = pd.to_numeric(df['mes'], errors='coerce')
        
        return df
    except Exception as e:
        st.error(f"Error al cargar datos: {str(e)}")
        return None

def crear_mapa_argentina_interactivo(df):
    """Crear mapa interactivo de Argentina con límites de provincias"""
    
    # Calcular estadísticas por provincia usando datos ya procesados
    stats_provincia = df.groupby('provincia_nombre').agg({
        'id_hecho': 'count',
        'victima_tr_edad': lambda x: x.dropna().mean() if len(x.dropna()) > 0 else 0,
        'anio': lambda x: x.dropna().min() if len(x.dropna()) > 0 else 0
    }).round(2)
    
    # Agregar año máximo por separado
    stats_max = df.groupby('provincia_nombre')['anio'].agg(
        lambda x: x.dropna().max() if len(x.dropna()) > 0 else 0
    ).round(2)
    
    stats_provincia['anio_max'] = stats_max
    stats_provincia.columns = ['total_muertes', 'edad_promedio', 'anio_min', 'anio_max']
    stats_provincia = stats_provincia.reset_index()
    
    # Coordenadas centrales de las provincias argentinas (más precisas)
    coordenadas_provincias = {
        'Buenos Aires': [-36.6769, -60.5586],
        'Córdoba': [-31.4201, -64.1888],
        'Santa Fe': [-31.5855, -60.7238],
        'Mendoza': [-32.8908, -68.8272],
        'Tucumán': [-26.8083, -65.2176],
        'Salta': [-24.7829, -65.4232],
        'Entre Ríos': [-32.0588, -60.6617],
        'Chaco': [-27.4512, -58.9866],
        'Corrientes': [-27.4692, -58.8306],
        'Santiago del Estero': [-27.7951, -64.2615],
        'Misiones': [-27.3621, -55.9009],
        'San Juan': [-31.5375, -68.5364],
        'Jujuy': [-24.1858, -65.2995],
        'Río Negro': [-40.8135, -63.0025],
        'Neuquén': [-38.9516, -68.0591],
        'Chubut': [-43.3002, -65.1023],
        'Formosa': [-26.1775, -58.1781],
        'San Luis': [-33.3017, -66.3378],
        'Catamarca': [-28.4696, -65.7852],
        'La Rioja': [-29.4133, -66.8563],
        'La Pampa': [-36.6200, -64.2900],
        'Santa Cruz': [-48.8233, -69.2285],
        'Tierra del Fuego': [-54.8019, -68.3030]
    }
    
    # Crear mapa base centrado en Argentina
    mapa = folium.Map(
        location=[-36.6769, -60.5586],  # Centro de Argentina
        zoom_start=5,
        tiles='OpenStreetMap',
        control_scale=True
    )
    
    # Agregar marcadores interactivos por provincia
    for _, row in stats_provincia.iterrows():
        provincia = row['provincia_nombre']
        if provincia in coordenadas_provincias:
            lat, lon = coordenadas_provincias[provincia]
            
            # Color según cantidad de muertes
            total_muertes = row['total_muertes']
            if total_muertes > 5000:
                color = 'red'
                size = 15
            elif total_muertes > 2000:
                color = 'orange'
                size = 12
            elif total_muertes > 500:
                color = 'yellow'
                size = 10
            else:
                color = 'green'
                size = 8
            
            # Popup con información detallada
            popup_text = f"""
            <div style="width: 250px;">
                <h3 style="color: {color}; margin-bottom: 10px;">{provincia}</h3>
                <table style="width: 100%; border-collapse: collapse;">
                    <tr><td><strong>Total Muertes:</strong></td><td>{total_muertes:,.0f}</td></tr>
                    <tr><td><strong>Edad Promedio:</strong></td><td>{row['edad_promedio']:.1f} años</td></tr>
                    <tr><td><strong>Período:</strong></td><td>{row['anio_min']:.0f}-{row['anio_max']:.0f}</td></tr>
                    <tr><td><strong>Promedio/año:</strong></td><td>{total_muertes/(row['anio_max']-row['anio_min']+1):.0f}</td></tr>
                </table>
                <p style="margin-top: 10px; font-size: 12px; color: #666;">
                    Haz clic para ver estadísticas detalladas
                </p>
            </div>
            """
            
            # Crear marcador con círculo para mejor visibilidad
            folium.CircleMarker(
                location=[lat, lon],
                radius=size,
                popup=folium.Popup(popup_text, max_width=300),
                tooltip=f"<b>{provincia}</b><br>{total_muertes:,.0f} muertes",
                color=color,
                fill=True,
                fillColor=color,
                fillOpacity=0.7,
                weight=2
            ).add_to(mapa)
            
            # Agregar etiqueta con el nombre de la provincia
            folium.Tooltip(
                f"{provincia}<br>{total_muertes:,.0f} muertes",
                permanent=False
            ).add_to(folium.CircleMarker(
                location=[lat, lon],
                radius=1,
                color='transparent',
                fill=False
            ).add_to(mapa))
    
    return mapa

def mostrar_estadisticas_detalladas(df, provincia_seleccionada):
    """Mostrar estadísticas detalladas de una provincia"""
    
    # Filtrar datos de la provincia
    df_provincia = df[df['provincia_nombre'] == provincia_seleccionada].copy()
    
    if len(df_provincia) == 0:
        st.warning("No hay datos disponibles para esta provincia")
        return
    
    # Métricas principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="🚗 Total Muertes",
            value=f"{len(df_provincia):,}",
            delta=None
        )
    
    with col2:
        edad_prom = df_provincia['victima_tr_edad'].dropna().mean()
        if pd.isna(edad_prom):
            edad_prom = 0
        st.metric(
            label="👥 Edad Promedio",
            value=f"{edad_prom:.1f} años",
            delta=None
        )
    
    with col3:
        anio_min = df_provincia['anio'].dropna().min()
        anio_max = df_provincia['anio'].dropna().max()
        if pd.isna(anio_min) or pd.isna(anio_max):
            anio_min = anio_max = 0
        st.metric(
            label="📅 Período",
            value=f"{anio_min:.0f}-{anio_max:.0f}",
            delta=None
        )
    
    with col4:
        if anio_max > anio_min:
            muertes_por_anio = len(df_provincia) / (anio_max - anio_min + 1)
        else:
            muertes_por_anio = len(df_provincia)
        st.metric(
            label="📊 Promedio por Año",
            value=f"{muertes_por_anio:.0f}",
            delta=None
        )
    
    st.markdown("---")
    
    # Gráficos detallados
    col1, col2 = st.columns(2)
    
    with col1:
        # Evolución temporal
        evolucion = df_provincia.groupby('anio').size().reset_index(name='muertes')
        fig_tiempo = px.line(
            evolucion,
            x='anio',
            y='muertes',
            title=f"📈 Evolución de Muertes Viales en {provincia_seleccionada}",
            labels={'anio': 'Año', 'muertes': 'Número de Muertes'},
            markers=True
        )
        fig_tiempo.update_layout(height=400, showlegend=False)
        fig_tiempo.update_traces(line_color='#1f77b4', line_width=3)
        st.plotly_chart(fig_tiempo, use_container_width=True)
    
    with col2:
        # Distribución por mes
        meses = df_provincia.groupby('mes').size().reset_index(name='muertes')
        meses['mes_nombre'] = meses['mes'].map({
            1: 'Ene', 2: 'Feb', 3: 'Mar', 4: 'Abr', 5: 'May', 6: 'Jun',
            7: 'Jul', 8: 'Ago', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dic'
        })
        
        fig_mes = px.bar(
            meses,
            x='mes_nombre',
            y='muertes',
            title=f"📅 Distribución por Mes - {provincia_seleccionada}",
            labels={'mes_nombre': 'Mes', 'muertes': 'Número de Muertes'}
        )
        fig_mes.update_layout(height=400, showlegend=False)
        fig_mes.update_traces(marker_color='#ff7f0e')
        st.plotly_chart(fig_mes, use_container_width=True)
    
    # Top localidades
    st.subheader(f"🏘️ Top 10 Localidades con Más Muertes - {provincia_seleccionada}")
    top_localidades = df_provincia['localidad_nombre'].value_counts().head(10)
    
    fig_localidades = px.bar(
        x=top_localidades.values,
        y=top_localidades.index,
        orientation='h',
        title="Localidades con Mayor Número de Muertes Viales",
        labels={'x': 'Número de Muertes', 'y': 'Localidad'}
    )
    fig_localidades.update_layout(height=500, showlegend=False)
    fig_localidades.update_traces(marker_color='#2ca02c')
    st.plotly_chart(fig_localidades, use_container_width=True)

def mostrar_analisis_comparativo(df):
    """Mostrar análisis comparativo entre provincias"""
    
    # Estadísticas por provincia usando datos ya procesados
    stats_comparativo = df.groupby('provincia_nombre').agg({
        'id_hecho': 'count',
        'victima_tr_edad': lambda x: x.dropna().mean() if len(x.dropna()) > 0 else 0,
        'anio': lambda x: x.dropna().nunique() if len(x.dropna()) > 0 else 0
    }).round(2)
    
    stats_comparativo.columns = ['Total Muertes', 'Edad Promedio', 'Años con Datos']
    stats_comparativo = stats_comparativo.sort_values('Total Muertes', ascending=False)
    
    # Gráfico de barras
    fig_comparativo = px.bar(
        stats_comparativo.reset_index(),
        x='provincia_nombre',
        y='Total Muertes',
        title="📊 Total de Muertes Viales por Provincia",
        labels={'provincia_nombre': 'Provincia', 'Total Muertes': 'Número de Muertes'},
        color='Total Muertes',
        color_continuous_scale='Reds'
    )
    fig_comparativo.update_xaxes(tickangle=45)
    fig_comparativo.update_layout(height=500, showlegend=False)
    st.plotly_chart(fig_comparativo, use_container_width=True)
    
    # Tabla de estadísticas
    st.subheader("📋 Tabla de Estadísticas por Provincia")
    st.dataframe(stats_comparativo, use_container_width=True)

def crear_graficos_tipo_lugar(df):
    """Crear gráficos de tipo de lugar por provincia y total Argentina"""
    
    st.markdown("### 🛣️ Análisis por Tipo de Lugar")
    
    # Limpiar datos de tipo_lugar
    df_limpio = df[df['tipo_lugar'].notna() & (df['tipo_lugar'] != '')].copy()
    
    if len(df_limpio) == 0:
        st.warning("No hay datos disponibles para tipo de lugar")
        return
    
    # Gráfico total Argentina
    st.markdown("#### 📊 Total Argentina - Distribución por Tipo de Lugar")
    
    tipo_lugar_total = df_limpio['tipo_lugar'].value_counts().head(10)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de barras
        fig_barras = px.bar(
            x=tipo_lugar_total.values,
            y=tipo_lugar_total.index,
            orientation='h',
            title="Top 10 Tipos de Lugar - Total Argentina",
            labels={'x': 'Número de Muertes', 'y': 'Tipo de Lugar'},
            color=tipo_lugar_total.values,
            color_continuous_scale='Reds'
        )
        fig_barras.update_layout(height=500, showlegend=False)
        st.plotly_chart(fig_barras, use_container_width=True)
    
    with col2:
        # Gráfico de torta
        fig_torta = px.pie(
            values=tipo_lugar_total.values,
            names=tipo_lugar_total.index,
            title="Distribución por Tipo de Lugar - Total Argentina"
        )
        fig_torta.update_layout(height=500)
        st.plotly_chart(fig_torta, use_container_width=True)
    
    # Gráfico por provincia
    st.markdown("#### 🗺️ Distribución por Provincia")
    
    # Selector de provincia
    provincias = sorted(df_limpio['provincia_nombre'].unique())
    provincia_seleccionada = st.selectbox(
        "Selecciona una provincia para ver el análisis de tipo de lugar:",
        provincias
    )
    
    # Datos de la provincia seleccionada
    df_provincia = df_limpio[df_limpio['provincia_nombre'] == provincia_seleccionada]
    tipo_lugar_provincia = df_provincia['tipo_lugar'].value_counts().head(10)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_prov_barras = px.bar(
            x=tipo_lugar_provincia.values,
            y=tipo_lugar_provincia.index,
            orientation='h',
            title=f"Top 10 Tipos de Lugar - {provincia_seleccionada}",
            labels={'x': 'Número de Muertes', 'y': 'Tipo de Lugar'},
            color=tipo_lugar_provincia.values,
            color_continuous_scale='Blues'
        )
        fig_prov_barras.update_layout(height=500, showlegend=False)
        st.plotly_chart(fig_prov_barras, use_container_width=True)
    
    with col2:
        fig_prov_torta = px.pie(
            values=tipo_lugar_provincia.values,
            names=tipo_lugar_provincia.index,
            title=f"Distribución por Tipo de Lugar - {provincia_seleccionada}"
        )
        fig_prov_torta.update_layout(height=500)
        st.plotly_chart(fig_prov_torta, use_container_width=True)

def crear_graficos_victima_vehiculo(df):
    """Crear gráficos de vehículo de la víctima por provincia y total Argentina"""
    
    st.markdown("### 🚗 Análisis por Vehículo de la Víctima")
    
    # Limpiar datos de victima_vehiculo
    df_limpio = df[df['victima_vehiculo'].notna() & (df['victima_vehiculo'] != '')].copy()
    
    if len(df_limpio) == 0:
        st.warning("No hay datos disponibles para vehículo de la víctima")
        return
    
    # Gráfico total Argentina
    st.markdown("#### 📊 Total Argentina - Distribución por Vehículo de la Víctima")
    
    victima_vehiculo_total = df_limpio['victima_vehiculo'].value_counts().head(10)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de barras
        fig_barras = px.bar(
            x=victima_vehiculo_total.values,
            y=victima_vehiculo_total.index,
            orientation='h',
            title="Top 10 Vehículos de Víctimas - Total Argentina",
            labels={'x': 'Número de Muertes', 'y': 'Tipo de Vehículo'},
            color=victima_vehiculo_total.values,
            color_continuous_scale='Greens'
        )
        fig_barras.update_layout(height=500, showlegend=False)
        st.plotly_chart(fig_barras, use_container_width=True)
    
    with col2:
        # Gráfico de torta
        fig_torta = px.pie(
            values=victima_vehiculo_total.values,
            names=victima_vehiculo_total.index,
            title="Distribución por Vehículo de la Víctima - Total Argentina"
        )
        fig_torta.update_layout(height=500)
        st.plotly_chart(fig_torta, use_container_width=True)
    
    # Gráfico por provincia
    st.markdown("#### 🗺️ Distribución por Provincia")
    
    # Selector de provincia
    provincias = sorted(df_limpio['provincia_nombre'].unique())
    provincia_seleccionada = st.selectbox(
        "Selecciona una provincia para ver el análisis de vehículo de la víctima:",
        provincias,
        key="victima_vehiculo_provincia"
    )
    
    # Datos de la provincia seleccionada
    df_provincia = df_limpio[df_limpio['provincia_nombre'] == provincia_seleccionada]
    victima_vehiculo_provincia = df_provincia['victima_vehiculo'].value_counts().head(10)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_prov_barras = px.bar(
            x=victima_vehiculo_provincia.values,
            y=victima_vehiculo_provincia.index,
            orientation='h',
            title=f"Top 10 Vehículos de Víctimas - {provincia_seleccionada}",
            labels={'x': 'Número de Muertes', 'y': 'Tipo de Vehículo'},
            color=victima_vehiculo_provincia.values,
            color_continuous_scale='Purples'
        )
        fig_prov_barras.update_layout(height=500, showlegend=False)
        st.plotly_chart(fig_prov_barras, use_container_width=True)
    
    with col2:
        fig_prov_torta = px.pie(
            values=victima_vehiculo_provincia.values,
            names=victima_vehiculo_provincia.index,
            title=f"Distribución por Vehículo de la Víctima - {provincia_seleccionada}"
        )
        fig_prov_torta.update_layout(height=500)
        st.plotly_chart(fig_prov_torta, use_container_width=True)

def crear_graficos_inculpado_vehiculo(df):
    """Crear gráficos de vehículo del inculpado por provincia y total Argentina"""
    
    st.markdown("### 🚙 Análisis por Vehículo del Inculpado")
    
    # Limpiar datos de inculpado_vehiculo
    df_limpio = df[df['inculpado_vehiculo'].notna() & (df['inculpado_vehiculo'] != '')].copy()
    
    if len(df_limpio) == 0:
        st.warning("No hay datos disponibles para vehículo del inculpado")
        return
    
    # Gráfico total Argentina
    st.markdown("#### 📊 Total Argentina - Distribución por Vehículo del Inculpado")
    
    inculpado_vehiculo_total = df_limpio['inculpado_vehiculo'].value_counts().head(10)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de barras
        fig_barras = px.bar(
            x=inculpado_vehiculo_total.values,
            y=inculpado_vehiculo_total.index,
            orientation='h',
            title="Top 10 Vehículos de Inculpados - Total Argentina",
            labels={'x': 'Número de Casos', 'y': 'Tipo de Vehículo'},
            color=inculpado_vehiculo_total.values,
            color_continuous_scale='Oranges'
        )
        fig_barras.update_layout(height=500, showlegend=False)
        st.plotly_chart(fig_barras, use_container_width=True)
    
    with col2:
        # Gráfico de torta
        fig_torta = px.pie(
            values=inculpado_vehiculo_total.values,
            names=inculpado_vehiculo_total.index,
            title="Distribución por Vehículo del Inculpado - Total Argentina"
        )
        fig_torta.update_layout(height=500)
        st.plotly_chart(fig_torta, use_container_width=True)
    
    # Gráfico por provincia
    st.markdown("#### 🗺️ Distribución por Provincia")
    
    # Selector de provincia
    provincias = sorted(df_limpio['provincia_nombre'].unique())
    provincia_seleccionada = st.selectbox(
        "Selecciona una provincia para ver el análisis de vehículo del inculpado:",
        provincias,
        key="inculpado_vehiculo_provincia"
    )
    
    # Datos de la provincia seleccionada
    df_provincia = df_limpio[df_limpio['provincia_nombre'] == provincia_seleccionada]
    inculpado_vehiculo_provincia = df_provincia['inculpado_vehiculo'].value_counts().head(10)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_prov_barras = px.bar(
            x=inculpado_vehiculo_provincia.values,
            y=inculpado_vehiculo_provincia.index,
            orientation='h',
            title=f"Top 10 Vehículos de Inculpados - {provincia_seleccionada}",
            labels={'x': 'Número de Casos', 'y': 'Tipo de Vehículo'},
            color=inculpado_vehiculo_provincia.values,
            color_continuous_scale='Reds'
        )
        fig_prov_barras.update_layout(height=500, showlegend=False)
        st.plotly_chart(fig_prov_barras, use_container_width=True)
    
    with col2:
        fig_prov_torta = px.pie(
            values=inculpado_vehiculo_provincia.values,
            names=inculpado_vehiculo_provincia.index,
            title=f"Distribución por Vehículo del Inculpado - {provincia_seleccionada}"
        )
        fig_prov_torta.update_layout(height=500)
        st.plotly_chart(fig_prov_torta, use_container_width=True)

def crear_graficos_modo_produccion_hecho(df):
    """Crear gráficos de modo de producción del hecho con valores absolutos y porcentuales"""
    
    st.markdown("### 🚨 Análisis por Modo de Producción del Hecho")
    
    # Limpiar datos de modo_produccion_hecho
    df_limpio = df[df['modo_produccion_hecho'].notna() & (df['modo_produccion_hecho'] != '')].copy()
    
    if len(df_limpio) == 0:
        st.warning("No hay datos disponibles para modo de producción del hecho")
        return
    
    # Selector de provincia
    st.markdown("#### 🗺️ Filtro por Provincia")
    provincias = ['Todas las Provincias'] + sorted(df_limpio['provincia_nombre'].unique())
    provincia_seleccionada = st.selectbox(
        "Selecciona una provincia para filtrar los datos (o 'Todas las Provincias' para el total):",
        provincias,
        key="modo_produccion_provincia"
    )
    
    # Filtrar datos según la selección
    if provincia_seleccionada == 'Todas las Provincias':
        df_filtrado = df_limpio
        titulo_analisis = "Total Argentina"
    else:
        df_filtrado = df_limpio[df_limpio['provincia_nombre'] == provincia_seleccionada]
        titulo_analisis = provincia_seleccionada
    
    # Calcular estadísticas
    modo_produccion_counts = df_filtrado['modo_produccion_hecho'].value_counts()
    total_casos = len(df_filtrado)
    
    # Crear DataFrame con valores absolutos y porcentuales
    df_stats = pd.DataFrame({
        'Modo de Producción': modo_produccion_counts.index,
        'Cantidad': modo_produccion_counts.values,
        'Porcentaje': (modo_produccion_counts.values / total_casos * 100).round(2)
    })
    
    # Mostrar métricas principales
    st.markdown(f"#### 📊 Estadísticas - {titulo_analisis}")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="📈 Total de Casos",
            value=f"{total_casos:,}",
            delta=None
        )
    
    with col2:
        modo_mas_frecuente = df_stats.iloc[0]
        st.metric(
            label="🔥 Modo Más Frecuente",
            value=modo_mas_frecuente['Modo de Producción'],
            delta=f"{modo_mas_frecuente['Porcentaje']:.1f}%"
        )
    
    with col3:
        st.metric(
            label="📋 Tipos Diferentes",
            value=f"{len(df_stats)}",
            delta=None
        )
    
    # Gráficos
    st.markdown("#### 📊 Visualización de Datos")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de barras con valores absolutos
        fig_barras = px.bar(
            df_stats.head(10),
            x='Cantidad',
            y='Modo de Producción',
            orientation='h',
            title=f"Top 10 Modos de Producción - {titulo_analisis} (Valores Absolutos)",
            labels={'Cantidad': 'Número de Casos', 'Modo de Producción': 'Tipo de Hecho'},
            color='Cantidad',
            color_continuous_scale='Reds'
        )
        fig_barras.update_layout(height=500, showlegend=False)
        st.plotly_chart(fig_barras, use_container_width=True)
    
    with col2:
        # Gráfico de torta con porcentajes
        fig_torta = px.pie(
            df_stats.head(10),
            values='Porcentaje',
            names='Modo de Producción',
            title=f"Distribución por Modo de Producción - {titulo_analisis} (Porcentajes)",
            hover_data=['Cantidad']
        )
        fig_torta.update_layout(height=500)
        fig_torta.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_torta, use_container_width=True)
    
    # Gráfico de barras con porcentajes
    st.markdown("#### 📈 Comparación de Porcentajes")
    
    fig_porcentajes = px.bar(
        df_stats.head(15),
        x='Modo de Producción',
        y='Porcentaje',
        title=f"Porcentaje de Modos de Producción - {titulo_analisis}",
        labels={'Porcentaje': 'Porcentaje (%)', 'Modo de Producción': 'Tipo de Hecho'},
        color='Porcentaje',
        color_continuous_scale='Blues'
    )
    fig_porcentajes.update_xaxes(tickangle=45)
    fig_porcentajes.update_layout(height=500, showlegend=False)
    st.plotly_chart(fig_porcentajes, use_container_width=True)
    
    # Tabla detallada
    st.markdown("#### 📋 Tabla Detallada")
    
    # Agregar columna con formato mejorado
    df_stats['Porcentaje_Formateado'] = df_stats['Porcentaje'].apply(lambda x: f"{x:.2f}%")
    df_stats['Cantidad_Formateada'] = df_stats['Cantidad'].apply(lambda x: f"{x:,}")
    
    # Mostrar tabla con columnas formateadas
    st.dataframe(
        df_stats[['Modo de Producción', 'Cantidad_Formateada', 'Porcentaje_Formateado']].rename(
            columns={
                'Modo de Producción': 'Tipo de Hecho',
                'Cantidad_Formateada': 'Cantidad',
                'Porcentaje_Formateado': 'Porcentaje'
            }
        ),
        use_container_width=True,
        hide_index=True
    )
    
    # Descargar datos
    csv = df_stats.to_csv(index=False)
    st.download_button(
        label="📥 Descargar datos de modo de producción (CSV)",
        data=csv,
        file_name=f"modo_produccion_hecho_{provincia_seleccionada.replace(' ', '_')}.csv",
        mime="text/csv"
    )

def main():
    """Función principal de la aplicación"""
    
    # Sidebar con diseño mejorado
    st.sidebar.markdown("""
    <div style="text-align: center; padding: 10px; background: linear-gradient(90deg, #1f77b4, #ff7f0e); border-radius: 5px; margin-bottom: 20px;">
        <h3 style="color: white; margin: 0;">🎛️ Panel de Control</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Cargar datos
    with st.spinner("🔄 Cargando datos de muertes viales..."):
        df = cargar_datos()
    
    if df is None:
        st.error("❌ No se pudieron cargar los datos. Verifica que el archivo CSV esté en la ubicación correcta.")
        return
    
    st.sidebar.success(f"✅ Datos cargados: {len(df):,} registros")
    
    # Opciones en el sidebar
    opcion = st.sidebar.selectbox(
        "Selecciona una opción:",
        ["🗺️ Mapa Interactivo", "📊 Estadísticas por Provincia", "📈 Análisis Comparativo", "🔍 Explorador de Datos",
         "🛣️ Análisis por Tipo de Lugar", "🚗 Análisis por Vehículo de la Víctima", "🚙 Análisis por Vehículo del Inculpado",
         "🚨 Análisis por Modo de Producción del Hecho"]
    )
    
    if opcion == "🗺️ Mapa Interactivo":
        st.markdown("### 🗺️ Mapa Interactivo de Argentina")
        st.markdown("**Haz clic en los círculos de colores para ver información detallada de cada provincia**")
        
        # Crear y mostrar mapa
        mapa = crear_mapa_argentina_interactivo(df)
        st_folium(mapa, width=800, height=600)
        
        # Leyenda mejorada
        st.markdown("---")
        st.markdown("### 📊 Leyenda del Mapa")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown("🔴 **Rojo**: > 5,000 muertes")
        with col2:
            st.markdown("🟠 **Naranja**: 2,000 - 5,000 muertes")
        with col3:
            st.markdown("🟡 **Amarillo**: 500 - 2,000 muertes")
        with col4:
            st.markdown("🟢 **Verde**: < 500 muertes")
    
    elif opcion == "📊 Estadísticas por Provincia":
        st.markdown("### 📊 Estadísticas por Provincia")
        
        # Selector de provincia
        provincias = sorted(df['provincia_nombre'].unique())
        provincia_seleccionada = st.selectbox(
            "Selecciona una provincia para ver estadísticas detalladas:",
            provincias
        )
        
        mostrar_estadisticas_detalladas(df, provincia_seleccionada)
    
    elif opcion == "📈 Análisis Comparativo":
        st.markdown("### 📈 Análisis Comparativo entre Provincias")
        mostrar_analisis_comparativo(df)
    
    elif opcion == "🔍 Explorador de Datos":
        st.markdown("### 🔍 Explorador de Datos")
        
        # Filtros
        st.markdown("#### 🔧 Filtros de Búsqueda")
        
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
        
        # Aplicar filtros
        df_filtrado = df[
            (df['anio'].between(anio_seleccionado[0], anio_seleccionado[1])) &
            (df['provincia_nombre'].isin(provincias_seleccionadas))
        ]
        
        st.markdown(f"#### 📊 Datos Filtrados: {len(df_filtrado):,} registros")
        
        # Mostrar datos
        st.dataframe(df_filtrado.head(100), use_container_width=True)
        
        # Descargar datos filtrados
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

if __name__ == "__main__":
    main()
