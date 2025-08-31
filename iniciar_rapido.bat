@echo off
chcp 65001 >nul
title Mapa Interactivo Argentina - Inicio Rápido

echo.
echo 🚀 Iniciando Mapa Interactivo de Argentina...
echo.

echo 📋 URL: http://localhost:8501
echo 📋 Para detener: Ctrl+C
echo.

py -m streamlit run mapa_argentina_interactivo.py

pause
