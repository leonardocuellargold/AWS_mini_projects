# Data Pipeline Simulation (Kinesis + Lambda + S3)

Goal: Build a minimal local pipeline where a Kinesis stream receives data → a Lambda reads and processes it → S3 stores the result.

Environment: LocalStack (Docker) + AWS CLI + Python 3.9 + boto3

---

## Overview

This is a small, self-contained demo that shows an event-driven streaming flow using LocalStack as a local AWS environment. It demonstrates:

- Kinesis as an ingestion stream (producer) 
- Lambda as an event-driven consumer that processes records
- S3 as a durable sink for processed outputs

The instructions below assume LocalStack is running on localhost:4566 and the AWS CLI is available on your PATH.

Note: this README is sanitized for local user privacy. Replace `<your-computer-username>` with your actual macOS username where filesystem paths are required.

---

## Prerequisites

- Docker and LocalStack (or a running LocalStack instance)
- AWS CLI configured (we'll pass the LocalStack endpoint explicitly)
- Python 3.9 and boto3 (for the Lambda code)
- zip utility (to package the Lambda function)

If you don't have LocalStack running, a quick way to run it with Docker is:

```bash
# (optional) start LocalStack using the Docker image
docker run --rm -it -p 4566:4566 -p 4571:4571 localstack/localstack
```

---

## Steps

### 1) Create a Kinesis Stream

Create the stream (single shard for this demo):

```bash
aws --endpoint-url=http://localhost:4566 kinesis create-stream \
	--stream-name demo-stream \
	--shard-count 1

# Verify
aws --endpoint-url=http://localhost:4566 kinesis list-streams
```

### 2) Write the Lambda Consumer

Create a file named `lambda_kinesis_consumer.py` with the following contents (this file takes Kinesis base64-encoded record data, decodes it, and writes it to S3):

```python
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
```

Zip the function for deployment:

```bash
zip function.zip lambda_kinesis_consumer.py
```

### 3) Create an S3 bucket for outputs

```bash
aws --endpoint-url=http://localhost:4566 s3 mb s3://demo-pipeline-bucket
```

### 4) Create an IAM Role and Deploy the Lambda

Create a minimal assume-role policy and role in LocalStack (LocalStack uses account id 000000000000 in examples):

```bash
aws --endpoint-url=http://localhost:4566 iam create-role \
	--role-name lambda-stream-role \
	--assume-role-policy-document '{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":{"Service":"lambda.amazonaws.com"},"Action":"sts:AssumeRole"}]}'

aws --endpoint-url=http://localhost:4566 lambda create-function \
	--function-name streamConsumer \
	--runtime python3.9 \
	--handler lambda_kinesis_consumer.handler \
	--role arn:aws:iam::000000000000:role/lambda-stream-role \
	--zip-file fileb://function.zip
```

### 5) Connect the Lambda to the Stream

Create an event source mapping so Lambda will receive records from Kinesis (batch-size 1 keeps it simple):

```bash
aws --endpoint-url=http://localhost:4566 lambda create-event-source-mapping \
	--function-name streamConsumer \
	--batch-size 1 \
	--starting-position LATEST \
	--event-source-arn arn:aws:kinesis:us-east-1:000000000000:stream/demo-stream

# Inspect mappings
aws --endpoint-url=http://localhost:4566 lambda list-event-source-mappings
```

### 6) Push Data Into the Stream

Put a single record into the stream. The example below sends a base64 payload that decodes to "Sample Data – LocalStack Test":

```bash
aws --endpoint-url=http://localhost:4566 kinesis put-record \
	--stream-name demo-stream \
	--partition-key 1 \
	--data "U2FtcGxlIERhdGEgLS0gTG9jYWxTdGFjayBUZXN0"
```

Wait a few seconds and list the bucket contents:

```bash
aws --endpoint-url=http://localhost:4566 s3 ls s3://demo-pipeline-bucket
```

You should see a file like `record-<eventID>.txt` containing the decoded data.

---

## Lessons Learned

- Streaming architecture: Kinesis decouples producers from consumers for scalable ingestion.
- Event-driven processing: Lambda reacts to stream events and persists results without polling.
- S3 as a sink: cheap, durable storage for processed outputs or downstream analytics.
- Hybrid cloud parallel: the same pattern maps to Azure Event Hubs / Functions or GCP Pub/Sub / Cloud Functions.

---

## Interview Talking Point

“I built a local data-pipeline demo using Kinesis → Lambda → S3 in LocalStack. It showed me how event-driven systems scale better than synchronous APIs, and how cloud services interconnect in real-time architectures that support modernization efforts.”

---

## Next Steps

- Once you confirm you see the object in S3, continue to Mini-Project 5 — Containerized Microservice (ECR + ECS).
- Optional improvements: add error handling, dead-letter queue for failed records, invoke Lambda via Kinesis client library (KCL) for advanced checkpointing, or wire up a downstream analytics consumer.
