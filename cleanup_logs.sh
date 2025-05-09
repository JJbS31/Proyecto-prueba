#!/bin/bash
# Script para limpiar logs antiguos
set -e

LOG_DIR="/var/log"
DAYS_TO_KEEP=7

echo "Eliminando logs de más de $DAYS_TO_KEEP días en $LOG_DIR..."
find $LOG_DIR -type f -name "*.log" -mtime +$DAYS_TO_KEEP -exec rm -f {} \;

echo "Limpieza de logs completada."