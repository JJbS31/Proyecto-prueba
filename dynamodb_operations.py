import boto3
from dotenv import load_dotenv
import os
import sys

# Cargar variables del archivo .env
print("Cargando variables de entorno...")
load_dotenv()

# Verificar las variables de entorno
aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
aws_session_token = os.getenv("AWS_SESSION_TOKEN")
aws_region = os.getenv("AWS_DEFAULT_REGION")

if not aws_access_key or not aws_secret_key:
    print("ERROR: No se encontraron las credenciales de AWS en el archivo .env")
    sys.exit(1)

if not aws_region:
    print("ERROR: No se encontró la región de AWS en el archivo .env")
    sys.exit(1)

print(f"Región configurada: {aws_region}")
print(f"Access Key ID: {aws_access_key[:4]}{'*' * (len(aws_access_key) - 4)}")

# Crear cliente de DynamoDB (con token de sesión si está disponible)
try:
    session = boto3.Session(
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        aws_session_token=aws_session_token,
        region_name=aws_region
    )
    
    dynamodb = session.resource('dynamodb')
    client = session.client('dynamodb')
    
    # Verificar la conexión
    print("\nVerificando conexión a DynamoDB...")
    response = client.list_tables()
    print("Conexión exitosa a DynamoDB")
    tablas = response.get('TableNames', [])
    print(f"Tablas disponibles: {tablas}")
    
except Exception as e:
    print(f"ERROR al conectar con DynamoDB: {str(e)}")
    sys.exit(1)

# Nombre de la tabla
table_name = "Punto10"

# Verificar si la tabla existe
if table_name not in tablas:
    print(f"ERROR: La tabla '{table_name}' no existe. Debes crearla primero.")
    # Código para crear la tabla automáticamente
    print(f"Creando tabla '{table_name}'...")
    try:
        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': 'ID',
                    'KeyType': 'HASH'  # Clave de partición
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'ID',
                    'AttributeType': 'S'  # String
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        
        # Esperar a que la tabla esté disponible
        print(f"Esperando a que la tabla esté disponible...")
        table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
        print(f"Tabla '{table_name}' creada exitosamente")
    except Exception as e:
        print(f"ERROR al crear la tabla: {str(e)}")
        sys.exit(1)

# Obtener la referencia a la tabla
table = dynamodb.Table(table_name)

# Insertar un registro
def insertar_registro():
    try:
        response = table.put_item(
            Item={
                'ID': '123',  # Clave primaria (partición)
                'Nombre': 'Juan Pérez',
                'Edad': 30,
                'Ciudad': 'Madrid'
            }
        )
        print("Registro insertado exitosamente")
        return True
    except Exception as e:
        print(f"ERROR al insertar registro: {str(e)}")
        return False

# Modificar un registro
def modificar_registro():
    try:
        response = table.update_item(
            Key={
                'ID': '123'  # Clave primaria del registro a modificar
            },
            UpdateExpression="SET Ciudad = :val1, Edad = :val2",
            ExpressionAttributeValues={
                ':val1': 'Barcelona',
                ':val2': 31
            },
            ReturnValues="UPDATED_NEW"
        )
        print("Registro modificado exitosamente")
        print("Valores actualizados:", response.get('Attributes', {}))
        return True
    except Exception as e:
        print(f"ERROR al modificar registro: {str(e)}")
        return False

# Eliminar un registro
def eliminar_registro():
    try:
        response = table.delete_item(
            Key={
                'ID': '123'  # Clave primaria del registro a eliminar
            }
        )
        print("Registro eliminado exitosamente")
        return True
    except Exception as e:
        print(f"ERROR al eliminar registro: {str(e)}")
        return False

# Consultar un registro
def consultar_registro(id):
    try:
        response = table.get_item(
            Key={
                'ID': id
            }
        )
        item = response.get('Item')
        if item:
            print(f"Registro encontrado: {item}")
        else:
            print(f"No se encontró ningún registro con ID '{id}'")
        return item
    except Exception as e:
        print(f"ERROR al consultar registro: {str(e)}")
        return None

# Llamar a las funciones
if __name__ == "__main__":
    print("\n=== OPERACIONES EN DYNAMODB ===")
    
    print("\n1. Insertando registro...")
    if insertar_registro():
        print("\n2. Consultando registro recién insertado...")
        consultar_registro('123')
        
        print("\n3. Modificando registro...")
        if modificar_registro():
            print("\n4. Consultando registro modificado...")
            consultar_registro('123')
            
            print("\n5. Eliminando registro...")
            if eliminar_registro():
                print("\n6. Verificando que el registro fue eliminado...")
                consultar_registro('123')
    
    print("\n=== OPERACIONES COMPLETADAS ===")