@echo off
chcp 65001 >nul
title Mapa Interactivo Argentina - Muertes Viales

echo.
echo ========================================
echo    🇦🇷 MAPA INTERACTIVO DE ARGENTINA
echo    📊 Análisis de Muertes Viales
echo ========================================
echo.

echo 🔍 Verificando Python...
py --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Python no está instalado o no está en el PATH
    echo.
    echo 📥 Por favor, instala Python desde: https://www.python.org/downloads/
    echo    Asegúrate de marcar "Add Python to PATH" durante la instalación
    echo.
    pause
    exit /b 1
)

echo ✅ Python encontrado
echo.

echo 🔍 Verificando dependencias...
if not exist "requirements.txt" (
    echo ❌ ERROR: No se encontró el archivo requirements.txt
    echo.
    echo 📁 Asegúrate de estar en el directorio correcto del proyecto
    echo.
    pause
    exit /b 1
)

echo ✅ Archivo requirements.txt encontrado
echo.

echo 🔍 Verificando archivo de datos...
if not exist "MUERTES_VIALES.csv" (
    echo ❌ ERROR: No se encontró el archivo MUERTES_VIALES.csv
    echo.
    echo 📁 Asegúrate de que el archivo de datos esté en el directorio
    echo.
    pause
    exit /b 1
)

echo ✅ Archivo de datos encontrado
echo.

echo 📦 Instalando dependencias...
echo.
py -m pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo ❌ ERROR: No se pudieron instalar las dependencias
    echo.
    echo 🔧 Soluciones posibles:
    echo    1. Verifica tu conexión a internet
    echo    2. Actualiza pip: py -m pip install --upgrade pip
    echo    3. Instala las dependencias manualmente
    echo.
    pause
    exit /b 1
)

echo.
echo ✅ Dependencias instaladas correctamente
echo.

echo 🚀 Iniciando aplicación...
echo.
echo 📋 Información importante:
echo    • La aplicación se abrirá en tu navegador web
echo    • URL local: http://localhost:8501
echo    • Para detener la aplicación, presiona Ctrl+C
echo    • Cierra esta ventana cuando termines
echo.

echo ⏳ Iniciando Streamlit...
echo.
py -m streamlit run main.py

echo.
echo 👋 Aplicación cerrada
echo.
pause
