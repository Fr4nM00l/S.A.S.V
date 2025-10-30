"""
Mapas interactivos (mapa por provincias y mapa de calor).
"""

import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
import streamlit as st
import pandas as pd
# Importación correcta: 'coordenadas_provincias' ahora viene de 'app.utils'
from app.utils import coordenadas_provincias 


def crear_mapa_argentina_interactivo(df: pd.DataFrame) -> folium.Map:
    """
    Crea un mapa de Argentina con marcadores por provincia.
    Retorna el objeto folium.Map (no hace display por sí mismo).
    """
    # Agrupar y calcular estadísticas por provincia
    stats_provincia = df.groupby('provincia_nombre').agg({
        'id_hecho': 'count',
        'victima_tr_edad': lambda x: x.dropna().mean() if len(x.dropna()) > 0 else 0,
        'anio': lambda x: x.dropna().min() if len(x.dropna()) > 0 else 0
    }).round(2)

    # año máximo
    stats_max = df.groupby('provincia_nombre')['anio'].agg(
        lambda x: x.dropna().max() if len(x.dropna()) > 0 else 0
    ).round(2)

    stats_provincia['anio_max'] = stats_max
    stats_provincia.columns = ['total_muertes', 'edad_promedio', 'anio_min', 'anio_max']
    stats_provincia = stats_provincia.reset_index()

    # NOTA: El diccionario coordenadas_provincias se importa ahora desde app.utils
    
    # Usamos Buenos Aires como centro de inicio (de las coordenadas importadas)
    mapa = folium.Map(
        location=coordenadas_provincias.get('Buenos Aires', [-34.60, -64.21]),
        zoom_start=5,
        tiles='OpenStreetMap',
        control_scale=True
    )

    for _, row in stats_provincia.iterrows():
        provincia = row['provincia_nombre']
        if provincia in coordenadas_provincias:
            lat, lon = coordenadas_provincias[provincia]

            total_muertes = row['total_muertes']
            # NOTA: Paleta que resalta más (rojo-naranja-amarillo-verde)
            if total_muertes > 5000:
                color = '#D9534F'  # Rojo fuerte (Advertencia)
                size = 15
            elif total_muertes > 2000:
                color = '#FF8C00'  # Naranja
                size = 12
            elif total_muertes > 500:
                color = '#FFD700'  # Amarillo/Oro
                size = 10
            else:
                color = "#24F81D"  # Azul profundo (Base)
                size = 8

            # Cálculo de promedio anual para el popup
            rango_anios = row['anio_max'] - row['anio_min']
            promedio_anual = total_muertes / (rango_anios + 1) if rango_anios >= 0 else total_muertes


            popup_text = f"""
            <div style="width: 250px; font-family: sans-serif; color: #333;">
                <h3 style="color: {color}; margin-bottom: 10px;">{provincia}</h3>
                <table style="width: 100%; border-collapse: collapse;">
                    <tr><td style="padding: 3px 5px;"><strong>Total Muertes:</strong></td><td style="padding: 3px 5px; text-align: right;">{total_muertes:,.0f}</td></tr>
                    <tr><td style="padding: 3px 5px;"><strong>Edad Promedio:</strong></td><td style="padding: 3px 5px; text-align: right;">{row['edad_promedio']:.1f} años</td></tr>
                    <tr><td style="padding: 3px 5px;"><strong>Período:</strong></td><td style="padding: 3px 5px; text-align: right;">{row['anio_min']:.0f}-{row['anio_max']:.0f}</td></tr>
                    <tr><td style="padding: 3px 5px;"><strong>Promedio/año:</strong></td><td style="padding: 3px 5px; text-align: right;">{promedio_anual:.0f}</td></tr>
                </table>
                <p style="margin-top: 10px; font-size: 12px; color: #666; text-align: center;">
                    Haz clic para ver estadísticas detalladas
                </p>
            </div>
            """

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

            # etiqueta (pequeña)
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

def crear_mapa_de_calor(df: pd.DataFrame):
    """
    Crea y muestra un mapa de calor en streamlit (hace st_folium internamente).
    """
    st.markdown("### 🔥 Mapa de Calor de las muertes viales en la República Argentina")
    st.markdown("Utiliza los filtros para explorar la concentración geográfica de los siniestros viales a lo largo del tiempo.")

    col1, col2 = st.columns(2)

    with col1:
        anio_min = int(df['anio'].dropna().min())
        anio_max = int(df['anio'].dropna().max())
        anios_seleccionados = st.slider(
            "Selecciona un rango de años:",
            min_value=anio_min,
            max_value=anio_max,
            value=(anio_min, anio_max)
        )

    with col2:
        meses_dict = {
            'Enero': 1, 'Febrero': 2, 'Marzo': 3, 'Abril': 4, 'Mayo': 5, 'Junio': 6,
            'Julio': 7, 'Agosto': 8, 'Septiembre': 9, 'Octubre': 10, 'Noviembre': 11, 'Diciembre': 12
        }
        todos_los_meses = list(meses_dict.keys())
        meses_seleccionados_nombres = st.multiselect(
            "Selecciona los meses:",
            options=todos_los_meses,
            default=todos_los_meses
        )

    if not meses_seleccionados_nombres:
        st.warning("Por favor, selecciona al menos un mes para visualizar los datos.")
        return

    meses_seleccionados_numeros = [meses_dict[nombre] for nombre in meses_seleccionados_nombres]

    df_filtrado = df[
        (df['anio'].between(anios_seleccionados[0], anios_seleccionados[1])) &
        (df['mes'].isin(meses_seleccionados_numeros))
    ]

    df_mapa = df_filtrado.dropna(subset=['latitud', 'longitud'])

    if df_mapa.empty:
        st.warning(f"No se encontraron siniestros con coordenadas para los filtros seleccionados. Intenta con otro rango de fechas.")
        return

    st.success(f"Mostrando {len(df_mapa):,} siniestros en el mapa de calor.")

    mapa_calor = folium.Map(
        location=[-38, -63],
        zoom_start=4,
        tiles='CartoDB dark_matter',
        control_scale=True
    )

    coordenadas = df_mapa[['latitud', 'longitud']].values.tolist()

    HeatMap(
        coordenadas,
        radius=10,
        blur=12
    ).add_to(mapa_calor)

    st_folium(mapa_calor, width=800, height=600)
