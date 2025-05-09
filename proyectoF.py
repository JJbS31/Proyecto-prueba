import datetime
import boto3
from dotenv import load_dotenv
import os

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Obtener las credenciales de las variables de entorno
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
aws_session_token = os.getenv('AWS_SESSION_TOKEN')
region_name = os.getenv('AWS_DEFAULT_REGION', 'us-east-1')

# Inicializar clientes de EC2 y CloudWatch
ec2 = boto3.client(
    'ec2',
    region_name=region_name,
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    aws_session_token=aws_session_token
)

cloudwatch = boto3.client(
    'cloudwatch',
    region_name=region_name,
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    aws_session_token=aws_session_token
)

def obtener_metricas_cloudwatch(instance_id):
    """
    Obtiene métricas básicas de CloudWatch para una instancia EC2.
    """
    print(f"\n=== Métricas de CloudWatch para la instancia {instance_id} ===")
    
    response = cloudwatch.get_metric_statistics(
        Namespace='AWS/EC2',
        MetricName='CPUUtilization',
        Dimensions=[
            {
                'Name': 'InstanceId',
                'Value': instance_id
            }
        ],
        StartTime=datetime.datetime.utcnow() - datetime.timedelta(hours=1),
        EndTime=datetime.datetime.utcnow(),
        Period=300,  # 5 minutos
        Statistics=['Average']
    )
    
    for datapoint in response['Datapoints']:
        timestamp = datapoint['Timestamp']
        average_cpu = datapoint['Average']
        print(f"  - Timestamp: {timestamp}, Uso promedio de CPU: {average_cpu:.2f}%")

def listar_recursos_por_tipo(tipo_instancia):
    """
    Lista las instancias EC2 del tipo especificado con métricas de CloudWatch.
    """
    print(f"\n=== Reporte de Recursos AWS - Tipo de Instancia: {tipo_instancia} ===\n")
    
    # Listar instancias EC2
    response = ec2.describe_instances()
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            state = instance['State']['Name']
            public_ip = instance.get('PublicIpAddress', 'N/A')
            instance_type = instance['InstanceType']
            
            # Obtener el nombre de la instancia
            name = 'N/A'
            if 'Tags' in instance:
                for tag in instance['Tags']:
                    if tag['Key'] == 'Name':
                        name = tag['Value']
                        break

            # Filtrar por tipo de instancia
            if instance_type == tipo_instancia:
                print(f"  - Nombre: {name}, ID: {instance_id}, Estado: {state}, IP Pública: {public_ip}, Tipo: {instance_type}")
                obtener_metricas_cloudwatch(instance_id)

if __name__ == "__main__":
    tipo = input("Por favor, ingrese el tipo de instancia que desea listar (ejemplo: t2.micro): ")
    listar_recursos_por_tipo(tipo)