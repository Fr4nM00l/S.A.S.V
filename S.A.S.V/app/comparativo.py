"""
Funciones para análisis comparativo entre provincias.
"""

import streamlit as st
import pandas as pd
import plotly.express as px

def mostrar_analisis_comparativo(df: pd.DataFrame):
    """
    Muestra gráficos y tablas comparativas entre provincias.
    """
    stats_comparativo = df.groupby('provincia_nombre').agg({
        'id_hecho': 'count',
        'victima_tr_edad': lambda x: x.dropna().mean() if len(x.dropna()) > 0 else 0,
        'anio': lambda x: x.dropna().nunique() if len(x.dropna()) > 0 else 0
    }).round(2)

    stats_comparativo.columns = ['Total Muertes', 'Edad Promedio', 'Años con Datos']
    stats_comparativo = stats_comparativo.sort_values('Total Muertes', ascending=False)

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

    st.subheader("📋 Tabla de Estadísticas por Provincia")
    st.dataframe(stats_comparativo, use_container_width=True)
