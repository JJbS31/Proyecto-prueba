#!/bin/bash
# Script para instalar paquetes esenciales
set -e

echo "Actualizando repositorios..."
sudo apt update -y

echo "Instalando paquetes esenciales..."
sudo apt install -y git vim docker.io python3 python3-pip

echo "Habilitando Docker..."
sudo systemctl start docker
sudo systemctl enable docker

echo "Instalación completada."