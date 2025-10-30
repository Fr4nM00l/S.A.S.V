"""
Funciones para gestionar el registro de nuevos incidentes viales.
Se enfoca en la interfaz de Streamlit para la entrada de datos
y la lógica para añadir el nuevo registro al archivo MUERTES_VIALES.csv.
"""
import streamlit as st
import pandas as pd
import os
from datetime import datetime
import uuid
import numpy as np
from app.utils import coordenadas_provincias # <--- IMPORTACIÓN AÑADIDA
from typing import Union

# Ruta del archivo CSV de datos. Asume que el archivo está en la carpeta 'data' al mismo nivel que 'app'.
DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'MUERTES_VIALES.csv')
DELIMITER = ';' # El CSV usa punto y coma como delimitador

def cargar_datos_registro(path: str = DATA_PATH) -> Union[pd.DataFrame, None]:
    """Intenta cargar el DataFrame para obtener los valores únicos de los selectores."""
    if not os.path.exists(path): # Si no existe el archivo, no se puede cargar
        st.warning(f"Archivo de datos no encontrado en: {path}. El formulario usará opciones por defecto.")
        # Retorna un DataFrame vacío con las columnas esperadas
        return pd.DataFrame(columns=[
            'provincia_nombre', 'tipo_lugar', 'victima_sexo', 
            'victima_vehiculo', 'inculpado_vehiculo', 'modo_produccion_hecho'
        ])
    try:
        # Importante: Usar el delimitador correcto (punto y coma)
        df = pd.read_csv(path, sep=DELIMITER)
        return df
    except Exception as e:
        st.error(f"Error al leer el CSV de registro ({path}): {e}")
        return None

def obtener_siguiente_id(df: pd.DataFrame) -> int:
    """Genera un nuevo ID basado en el máximo existente o un UUID."""
    try:
        # Intentamos encontrar el ID numérico más alto y sumarle 1
        max_id = df['id_hecho'].astype(str).str.extract(r'(\d+)', expand=False).astype(float).max()
        if pd.isna(max_id):
            return 100000 # Comenzamos desde un número alto si no hay IDs numéricos
        return int(max_id) + 1
    except:
        # Si el ID no es numérico o hay error, usamos un UUID aleatorio (como fallback)
        st.warning("No se pudo generar un ID numérico secuencial. Usando UUID.")
        return str(uuid.uuid4())


def mostrar_formulario_registro():
    """
    Muestra el formulario de registro y gestiona el guardado del nuevo registro en el CSV.  
    Usa st.form para agrupar los campos y un botón de envío.
    """
    
    # Cargar datos para obtener las opciones únicas
    df_base = cargar_datos_registro() 
    if df_base is None:
        return
        
    # --- Opciones Normalizadas (limpieza y ordenamiento) ---
    def get_options(col_name, default_list):
        if col_name in df_base.columns:
            # Reemplazar valores NaN por "Desconocido" y obtener únicos
            options = df_base[col_name].fillna("Desconocido").astype(str).unique().tolist()
            # Opcionalmente, agregar una limpieza de espacios y capitalización
            options = sorted([o.strip().title() for o in options if o.strip() not in ('', 'nan')])
            return ["Seleccione..."] + options
        return ["Seleccione..."] + default_list

    # Mapeo de nombres largos a las claves de coordenadas (ej: 'Ciudad Autónoma de Buenos Aires' -> 'CABA')
    PROVINCIA_COORD_MAP = {
        'Ciudad Autónoma de Buenos Aires': 'CABA',
        **{p: p for p in coordenadas_provincias.keys() if p != 'CABA'} 
    }

    # Lista de provincias en formato de visualización
    provincias_argentinas_display = [
        'Ciudad Autónoma de Buenos Aires', 'Buenos Aires', 'Catamarca', 'Chaco', 'Chubut', 
        'Córdoba', 'Corrientes', 'Entre Ríos', 'Formosa', 'Jujuy', 'La Pampa', 
        'La Rioja', 'Mendoza', 'Misiones', 'Neuquén', 'Río Negro', 'Salta', 
        'San Juan', 'San Luis', 'Santa Cruz', 'Santa Fe', 'Santiago del Estero', 
        'Tierra del Fuego', 'Tucumán'
    ]

    # Lista de opciones para el selector externo
    provincias_opciones = ["Seleccione..."] + sorted(provincias_argentinas_display)
    
    # Opciones de otros selectores
    tipos_lugar = get_options('tipo_lugar', ['Ruta', 'Calle', 'Autopista'])
    vehiculos = get_options('victima_vehiculo', ['Auto', 'Moto', 'Bicicleta', 'Peatón', 'Camión'])
    modos_produccion = get_options('modo_produccion_hecho', ['Colisión vehículo-vehículo', 'Vuelco', 'Colisión vehículo-persona'])
    generos = ["Seleccione...", "Masculino", "Femenino", "Otro", "Sin determinar"]
    
    # --- LÓGICA DE CENTRADO DEL FORMULARIO ---
    # 1. Creamos tres columnas: un espacio vacío (1 unidad), la columna central para el formulario (3 unidades), y otro espacio vacío (1 unidad).
    # Esto empuja el formulario al centro.
    col_izq, col_central, col_der = st.columns([0.5, 8, 0.5])
    
    # 2. Toda la interfaz del formulario se coloca DENTRO de la columna central.
    with col_central:
        
        st.subheader("Información Esencial del Incidente")
        
        # --- SELECTOR DE PROVINCIA EXTERNO ---
        # Este cambio dispara la actualización de las coordenadas
        # Usamos un solo contenedor para el selector de provincia dentro de la col_central

        provincia_col_solo = st.container()
        with provincia_col_solo:
            # Añadir index=0 para asegurar que la primera opción ("Seleccione...") se muestre siempre.
            provincia_seleccionada = st.selectbox(
                "🌎 Provincia", 
                provincias_opciones, 
                index=0, # Asegura que aparezca "Seleccione..." al cargar la página
                key="provincia_nombre_external"
            )

        # Calcular las coordenadas por defecto basadas en la provincia seleccionada
        if provincia_seleccionada != "Seleccione...":
            provincia_coord_key = PROVINCIA_COORD_MAP.get(provincia_seleccionada, None)
            # Si la clave existe en coordenadas_provincias, usar sus valores. Si no, vamos a usar CABA como default.
            default_lat, default_lon = coordenadas_provincias.get(provincia_coord_key, (-34.6037, -58.3816))
        else:
            # Si no hay provincia seleccionada, usar CABA como valor predeterminado
            default_lat, default_lon = coordenadas_provincias.get('CABA', (-34.6037, -58.3816))
        
        with st.form("registro_incidente_form"):
            col1, col2, col3 = st.columns(3)
            
            # Columna 1: Fecha y Ubicación
            with col1:
                st.markdown("<p style='visibility: hidden;'>placeholder</p>", unsafe_allow_html=True) # Alineación
                fecha_incidente = st.date_input("🗓️ Fecha del Hecho", datetime.now().date(), key="fecha_hecho")
                st.text_input("🌎 Provincia Seleccionada", provincia_seleccionada, disabled=True)
                localidad = st.text_input("🏙️ Localidad/Municipio", key="localidad_nombre")
                
                
            # Columna 2: Geo y Tipo de Lugar
            with col2:
                st.markdown("<p style='visibility: hidden;'>placeholder</p>", unsafe_allow_html=True) # Alineación
                # Usar los valores calculados dinámicamente como valores iniciales
                latitud = st.number_input(
                    "📍 Latitud", 
                    format="%.6f", 
                    value=default_lat, # <--- VALOR DINÁMICO
                    help=f"Coordenada Y. Valor por defecto de {provincia_seleccionada}.", 
                    key="latitud"
                )
                longitud = st.number_input(
                    "📍 Longitud", 
                    format="%.6f", 
                    value=default_lon, # <--- VALOR DINÁMICO
                    help=f"Coordenada X. Valor por defecto de {provincia_seleccionada}.", 
                    key="longitud"
                )
                tipo_lugar = st.selectbox("🛣️ Tipo de Lugar", tipos_lugar, key="tipo_lugar")
                
            # Columna 3: Detalles del Hecho
            with col3:
                st.markdown("<p style='visibility: hidden;'>placeholder</p>", unsafe_allow_html=True) # Alineación
                edad = st.number_input("👤 Edad de la Víctima", min_value=0, max_value=120, value=30, key="victima_tr_edad")
                genero = st.selectbox("🚻 Género de la Víctima", generos, key="victima_sexo")
                modo_produccion = st.selectbox("🚨 Modo de Producción del Hecho", modos_produccion, key="modo_produccion_hecho")

            st.markdown("---")
            st.subheader("Vehículos Involucrados")
            col4, col5 = st.columns(2)
            
            with col4:
                vehiculo_victima = st.selectbox("🚗 Vehículo de la Víctima", vehiculos, key="victima_vehiculo")

            with col5:
                vehiculo_inculpado = st.selectbox("🚙 Vehículo del Inculpado", vehiculos, key="inculpado_vehiculo")
                
            st.markdown("---")
            submitted = st.form_submit_button("💾 Guardar Nuevo Registro", type="primary")

        if submitted:
            # Validar selección de valores
            campos_a_validar = {
                "Provincia": provincia_seleccionada, 
                "Tipo de Lugar": tipo_lugar, "Género": genero,
                "Vehículo Víctima": vehiculo_victima, "Vehículo Inculpado": vehiculo_inculpado,
                "Modo de Producción": modo_produccion
            }
            
            if any(v == "Seleccione..." for v in campos_a_validar.values()):
                st.error("⚠️ Por favor, complete todos los campos de selección.")
                return

            # 1. Crear el nuevo registro con los campos mínimos requeridos
            nuevo_id = obtener_siguiente_id(df_base)
            
            nuevo_registro = {
                # Campos obligatorios del CSV
                'id_hecho': nuevo_id,
                'provincia_nombre': provincia_seleccionada, 
                'localidad_nombre': localidad,
                'anio': fecha_incidente.year,
                'mes': fecha_incidente.month,
                'fecha_hecho': fecha_incidente.strftime('%d/%m/%Y'),
                'latitud': latitud,
                'longitud': longitud,
                'victima_tr_edad': edad,
                'victima_sexo': genero,
                'tipo_lugar': tipo_lugar,
                'modo_produccion_hecho': modo_produccion,
                'victima_vehiculo': vehiculo_victima,
                'inculpado_vehiculo': vehiculo_inculpado,
                
                # Campos restantes del CSV (se rellenan con np.nan)
                'federal': np.nan,
                'tipo_persona': 'Víctima', 
                'tipo_persona_id': np.nan,
                'provincia_id': np.nan,
                'departamento_id': np.nan,
                'departamento_nombre': np.nan,
                'localidad_id': np.nan,
                'hora_hecho': np.nan,
                'calle_nombre': np.nan,
                'calle_altura': np.nan,
                'calle_interseccion': np.nan,
                'calle_interseccion_nombre': np.nan,
                'semaforo_estado': np.nan,
                'modo_produccion_hecho_ampliada': np.nan,
                'modo_produccion_hecho_otro': np.nan,
                'clima_condicion': np.nan,
                'clima_otro': np.nan,
                'motivo_origen_registro': np.nan,
                'motivo_origen_registro_otro': np.nan,
                'victima_18_años_o_mas': 'Sí' if edad >= 18 else 'No',
                'victima_clase': np.nan,
                'victima_clase_otro': np.nan,
                'victima_vehiculo_ampliado': np.nan,
                'victima_vehiculo_otro': np.nan,
                'victima_identidad_genero': np.nan,
                'inculpado_sexo': np.nan,
                'inculpado_tr_edad': np.nan,
                'inculpado_18_años_o_mas': np.nan,
                'inculpado_vehiculo_ampliado': np.nan,
                'inculpado_vehiculo_otro': np.nan,
                'inculpado_identidad_genero': np.nan,
            }
            
            # Asegurar que el diccionario tenga todas las 44 columnas del CSV original
            columnas_csv = df_base.columns.tolist()
            registro_final = {col: nuevo_registro.get(col, np.nan) for col in columnas_csv}


            # 2. Crear el DataFrame de un solo registro y guardar
            try:
                nuevo_df = pd.DataFrame([registro_final])
                
                # Guardar en el CSV, modo 'a' (append) y sin escribir el encabezado si el archivo ya existe.
                # Usar el delimitador punto y coma (';')
                nuevo_df.to_csv(
                    DATA_PATH, 
                    mode='a', 
                    index=False, 
                    header=False, # Nunca escribir encabezado al añadir
                    sep=DELIMITER 
                )
                
                st.success(f"✅ ¡Registro #{nuevo_id} guardado con éxito en el archivo CSV!")
                st.balloons()
                
                # Opcionalmente, forzar una recarga de datos en Streamlit para ver el cambio
                st.session_state["data_reloaded"] = True
                
            except Exception as e:
                st.error(f"❌ Error al guardar el registro en el CSV: {e}")

# Ejecución de la función
if __name__ == "__main__":
    st.set_page_config(layout="wide")
    mostrar_formulario_registro()
