# 🇦🇷 Mapa Interactivo de Argentina - Análisis de Muertes Viales

## 📋 Descripción del Proyecto

Este proyecto presenta una aplicación web interactiva desarrollada con **Streamlit** que permite visualizar y analizar datos de muertes viales en Argentina por provincia. La aplicación incluye un mapa interactivo, estadísticas detalladas y herramientas de análisis comparativo.

## 🚀 Características Principales

- **🗺️ Mapa Interactivo**: Visualización geográfica de muertes viales por provincia
- **📊 Estadísticas Detalladas**: Análisis específico por provincia con gráficos temporales
- **📈 Análisis Comparativo**: Comparación entre provincias argentinas
- **🔍 Explorador de Datos**: Filtros avanzados y descarga de datos
- **📱 Interfaz Responsiva**: Diseño moderno y fácil de usar

## 🛠️ Tecnologías Utilizadas

- **Python 3.8+**
- **Streamlit** - Framework web
- **Pandas** - Manipulación de datos
- **Plotly** - Gráficos interactivos
- **Folium** - Mapas interactivos
- **NumPy** - Cálculos numéricos

## 📦 Instalación

### Prerrequisitos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar el repositorio:**
```bash
git clone https://github.com/Fr4nM00l/S.A.S.V.git
cd S.A.S.V
```

2. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

3. **Ejecutar la aplicación:**
```bash
streamlit run mapa_argentina_interactivo.py
```

## 📊 Estructura de Datos

El proyecto utiliza el archivo `MUERTES_VIALES.csv` que contiene:
- **provincia_nombre**: Nombre de la provincia
- **localidad_nombre**: Nombre de la localidad
- **anio**: Año del incidente
- **mes**: Mes del incidente
- **victima_tr_edad**: Edad de la víctima
- **latitud/longitud**: Coordenadas geográficas
- **id_hecho**: Identificador único del incidente

## 🎯 Funcionalidades

### 1. Mapa Interactivo
- Visualización geográfica de todas las provincias argentinas
- Marcadores de colores según la cantidad de muertes
- Información detallada al hacer clic en cada provincia

### 2. Estadísticas por Provincia
- Métricas principales (total muertes, edad promedio, período)
- Gráficos de evolución temporal
- Distribución por meses
- Top 10 localidades con más muertes

### 3. Análisis Comparativo
- Comparación entre todas las provincias
- Gráficos de barras interactivos
- Tabla de estadísticas completa

### 4. Explorador de Datos
- Filtros por año y provincia
- Vista de datos filtrados
- Descarga de datos en formato CSV

## 🎨 Características del Diseño

- **Interfaz moderna** con gradientes y colores atractivos
- **Responsive design** que se adapta a diferentes tamaños de pantalla
- **Navegación intuitiva** con sidebar de control
- **Gráficos interactivos** con Plotly
- **Mapas interactivos** con Folium

## 📈 Uso de la Aplicación

1. **Selecciona una opción** en el panel de control lateral
2. **Explora el mapa** haciendo clic en las provincias
3. **Analiza estadísticas** específicas por provincia
4. **Compara provincias** en el análisis comparativo
5. **Filtra y descarga** datos según tus necesidades

## 🔧 Configuración

### Variables de Entorno
No se requieren variables de entorno adicionales.

### Personalización
Puedes modificar:
- Colores del mapa en `crear_mapa_argentina_interactivo()`
- Estilos CSS en los `st.markdown()`
- Configuración de gráficos en las funciones de Plotly

## 📝 Notas Técnicas

- **Caché de datos**: Los datos se cargan una vez y se almacenan en caché
- **Optimización**: Procesamiento eficiente de grandes volúmenes de datos
- **Compatibilidad**: Funciona en Windows, macOS y Linux

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Para contribuir:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 👨‍💻 Autor

**FranM00l** - [GitHub](https://github.com/Fr4nM00l)

## 🙏 Agradecimientos

- Datos proporcionados por fuentes oficiales argentinas
- Comunidad de Streamlit por el excelente framework
- Contribuidores de las librerías utilizadas

---

⭐ **¡Si te gusta este proyecto, dale una estrella en GitHub!**
