"""
Carga y preprocesamiento de datos.
"""

import os
import pandas as pd
import numpy as np
import streamlit as st
from app.utils import limpiar_edad
from typing import Optional


# Ruta absoluta al CSV 
BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # sube desde app/ a S.A.S.V/
DATA_PATH = os.path.join(BASE_DIR, "data", "MUERTES_VIALES.csv")


@st.cache_data
def cargar_datos(path: str = DATA_PATH) -> Optional[pd.DataFrame]:
    """
    Carga el CSV y aplica limpieza básica:
    - Filtra provincias desconocidas
    - Convierte lat/long, año, mes
    - Normaliza edades con limpiar_edad
    - Devuelve DataFrame o None si ocurre error
    """
    try:
        df = pd.read_csv(
            path,
            sep=";",
            encoding="utf-8",
            low_memory=False
        )

        # Mantener todos los registros pero descartar 'Desconocido' o NaN en provincia
        df = df[df['provincia_nombre'] != 'Desconocido']
        df = df[df['provincia_nombre'].notna()]

        # Coordenadas a numérico
        df['latitud'] = pd.to_numeric(df['latitud'], errors='coerce')
        df['longitud'] = pd.to_numeric(df['longitud'], errors='coerce')

        # Limpiar edades con la función utilitaria
        if 'victima_tr_edad' in df.columns:
            df['victima_tr_edad'] = df['victima_tr_edad'].apply(limpiar_edad)
        else:
            df['victima_tr_edad'] = np.nan

        # Año y mes
        df['anio'] = pd.to_numeric(df['anio'], errors='coerce') if 'anio' in df.columns else np.nan
        df['mes'] = pd.to_numeric(df['mes'], errors='coerce') if 'mes' in df.columns else np.nan

        return df

    except Exception as e:
        st.error(f"Error al cargar datos: {str(e)}")
        return None
