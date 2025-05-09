#!/bin/bash
# Script para configurar tareas cron

echo "Configurando tareas cron..."

# Tarea para ejecutar la limpieza de logs todos los días a la medianoche
CRON_JOB="0 0 * * * /bin/bash /ruta/al/script/cleanup_logs.sh >> /var/log/cleanup_logs_cron.log 2>&1"

# Añadir tarea al crontab del usuario actual
(crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -

echo "Tareas cron configuradas."