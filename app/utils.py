"""
Funciones de utilidad y constantes compartidas entre módulos (data, registro, mapa).
"""

import numpy as np
from typing import Any

def limpiar_edad(valor: Any) -> float:
    """
    Normaliza el campo de edad de víctimas.
    - Rangos "X-Y" -> promedio
    - "menos de N" -> N/2 (aprox)
    - números directos -> float
    - valores inválidos -> np.nan
    """
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


# Coordenadas centrales de las provincias argentinas (Latitud, Longitud)
# Utilizadas para centrar el mapa o preseleccionar coordenadas en el registro.
coordenadas_provincias = {
    "Buenos Aires": (-36.6769, -60.5598),
    "CABA": (-34.6037, -58.3816),
    "Catamarca": (-27.4578, -66.9084),
    "Chaco": (-27.0854, -60.8447),
    "Chubut": (-43.7925, -68.7495),
    "Córdoba": (-31.3995, -64.2127),
    "Corrientes": (-29.1723, -57.8540),
    "Entre Ríos": (-32.0520, -59.2016),
    "Formosa": (-24.9658, -59.5447),
    "Jujuy": (-23.3175, -65.7331),
    "La Pampa": (-37.1610, -65.4190),
    "La Rioja": (-29.8340, -67.1627),
    "Mendoza": (-34.6542, -68.5866),
    "Misiones": (-26.8687, -54.6534),
    "Neuquén": (-38.7454, -70.1172),
    "Río Negro": (-40.4026, -67.2014),
    "Salta": (-24.7821, -65.4239),
    "San Juan": (-30.8654, -68.8878),
    "San Luis": (-33.7431, -66.1960),
    "Santa Cruz": (-48.8156, -70.0152),
    "Santa Fe": (-31.6496, -60.7001),
    "Santiago del Estero": (-27.7801, -63.3644),
    "Tierra del Fuego": (-54.8019, -68.3030),
    "Tucumán": (-26.8083, -65.2282)
}
