import boto3, base64, json

s3 = boto3.client('s3')

def handler(event, context):
    for record in event['Records']:
        data = base64.b64decode(record['kinesis']['data']).decode('utf-8')
        s3.put_object(
            Bucket='demo-pipeline-bucket',
            Key=f"record-{record['eventID']}.txt",
            Body=data
        )
    return {'statusCode':200, 'body':json.dumps('Processed successfully')}