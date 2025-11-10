import boto3
import json

# Let LocalStack / AWS SDK handle the endpoint internally
s3 = boto3.client('s3')

def handler(event, context):
    file_name = event.get('file_name', 'test.txt')
    s3.put_object(
        Bucket='demo-bucket',
        Key=file_name,
        Body='Uploaded via Lambda from LocalStack!'
    )
    return {
        'statusCode': 200,
        'body': json.dumps({'uploaded': file_name})
    }