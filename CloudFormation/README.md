# AWS CloudFormation Demo — Serverless File Uploader (LocalStack)

Excellent, Leonardo — you're following the right approach for an interview-friendly Infrastructure-as-Code demo.

This small, local project shows how to codify an S3 + Lambda serverless workflow using a single `template.yaml` CloudFormation template and deploy it to LocalStack for repeatable, auditable provisioning.

## Goal

Deploy a simple serverless architecture (S3 bucket + Lambda function) using CloudFormation running in LocalStack. The Lambda writes a test object to the S3 bucket; the template demonstrates declarative, repeatable infra provisioning.

## Files added

- `template.yaml` — CloudFormation template that creates an S3 bucket (`demo-stack-bucket`) and a Lambda (`demo-lambda`) whose inline code uploads a file to the bucket.

## Prerequisites

- LocalStack installed and running locally (default edge port 4566)
- AWS CLI configured (any profile) — we'll target LocalStack with `--endpoint-url`

## Template (already added)

The template is in `template.yaml` and contains:

- AWSTemplateFormatVersion: 2010-09-09
- An S3 bucket resource: `DemoBucket` with name `demo-stack-bucket`
- A Lambda function resource: `DemoFunction` named `demo-lambda` with inline Python code that uploads `cloudformation-upload.txt` to the bucket.

> Note: the template uses an IAM role ARN `arn:aws:iam::000000000000:role/lambda-role`. LocalStack does not enforce IAM by default for local testing; for real AWS deployments you must supply a valid role with the correct trust/permission policy.

## Deploy to LocalStack

1. Make sure LocalStack is running (for example via Docker Compose or `localstack start`).

2. Create the stack using the AWS CLI pointed at LocalStack:

```bash
aws --endpoint-url=http://localhost:4566 cloudformation create-stack \
  --stack-name serverless-demo-stack \
  --template-body file://template.yaml
```

3. Wait a few seconds then confirm the stack status:

```bash
aws --endpoint-url=http://localhost:4566 cloudformation describe-stacks \
  --stack-name serverless-demo-stack
```

You should see `StackStatus: CREATE_COMPLETE` and the resources listed.

## Optional check — invoke the Lambda and validate S3

1. Invoke the Lambda (LocalStack uses the function name in this template):

```bash
aws --endpoint-url=http://localhost:4566 lambda invoke \
  --function-name demo-lambda \
  --cli-binary-format raw-in-base64-out \
  --payload '{}' response.json

cat response.json
```

2. List the bucket contents:

```bash
aws --endpoint-url=http://localhost:4566 s3 ls s3://demo-stack-bucket
```

If `cloudformation-upload.txt` appears, the Lambda successfully uploaded the object.

## Lessons learned

- IaC codifies infrastructure: the template describes the full environment, making deployments consistent across dev, test, and prod.
- CloudFormation handles dependencies: S3 exists before Lambda writes to it, and CloudFormation builds resources in the correct order automatically.
- Error handling & rollback: if a resource fails, CloudFormation rolls back by default — essential for enterprise-grade deployments.
- Portable skill: these IaC concepts map to other providers (Bicep, Deployment Manager, Terraform).


## Next steps / variations

- Add an `AWS::IAM::Role` resource to the template and reference it from the Lambda `Role` property to make the template fully self-contained.
- Replace inline `ZipFile` with an S3-backed Lambda deployment or a packaging step for larger functions.
- Add unit tests for the template (cfn-lint) or integrate with CI that runs LocalStack to validate stack creation as part of a pipeline.
