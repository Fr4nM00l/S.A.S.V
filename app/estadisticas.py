"""
Funciones para mostrar estadísticas detalladas por provincia.
"""

import streamlit as st
import pandas as pd
import plotly.express as px

def mostrar_estadisticas_detalladas(df: pd.DataFrame, provincia_seleccionada: str):
    """
    Calcula y muestra métricas y gráficos para una provincia seleccionada.
    """
    df_provincia = df[df['provincia_nombre'] == provincia_seleccionada].copy()

    if len(df_provincia) == 0:
        st.warning("No hay datos disponibles para esta provincia")
        return

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

    col1, col2 = st.columns(2)

    with col1:
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
        fig_tiempo.update_traces(line_color='#0A497A', line_width=3)
        st.plotly_chart(fig_tiempo, use_container_width=True)

    with col2:
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
        fig_mes.update_traces(marker_color= '#D9534F')
        st.plotly_chart(fig_mes, use_container_width=True)

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
