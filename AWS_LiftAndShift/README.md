# **AWS Lift-and-Shift Simulation (LocalStack)**

This mini-project simulates the early stages of a **lift-and-shift migration** to AWS. The goal was to model a simple **application tier (EC2)** and **database tier (RDS)** running locally on **LocalStack** to understand how compute, database, IAM, and tagging all fit together in a cloud modernization workflow.

---

## **Overview**

The exercise represents a classic migration pattern where an on-prem monolithic system is moved into the cloud with minimal refactoring. The environment was built entirely in **LocalStack** (Docker) using the **AWS CLI**.

- **Compute Layer** – simulated EC2 instance (application server)
- **Database Layer** – RDS MySQL instance
- **Security & Governance** – IAM role for EC2, environment and project tagging

---

## **Implementation Summary**

1. **IAM Setup**
    - Created an IAM role (app-ec2-role) with an assume-role policy allowing ec2.amazonaws.com to assume it.
    - Attached an inline policy granting access to logs:* and s3:*, modeling what a typical app server would need for logging and storage.
2. **EC2 Simulation**
    - Attempted to create a mock EC2 instance.
    - Encountered multiple InvalidAMIID.NotFound and InternalError messages—expected behavior because LocalStack does not maintain a library of AMIs.
    - Registered a dummy AMI (ami-2eeaba62) to bypass validation and successfully invoked a placeholder run-instances call.
3. **RDS Simulation**
        Created an RDS MySQL instance (app-db) using:

```bash
aws --endpoint-url=http://localhost:4566 rds create-db-instance \
    --db-instance-identifier app-db \
    --db-instance-class db.t3.micro \
    --engine mysql \
    --master-username admin \
    --master-user-password [password] \
    --allocated-storage 20
```
- Verified output showed realistic fields: endpoint, storage, security groups, parameter groups, and tags.

2. **Tagging & Governance**
    - Applied tags for Name, Environment, and Project.
    - Discussed how tagging connects to cost allocation, automation, and environment separation (dev/test/prod).

---

# AWS Lift-and-Shift Simulation (LocalStack)

This mini-project simulates the early stages of a lift-and-shift migration to AWS. The goal was to model a simple application tier (EC2) and database tier (RDS) running locally on LocalStack to understand how compute, database, IAM, and tagging all fit together in a cloud modernization workflow.

---

## Overview

The exercise represents a classic migration pattern where an on-prem monolithic system is moved into the cloud with minimal refactoring. The environment was built entirely in LocalStack (Docker) using the AWS CLI.

- Compute Layer – simulated EC2 instance (application server)
- Database Layer – RDS MySQL instance
- Security & Governance – IAM role for EC2, environment and project tagging

---

## Implementation Summary

1. IAM Setup
    - Created an IAM role (app-ec2-role) with an assume-role policy allowing `ec2.amazonaws.com` to assume it.
    - Attached an inline policy granting access to `logs:*` and `s3:*`, modeling what a typical app server would need for logging and storage.

2. EC2 Simulation
    - Attempted to create a mock EC2 instance.
    - Encountered multiple `InvalidAMIID.NotFound` and `InternalError` messages — expected behavior because LocalStack does not maintain a library of AMIs.
    - Registered a dummy AMI (ami-2eeaba62) to bypass validation and successfully invoked a placeholder `run-instances` call.

3. RDS Simulation
    - Created an RDS MySQL instance (app-db) using the following command (LocalStack endpoint shown as example):

```bash
aws --endpoint-url=http://localhost:4566 rds create-db-instance \
  --db-instance-identifier app-db \
  --db-instance-class db.t3.micro \
  --engine mysql \
  --master-username admin \
  --master-user-password [password] \
  --allocated-storage 20
```

    - Verified output showed realistic fields: endpoint, storage, security groups, parameter groups, and tags.

4. Tagging & Governance
    - Applied tags for Name, Environment, and Project.
    - Discussed how tagging connects to cost allocation, automation, and environment separation (dev/test/prod).

---

## Lessons Learned

- IAM is foundational: every AWS resource that interacts with others requires an appropriate role and trust policy. Defining those correctly prevents permission and security issues later.
- AMIs are prerequisites for EC2: even in LocalStack, an EC2 instance cannot start without a registered AMI.
- LocalStack limitations mirror real AWS complexity: EC2 mocking is limited, but the experience reinforces the need to plan for dependencies, retry logic, and graceful failure when automating infrastructure.
- RDS output provides deep insight: even locally, the JSON response mimics real metadata fields—useful for understanding backup windows, parameter groups, and maintenance windows that appear in production RDS environments.
- Lift-and-shift ≠ done: standing up EC2 + RDS is the first modernization step. True transformation requires breaking monoliths into microservices, adopting serverless or container-based architectures, and using IaC for repeatability.

## Next Steps

- Automate deployment using CloudFormation or Terraform.
- Connect RDS output to a small Lambda or Python app to represent a complete application tier.
- Experiment with ECS or EKS as a modernization step beyond lift-and-shift.

---

## Local terminal outputs (sanitized)

Note: personal machine names and user paths have been removed or replaced with generic placeholders to avoid exposing local identifiers.

- Directory listing for the `AWS_LiftAndShift` folder:

```text
ec2-trust-policy.json
README.md
```

- `ec2-trust-policy.json` (contents):

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": { "Service": "ec2.amazonaws.com" },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

- Git information (captured locally):

```text
Branch: main
```

These outputs were captured from the local repository and sanitized to remove any personal or machine-specific identifiers before being added here.
