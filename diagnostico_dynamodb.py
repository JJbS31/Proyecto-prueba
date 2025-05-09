import boto3
from dotenv import load_dotenv
import os
import sys

def diagnosticar_dynamodb():
    print("=== DIAGNÓSTICO DE DYNAMODB ===")
    
    # 1. Verificar si se cargaron las variables de entorno
    print("\n1. Verificando variables de entorno...")
    load_dotenv()
    aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    aws_region = os.getenv("AWS_DEFAULT_REGION")
    
    if not aws_access_key or not aws_secret_key:
        print("❌ ERROR: No se encontraron las credenciales de AWS en el archivo .env")
        print("   Asegúrate de que tu archivo .env contenga:")
        print("   AWS_ACCESS_KEY_ID=tu_access_key")
        print("   AWS_SECRET_ACCESS_KEY=tu_secret_key")
        print("   AWS_DEFAULT_REGION=tu_region")
        return
    
    if not aws_region:
        print("❌ ERROR: No se encontró la región de AWS en el archivo .env")
        print("   Asegúrate de que tu archivo .env contenga AWS_DEFAULT_REGION=tu_region")
        return
    
    print(f"✅ Variables de entorno cargadas correctamente")
    print(f"   Región configurada: {aws_region}")
    print(f"   Access Key ID: {aws_access_key[:4]}{'*' * (len(aws_access_key) - 4)}")
    
    # 2. Intentar conectar con DynamoDB
    print("\n2. Conectando con DynamoDB...")
    try:
        dynamodb = boto3.resource('dynamodb', region_name=aws_region)
        client = boto3.client('dynamodb', region_name=aws_region)
        
        # Verificar credenciales llamando a list_tables
        response = client.list_tables()
        print(f"✅ Conexión exitosa a DynamoDB")
        tablas = response.get('TableNames', [])
        if tablas:
            print(f"   Tablas existentes: {', '.join(tablas)}")
        else:
            print(f"   No hay tablas en la región {aws_region}")
    except Exception as e:
        print(f"❌ ERROR: No se pudo conectar a DynamoDB: {str(e)}")
        return
    
    # 3. Verificar si la tabla existe
    tabla_nombre = "Punto10"  # Nombre de la tabla del script original
    print(f"\n3. Verificando si la tabla '{tabla_nombre}' existe...")
    
    try:
        if tabla_nombre in tablas:
            print(f"✅ La tabla '{tabla_nombre}' existe")
            
            # 4. Verificar la estructura de la tabla
            print(f"\n4. Verificando estructura de la tabla '{tabla_nombre}'...")
            try:
                response = client.describe_table(TableName=tabla_nombre)
                key_schema = response['Table']['KeySchema']
                
                # Verificar si 'ID' es la clave primaria
                id_es_clave = False
                for key in key_schema:
                    if key['AttributeName'] == 'ID':
                        id_es_clave = True
                        break
                
                if id_es_clave:
                    print(f"✅ La tabla tiene 'ID' como clave primaria")
                else:
                    print(f"❌ ADVERTENCIA: La tabla no tiene 'ID' como clave primaria")
                    print(f"   Esquema de clave actual: {key_schema}")
                    print(f"   Esto podría causar errores en las operaciones del script original")
                
                # 5. Intentar operaciones básicas
                print(f"\n5. Probando operaciones básicas en la tabla...")
                tabla = dynamodb.Table(tabla_nombre)
                
                # Intentar insertar un registro de prueba
                print("   Insertando registro de prueba...")
                try:
                    response = tabla.put_item(
                        Item={
                            'ID': 'test123',
                            'Prueba': 'Diagnóstico',
                            'Valor': 1
                        }
                    )
                    print(f"✅ Inserción exitosa: {response}")
                except Exception as e:
                    print(f"❌ ERROR al insertar: {str(e)}")
                
                # Intentar leer el registro
                print("   Leyendo registro de prueba...")
                try:
                    response = tabla.get_item(
                        Key={
                            'ID': 'test123'
                        }
                    )
                    if 'Item' in response:
                        print(f"✅ Lectura exitosa: {response['Item']}")
                    else:
                        print(f"❌ ERROR: No se encontró el registro")
                except Exception as e:
                    print(f"❌ ERROR al leer: {str(e)}")
                
                # Intentar eliminar el registro de prueba
                print("   Eliminando registro de prueba...")
                try:
                    response = tabla.delete_item(
                        Key={
                            'ID': 'test123'
                        }
                    )
                    print(f"✅ Eliminación exitosa: {response}")
                except Exception as e:
                    print(f"❌ ERROR al eliminar: {str(e)}")
                
            except Exception as e:
                print(f"❌ ERROR al verificar estructura: {str(e)}")
        else:
            print(f"❌ ERROR: La tabla '{tabla_nombre}' no existe")
            print(f"   Debes crear la tabla '{tabla_nombre}' antes de ejecutar el script")
            print(f"   Puedes crear la tabla desde la consola de AWS o mediante código")
            print(f"   Ejemplo de código para crear la tabla:")
            print(f"""
            import boto3
            dynamodb = boto3.resource('dynamodb', region_name='{aws_region}')
            
            # Crear la tabla
            table = dynamodb.create_table(
                TableName='{tabla_nombre}',
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
            table.meta.client.get_waiter('table_exists').wait(TableName='{tabla_nombre}')
            print("Tabla creada exitosamente")
            """)
    except Exception as e:
        print(f"❌ ERROR: No se pudo verificar la existencia de la tabla: {str(e)}")

if __name__ == "__main__":
    diagnosticar_dynamodb()
