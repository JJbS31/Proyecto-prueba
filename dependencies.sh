#!/bin/bash
# Script para instalar dependencias

# Instalar dependencias para un proyecto de Python
echo "Instalando dependencias de Python..."
pip3 install -r requirements.txt

# Construcción de una imagen Docker
echo "Construyendo imagen Docker..."
docker build -t my_app .

# Ejecutar contenedor Docker
echo "Ejecutando contenedor Docker..."
docker run -d --name my_app_container my_app