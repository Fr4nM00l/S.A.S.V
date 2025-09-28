🇦🇷 S.A.S.V - Sistema de Análisis de Siniestros Viales en Argentina
📋 Descripción del Proyecto
Este proyecto es una aplicación web interactiva desarrollada con Streamlit para visualizar, analizar y gestionar datos de muertes viales en Argentina.

La aplicación ofrece un conjunto completo de herramientas analíticas (mapas, estadísticas, comparativas) y se complementa con un sistema de registro de incidentes que permite a los usuarios añadir nuevos datos de manera normalizada al archivo CSV original.


🚀 Características Principales:
___________________________________________________________________________________________________________________________________________________
                                                                                                                                                  
🗺️ Mapa Interactivo: Visualización geográfica de muertes viales por provincia.                                                                    
                                                                                                                                                  
🔥 Mapa de Calor: Identificación de zonas de alta concentración de siniestros viales.                                                            

➕ Registro de Incidentes: Formulario para añadir nuevos registros al archivo de datos CSV, asegurando la consistencia de los campos categóricos.

📊 Análisis Segmentado: Desglose detallado por tipo de vehículo, tipo de lugar y modo de producción del hecho.

📈 Análisis Comparativo: Comparación de métricas clave entre las provincias argentinas.

🔍 Explorador de Datos: Permite filtrar datos por rango de año y provincia para su previsualización y descarga.

📱 Interfaz Responsiva: Diseño moderno y adaptable a diferentes dispositivos.


🛠️ Tecnologías Utilizadas
_______________________________________________________

Python 3.8+

Streamlit - Framework web y de interfaz de usuario.

Pandas - Manipulación y gestión de datos.

Plotly - Gráficos interactivos y dinámicos.

Folium - Mapas interactivos geolocalizados.

NumPy - Cálculos numéricos y manejo de valores nulos.

📦 Instalación
______________________________________________________________________________________________

Prerrequisitos
Python 3.8 o superior

pip (gestor de paquetes de Python)

Pasos de Instalación
Opción 1: Inicio Automático (Recomendado para Windows)
Clonar el repositorio:

git clone [https://github.com/Fr4nM00l/S.A.S.V.git](https://github.com/Fr4nM00l/S.A.S.V.git)
cd S.A.S.V

Ejecutar el archivo .bat:

iniciar_aplicacion.bat

Opción 2: Inicio Manual
- Clonar el repositorio:

git clone [https://github.com/Fr4nM00l/S.A.S.V.git](https://github.com/Fr4nM00l/S.A.S.V.git)
- cd S.A.S.V

Instalar dependencias:

- pip install -r requirements.txt

Ejecutar la aplicación (Punto de entrada principal):

streamlit run main.py

____________________________________________________________________________________________________________________________________________________

📊 Estructura de Datos (MUERTES_VIALES.csv)
El archivo MUERTES_VIALES.csv (delimitado por ;) debe contener todas las columnas para que el registro funcione correctamente. Los campos clave para el análisis y la entrada de datos son:

______________________________________________________________________________________________________________________
** Campo Clave **             | ** Descripción **                    | ** Formato de Normalización **                 |
                              |                                      |                                                |
id_hecho                      | Identificador único del incidente.   | Generado automáticamente.                      |
                              |                                      |                                                |
provincia_nombre              | Nombre de la provincia.              | Lista cerrada (normalizada).                   |
                              |                                      |                                                |
latitud/longitud              | Coordenadas geográficas.             | Decimal Degrees (DD).                          |
                              |                                      |                                                |
fecha_hecho                   | Fecha completa del siniestro.        | Derivado del campo de fecha.                   |
                              |                                      |                                                |
victima_tr_edad               | Edad de la víctima.                  | Número entero.                                 |
                              |                                      |                                                |    
tipo_lugar                    | Clasificación del lugar.             | Lista cerrada (normalizada).                   |
                              |                                      |                                                |
victima/inculpado_vehiculo    | Tipo de vehículo involucrado.        | Lista cerrada (normalizada).                   |
                              |                                      |                                                |
modo_produccion_hecho         | Descripción del siniestro.           |Lista cerrada (normalizada).                    |
______________________________________________________________________________________________________________________|


🎯 Funcionalidades por Sección
_________________________________________________________________________________________________________________________________________________

1. Visualización Geográfica (Mapa)
Presenta un mapa interactivo de Argentina.

Permite alternar entre el Mapa de Coropletas (colores por provincia) y el Mapa de Calor (zonas de alta densidad).

2. Estadísticas Detalladas
Muestra métricas principales (Total Muertes, Edad Promedio).

Gráficos de evolución temporal y distribución mensual para la provincia seleccionada.

3. Registro de Nuevo Incidente (NUEVO)
Formulario de Entrada: Incluye campos mínimos y esenciales para la alta de un nuevo siniestro.

Normalización: Utiliza listas desplegables (selectbox) pobladas con los valores únicos ya existentes en el CSV, garantizando que los nuevos registros sean consistentes con los datos históricos.

Persistencia: El nuevo registro se añade directamente al archivo data/MUERTES_VIALES.csv.

4. Análisis Segmentado
Vehículos: Desglose por victima_vehiculo y inculpado_vehiculo.

Lugar y Modo: Distribución por tipo_lugar (Ruta, Calle) y modo_produccion_hecho (Colisión, Vuelco).


📁 Estructura del Proyecto
S.A.S.V/
│── app/
│   ├── __init__".py
│   ├── data_loader.py          <-- Carga y caché de datos.
│   ├── mapa.py                 <-- Lógica para Folium (Mapas Interactivo y de Calor).
│   ├── estadisticas.py         <-- Funciones para KPIs y gráficos por provincia.
│   ├── comparativo.py          <-- Funciones para el análisis entre provincias.
│   ├── graficos.py             <-- Funciones para análisis segmentado (Vehículos, Lugar, Modo).
│   ├── registro.py             <-- Lógica del formulario de registro de nuevos incidentes.
│   ├── utils.py
│── main.py                     <-- Punto de entrada de la aplicación Streamlit.
│── data/
│   └── MUERTES_VIALES.csv      <-- El conjunto de datos fuente.
│── requirements.txt            <-- Dependencias de Python.

🤝 Contribuciones
Las contribuciones son bienvenidas para mejorar las funcionalidades, optimizar el código o añadir más análisis.

Fork el proyecto.

Crea una rama para tu feature (git checkout -b feature/MiNuevaFuncionalidad).

Commit tus cambios y abre un Pull Request.

📄 Licencia
Este proyecto está bajo la Licencia MIT.

👨‍💻 Autors: 
__________________
FranM00l - GitHub |
__________________|
EF1507   - GitHUb |
__________________|

⭐ ¡Si te gusta este proyecto, dale una estrella en GitHub!
