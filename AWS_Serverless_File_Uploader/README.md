# AWS Serverless File Uploader (LocalStack Demo)

This mini-project simulates a serverless file-upload workflow using AWS Lambda and S3, all running locally through LocalStack.  
It’s a lightweight hands-on demo I built to prep for my IBM Consulting – Hybrid Cloud (AWS Modernization) interview and to show real-world understanding of event-driven cloud design.

---

## Tech Stack
- **LocalStack (Docker)** – local AWS emulator  
- **AWS CLI v2** – interface to services  
- **Python 3.9 + boto3** – Lambda logic  
- **S3 + Lambda + IAM** – core AWS services mocked locally  

---

## What It Does
1. Creates a local S3 bucket (`demo-bucket`).  
2. Deploys a Python Lambda function that uploads a file to S3.  
3. Invokes the Lambda manually with a test payload (`demo.txt`).  
4. Confirms the uploaded file exists inside the bucket.  

The whole flow runs in under 5 minutes, no AWS charges, and mirrors real production behavior.

---

## Architecture
```text
Client → Lambda → S3
          │
          └──> IAM Role (lambda-role)

Each invocation sends a filename payload → Lambda writes a text object → S3 stores it.
```

⸻

## Quick Start

1. Start LocalStack
``` bash
localstack start
```

2. Create Bucket
```bash
aws --endpoint-url=http://localhost:4566 s3 mb s3://demo-bucket
```
3. Deploy Lambda
```bash
zip function.zip lambda_function.py
aws --endpoint-url=http://localhost:4566 lambda create-function \
  --function-name uploadFunc \
  --runtime python3.9 \
  --handler lambda_function.handler \
  --role arn:aws:iam::000000000000:role/lambda-role \
  --zip-file fileb://function.zip
```
4. Invoke
```bash
aws --endpoint-url=http://localhost:4566 lambda invoke \
  --function-name uploadFunc \
  --payload '{"file_name":"demo.txt"}' \
  --cli-binary-format raw-in-base64-out \
  response.json
```
5. Verify
```bash
aws --endpoint-url=http://localhost:4566 s3 ls s3://demo-bucket
```

⸻

## Lambda Code
```python
import boto3, json
s3 = boto3.client('s3')

def handler(event, context):
    file_name = event.get('file_name', 'test.txt')
    s3.put_object(Bucket='demo-bucket', Key=file_name, Body='Uploaded via Lambda!')
    return {'statusCode': 200, 'body': json.dumps({'uploaded': file_name})}
```
