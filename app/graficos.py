"""
Gráficos temáticos: tipo de lugar, vehículos (víctima/inculpado), modo de producción del hecho.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from folium.plugins import HeatMap

def crear_graficos_tipo_lugar(df: pd.DataFrame):
    """Crear gráficos de tipo de lugar por provincia y total Argentina"""
    st.markdown("### 🛣️ Análisis por Tipo de Lugar")

    df_limpio = df[df['tipo_lugar'].notna() & (df['tipo_lugar'] != '')].copy()

    if len(df_limpio) == 0:
        st.warning("No hay datos disponibles para tipo de lugar")
        return

    st.markdown("#### 📊 Total Argentina - Distribución por Tipo de Lugar")
    tipo_lugar_total = df_limpio['tipo_lugar'].value_counts().head(10)

    col1, col2 = st.columns(2)

    with col1:
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
        fig_torta = px.pie(
            values=tipo_lugar_total.values,
            names=tipo_lugar_total.index,
            title="Distribución por Tipo de Lugar - Total Argentina"
        )
        fig_torta.update_layout(height=500)
        st.plotly_chart(fig_torta, use_container_width=True)

    st.markdown("#### 🗺️ Distribución por Provincia")
    provincias = sorted(df_limpio['provincia_nombre'].unique())
    provincia_seleccionada = st.selectbox(
        "Selecciona una provincia para ver el análisis de tipo de lugar:",
        provincias
    )

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

def crear_graficos_victima_vehiculo(df: pd.DataFrame):
    """Crear gráficos de vehículo de la víctima por provincia y total Argentina"""
    st.markdown("### 🚗 Análisis por Vehículo de la Víctima")

    df_limpio = df[df['victima_vehiculo'].notna() & (df['victima_vehiculo'] != '')].copy()

    if len(df_limpio) == 0:
        st.warning("No hay datos disponibles para vehículo de la víctima")
        return

    st.markdown("#### 📊 Total Argentina - Distribución por Vehículo de la Víctima")
    victima_vehiculo_total = df_limpio['victima_vehiculo'].value_counts().head(10)

    col1, col2 = st.columns(2)

    with col1:
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
        fig_torta = px.pie(
            values=victima_vehiculo_total.values,
            names=victima_vehiculo_total.index,
            title="Distribución por Vehículo de la Víctima - Total Argentina"
        )
        fig_torta.update_layout(height=500)
        st.plotly_chart(fig_torta, use_container_width=True)

    st.markdown("#### 🗺️ Distribución por Provincia")
    provincias = sorted(df_limpio['provincia_nombre'].unique())
    provincia_seleccionada = st.selectbox(
        "Selecciona una provincia para ver el análisis de vehículo de la víctima:",
        provincias,
        key="victima_vehiculo_provincia"
    )

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

def crear_graficos_inculpado_vehiculo(df: pd.DataFrame):
    """Crear gráficos de vehículo del inculpado por provincia y total Argentina"""
    st.markdown("### 🚙 Análisis por Vehículo del Inculpado")

    df_limpio = df[df['inculpado_vehiculo'].notna() & (df['inculpado_vehiculo'] != '')].copy()

    if len(df_limpio) == 0:
        st.warning("No hay datos disponibles para vehículo del inculpado")
        return

    st.markdown("#### 📊 Total Argentina - Distribución por Vehículo del Inculpado")
    inculpado_vehiculo_total = df_limpio['inculpado_vehiculo'].value_counts().head(10)

    col1, col2 = st.columns(2)

    with col1:
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
        fig_torta = px.pie(
            values=inculpado_vehiculo_total.values,
            names=inculpado_vehiculo_total.index,
            title="Distribución por Vehículo del Inculpado - Total Argentina"
        )
        fig_torta.update_layout(height=500)
        st.plotly_chart(fig_torta, use_container_width=True)

    st.markdown("#### 🗺️ Distribución por Provincia")
    provincias = sorted(df_limpio['provincia_nombre'].unique())
    provincia_seleccionada = st.selectbox(
        "Selecciona una provincia para ver el análisis de vehículo del inculpado:",
        provincias,
        key="inculpado_vehiculo_provincia"
    )

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


def crear_graficos_modo_produccion_hecho(df: pd.DataFrame):
    """Crear gráficos de modo de producción del hecho con valores absolutos y porcentuales"""
    st.markdown("### 🚨 Análisis por Modo de Producción del Hecho")

    df_limpio = df[df['modo_produccion_hecho'].notna() & (df['modo_produccion_hecho'] != '')].copy()

    if len(df_limpio) == 0:
        st.warning("No hay datos disponibles para modo de producción del hecho")
        return

    st.markdown("#### 🗺️ Filtro por Provincia")
    provincias = ['Todas las Provincias'] + sorted(df_limpio['provincia_nombre'].unique())
    provincia_seleccionada = st.selectbox(
        "Selecciona una provincia para filtrar los datos (o 'Todas las Provincias' para el total):",
        provincias,
        key="modo_produccion_provincia"
    )

    if provincia_seleccionada == 'Todas las Provincias':
        df_filtrado = df_limpio
        titulo_analisis = "Total Argentina"
    else:
        df_filtrado = df_limpio[df_limpio['provincia_nombre'] == provincia_seleccionada]
        titulo_analisis = provincia_seleccionada

    modo_produccion_counts = df_filtrado['modo_produccion_hecho'].value_counts()
    total_casos = len(df_filtrado)

    df_stats = pd.DataFrame({
        'Modo de Producción': modo_produccion_counts.index,
        'Cantidad': modo_produccion_counts.values,
        'Porcentaje': (modo_produccion_counts.values / total_casos * 100).round(2)
    })

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

    st.markdown("#### 📊 Visualización de Datos")

    col1, col2 = st.columns(2)

    with col1:
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

    st.markdown("#### 📋 Tabla Detallada")

    df_stats['Porcentaje_Formateado'] = df_stats['Porcentaje'].apply(lambda x: f"{x:.2f}%")
    df_stats['Cantidad_Formateada'] = df_stats['Cantidad'].apply(lambda x: f"{x:,}")

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

    csv = df_stats.to_csv(index=False)
    st.download_button(
        label="📥 Descargar datos de modo de producción (CSV)",
        data=csv,
        file_name=f"modo_produccion_hecho_{provincia_seleccionada.replace(' ', '_')}.csv",
        mime="text/csv"
    )

