import boto3
import pymysql
import os
import json

def lambda_handler(event, context):
    secret_name = os.environ['SECRET_NAME']
    database = os.environ['DB_NAME']
    stage = os.environ['STAGE'] 

    secrets_client = boto3.client('secretsmanager')

    try:
        response = secrets_client.get_secret_value(SecretId=secret_name)
        secret = json.loads(response['SecretString'])

        user_key = f'user_{stage}'
        password_key = f'password_{stage}'
        host = secret['host']
        user = secret[user_key]
        password = secret[password_key]
        port = secret['port']

        connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            db=database,
            port=port,
            connect_timeout=5
        )

        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM alumnos;")
            results = cursor.fetchall()

        return {
            "statusCode": 200,
            "body": results
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "error": str(e)
        }

    finally:
        if 'connection' in locals():
            connection.close()