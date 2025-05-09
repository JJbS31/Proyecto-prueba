import boto3
import os

# Configura el nombre del bucket S3 aquí
BUCKET_NAME = 'punto10'

# Inicializa el cliente de S3
s3_client = boto3.client('s3')

def upload_file_to_s3(file_name, bucket, object_name=None):
    """
    Sube un archivo a un bucket S3.
    :param file_name: Ruta del archivo a cargar.
    :param bucket: Nombre del bucket S3.
    :param object_name: Nombre del archivo en S3. Si se deja en None, se usará el nombre del archivo local.
    """
    if object_name is None:
        object_name = os.path.basename(file_name)

    try:
        s3_client.upload_file(file_name, bucket, object_name)
        print(f"Archivo {file_name} cargado exitosamente a {bucket}/{object_name}")
    except Exception as e:
        print(f"Error al cargar el archivo {file_name}: {e}")

def upload_directory_to_s3(directory_path, bucket):
    """
    Carga todos los archivos de un directorio a un bucket S3.
    :param directory_path: Ruta del directorio a cargar.
    :param bucket: Nombre del bucket S3.
    """
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            object_name = os.path.relpath(file_path, directory_path)
            upload_file_to_s3(file_path, bucket, object_name)

if __name__ == "__main__":
    # Ruta del archivo o directorio a cargar
    ruta = input("Introduce la ruta del archivo o directorio a cargar: ")

    if os.path.isfile(ruta):
        # Cargar un archivo individual
        upload_file_to_s3(ruta, BUCKET_NAME)
    elif os.path.isdir(ruta):
        # Cargar todos los archivos de un directorio
        upload_directory_to_s3(ruta, BUCKET_NAME)
    else:
        print("La ruta proporcionada no es válida.")