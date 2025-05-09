# Usamos una imagen base ligera basada en Python
FROM python:3.11-slim-bookworm

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar los archivos necesarios al contenedor
COPY . /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    nginx \
    && rm -rf /var/lib/apt/lists/*

# Instalar las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Configurar Nginx
COPY nginx.conf /etc/nginx/nginx.conf

# Exponer el puerto donde Nginx escuchará
EXPOSE 80

# Comando para ejecutar la aplicación Flask con Nginx como proxy
CMD ["sh", "-c", "nginx && gunicorn --bind 0.0.0.0:5000 app:app"]