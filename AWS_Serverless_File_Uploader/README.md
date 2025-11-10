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

## Local session transcript

Below is a verbatim transcript of a local terminal session showing the LocalStack / AWS CLI steps and responses while running this demo.

```bash
Last login: Sun Nov  9 14:10:28 on ttys000

The default interactive shell is now zsh.
To update your account to use zsh, please run `chsh -s /bin/zsh`.
For more details, please visit https://support.apple.com/kb/HT208050.
MacBook-Pro-3:AWS_Serverless_File_Uploader $ awslocal s3 mb s3://uploader bucket
-bash: awslocal: command not found
MacBook-Pro-3:AWS_Serverless_File_Uploader $ pip install localstack awscli-local
-bash: pip: command not found
MacBook-Pro-3:AWS_Serverless_File_Uploader $ aws --endpoint-url=http://localhost:4566 s3 ls
-bash: aws: command not found
MacBook-Pro-3:AWS_Serverless_File_Uploader $ aws --endpoint-url=http://localhost:4566 s3 mb s3://demo-bucket
make_bucket: demo-bucket
MacBook-Pro-3:AWS_Serverless_File_Uploader $ aws --endpoint-url=http://localhost:4566 s3 ls
2025-11-09 14:32:08 demo-bucket
MacBook-Pro-3:AWS_Serverless_File_Uploader $ zip function.zip lambda_function.py
  adding: lambda_function.py (deflated 30%)
MacBook-Pro-3:AWS_Serverless_File_Uploader $ aws --endpoint-url=http://localhost:4566 iam create-role \
>   --role-name lambda-role \
>   --assume-role-policy-document '{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":{"Service":"lambda.amazonaws.com"},"Action":"sts:AssumeRole"}]}'
{
  "Role": {
    "Path": "/",
    "RoleName": "lambda-role",
    "RoleId": "AROAQAAAAAAAIRDDOG4IT",
    "Arn": "arn:aws:iam::000000000000:role/lambda-role",
    "CreateDate": "2025-11-09T19:35:21.342942+00:00",
    "AssumeRolePolicyDocument": {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Effect": "Allow",
          "Principal": {
            "Service": "lambda.amazonaws.com"
          },
          "Action": "sts:AssumeRole"
        }
      ]
    }
  }
}
MacBook-Pro-3:AWS_Serverless_File_Uploader $ aws --endpoint-url=http://localhost:4566 lambda create-function \
>   --function-name uploadFunc \
>   --runtime python3.9 \
>   --role arn:aws:iam::000000000000:role/lambda-role \
>   --handler lambda_function.handler \
>   --zip-file fileb://function.zip
{
  "FunctionName": "uploadFunc",
  "FunctionArn": "arn:aws:lambda:us-east-1:000000000000:function:uploadFunc",
  "Runtime": "python3.9",
  "Role": "arn:aws:iam::000000000000:role/lambda-role",
  "Handler": "lambda_function.handler",
  "CodeSize": 414,
  "Description": "",
  "Timeout": 3,
  "MemorySize": 128,
  "LastModified": "2025-11-09T19:35:51.468475+0000",
  "CodeSha256": "PPgn2dOY3dcs1tnxFeHN3qjPadSgvrmwOXJxPWO7DXM=",
  "Version": "$LATEST",
  "TracingConfig": {
    "Mode": "PassThrough"
  },
  "RevisionId": "425ff403-5ff0-42ee-b99e-39b98dc07c4d",
  "State": "Pending",
  "StateReason": "The function is being created.",
  "StateReasonCode": "Creating",
  "PackageType": "Zip",
  "Architectures": [
    "x86_64"
  ],
  "EphemeralStorage": {
    "Size": 512
  },
  "SnapStart": {
    "ApplyOn": "None",
    "OptimizationStatus": "Off"
  },
  "RuntimeVersionConfig": {
    "RuntimeVersionArn": "arn:aws:lambda:us-east-1::runtime:8eeff65f6809a3ce81507fe733fe09b835899b99481ba22fd75b5a7338290ec1"
  },
  "LoggingConfig": {
    "LogFormat": "Text",
    "LogGroup": "/aws/lambda/uploadFunc"
  }
}
(END)
  "State": "Pending",
  "StateReason": "The function is being created.",
  "StateReasonCode": "Creating",
  "PackageType": "Zip",
  "Architectures": [
    "x86_64"
  ],
  "EphemeralStorage": {
    "Size": 512
  },
  "SnapStart": {
    "ApplyOn": "None",
    "OptimizationStatus": "Off"
  },
  "RuntimeVersionConfig": {
    "RuntimeVersionArn": "arn:aws:lambda:us-east-1::runtime:8eeff65f6809a3ce81507fe733fe09b835899b99481ba22fd75b5a7338290ec1"
  },
  "LoggingConfig": {
    "LogFormat": "Text",
    "LogGroup": "/aws/lambda/uploadFunc"
  }
}
(END)
MacBook-Pro-3:AWS_Serverless_File_Uploader $ > > > 
Invalid base64: "{"file_name":"demo.txt"}"
MacBook-Pro-3:AWS_Serverless_File_Uploader $ MacBook-Pro-3:AWS_Serverless_File_Uploader $ MacBook-Pro-3:AWS_Serverless_File_Uploader $ > > > 
Invalid base64: "{"file_name":"demo.txt"}"
MacBook-Pro-3:AWS_Serverless_File_Uploader $ > > > 
Invalid base64: "{"file_name":"demo.txt"}"
MacBook-Pro-3:AWS_Serverless_File_Uploader $ > > > 
Invalid base64: "{"file_name":"demo.txt"}"
{acBook-Pro-3:AWS_Serverless_File_Uploader $ > > > > 
  "StatusCode": 200,
  "FunctionError": "Unhandled",
  "ExecutedVersion": "$LATEST"
}
MacBook-Pro-3:AWS_Serverless_File_Uploader $ updating: lambda_function.py (deflated 37%)
MacBook-Pro-3:AWS_Serverless_File_Uploader $ MacBook-Pro-3:AWS_Serverless_File_Uploader leo{ardocuellar$ > > 
  "FunctionName": "uploadFunc",
  "FunctionArn": "arn:aws:lambda:us-east-1:000000000000:function:uploadFunc",
  "Runtime": "python3.9",
  "Role": "arn:aws:iam::000000000000:role/lambda-role",
  "Handler": "lambda_function.handler",
  "CodeSize": 448,
  "Description": "",
  "Timeout": 3,
  "MemorySize": 128,
  "LastModified": "2025-11-09T19:43:07.151104+0000",
  "CodeSha256": "LXvdaLwMPYUqBDeUetapigoS99FhowMr0udwb4q6LRU=",
  "Version": "$LATEST",
  "TracingConfig": {
    "Mode": "PassThrough"
  },
  "RevisionId": "cb4a2a13-706e-4556-b03d-36c28691011c",
  "State": "Active",
  "LastUpdateStatus": "InProgress",
  "LastUpdateStatusReason": "The function is being created.",
  "LastUpdateStatusReasonCode": "Creating",
  "PackageType": "Zip",
  "Architectures": [
    "x86_64"
  ],
  "EphemeralStorage": {
    "Size": 512
  },
  "SnapStart": {
    "ApplyOn": "None",
    "OptimizationStatus": "Off"
  },
  "RuntimeVersionConfig": {
    "RuntimeVersionArn": "arn:aws:lambda:us-east-1::runtime:8eeff65f6809a3ce81507fe733fe09b835899b99481ba22fd75b5a7338290ec1"
  },
  "LoggingConfig": {
    "LogFormat": "Text",
    "LogGroup": "/aws/lambda/uploadFunc"
  }
}
(END)
  "TracingConfig": {
    "Mode": "PassThrough"
  },
  "RevisionId": "cb4a2a13-706e-4556-b03d-36c28691011c",
  "State": "Active",
  "LastUpdateStatus": "InProgress",
  "LastUpdateStatusReason": "The function is being created.",
  "LastUpdateStatusReasonCode": "Creating",
  "PackageType": "Zip",
  "Architectures": [
    "x86_64"
  ],
  "EphemeralStorage": {
    "Size": 512
  },
  "SnapStart": {
    "ApplyOn": "None",
    "OptimizationStatus": "Off"
  },
  "RuntimeVersionConfig": {
    "RuntimeVersionArn": "arn:aws:lambda:us-east-1::runtime:8eeff65f6809a3ce81507fe733fe09b835899b99481ba22fd75b5a7338290ec1"
  },
  "LoggingConfig": {
    "LogFormat": "Text",
    "LogGroup": "/aws/lambda/uploadFunc"
  }
}
(END)
{acBook-Pro-3:AWS_Serverless_File_Uploader $ > > > > 
  "StatusCode": 200,
  "ExecutedVersion": "$LATEST"
}
MacBook-Pro-3:AWS_Serverless_File_Uploader $ 
```

Notes:

- Some commands returned "command not found" because `pip`, `aws`, or `awslocal` weren't available in the shell environment when the session started.
- The transcript captures the successful creation of bucket `demo-bucket`, IAM role `lambda-role`, and Lambda `uploadFunc` in LocalStack.

