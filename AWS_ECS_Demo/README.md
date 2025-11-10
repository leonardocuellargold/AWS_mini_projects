# Containerized Microservice (ECR + ECS)

## Goal
------

Deploy a simple containerized web microservice to a mock ECS cluster in LocalStack, storing the image in ECR.

This demonstrates how container workloads are packaged, pushed, and orchestrated — useful for interview demonstrations of containerization and orchestration.

## Quick structure
---------------

- `app.py` — tiny Flask microservice
- `Dockerfile` — container build
- `requirements.txt` — Python deps
- `task-def.json` — ECS Task Definition (points to LocalStack ECR image)

1) Create working folder (if you haven't):

	 mkdir AWS_ECS_Demo
	 cd AWS_ECS_Demo

2) Microservice (`app.py`)

```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
		return 'Hello from ECS LocalStack container!'

if __name__ == '__main__':
		app.run(host='0.0.0.0', port=8080)
```

`requirements.txt`

```
flask==3.0.3
```

3) Dockerfile

```
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app.py .
CMD ["python", "app.py"]
```

Build locally:

```
docker build -t ecs-demo:latest .
```

Optional test run:

```
docker run -p 8080:8080 ecs-demo:latest
# visit http://localhost:8080 and expect: Hello from ECS LocalStack container!
```

4) Create repository in LocalStack ECR (example)

```
aws --endpoint-url=http://localhost:4566 ecr create-repository \
	--repository-name ecs-demo-repo
```

Sample `aws` output:

```
{
		"repository": {
				"repositoryArn": "arn:aws:ecr:us-east-1:000000000000:repository/ecs-demo-repo",
				"registryId": "000000000000",
				"repositoryName": "ecs-demo-repo",
				"repositoryUri": "localhost:4566/ecs-demo-repo"
		}
}
```

5) Tag & push the image to LocalStack ECR

```
docker tag ecs-demo:latest localhost:4566/ecs-demo-repo:latest
docker push localhost:4566/ecs-demo-repo:latest
```

Example push output:

```
The push refers to repository [localhost:4566/ecs-demo-repo]
abcdef123456: Pushed
latest: digest: sha256:xxxxxxxxxxxx size: 1234
```

6) Create ECS cluster & register task definition (LocalStack)

Create cluster:

```
aws --endpoint-url=http://localhost:4566 ecs create-cluster --cluster-name ecs-demo-cluster
```

Response:

```
{
	"cluster": {
		"clusterArn": "arn:aws:ecs:us-east-1:000000000000:cluster/ecs-demo-cluster",
		"clusterName": "ecs-demo-cluster",
		"status": "ACTIVE"
	}
}
```

`task-def.json` (already included):

```json
{
	"family": "ecs-demo-task",
	"networkMode": "bridge",
	"containerDefinitions": [
		{
			"name": "ecs-demo-container",
			"image": "localhost:4566/ecs-demo-repo:latest",
			"memory": 128,
			"cpu": 64,
			"essential": true,
			"portMappings": [
				{ "containerPort": 8080, "hostPort": 8080 }
			]
		}
	]
}
```

Register task definition:

```
aws --endpoint-url=http://localhost:4566 ecs register-task-definition --cli-input-json file://task-def.json
```

Output:

```
{
	"taskDefinition": {
		"taskDefinitionArn": "arn:aws:ecs:us-east-1:000000000000:task-definition/ecs-demo-task:1",
		"family": "ecs-demo-task",
		"revision": 1
	}
}
```

Run the task:

```
aws --endpoint-url=http://localhost:4566 ecs run-task \
	--cluster ecs-demo-cluster \
	--task-definition ecs-demo-task
```

`run-task` output (LocalStack):

```
{
	"tasks": [
		{
			"taskArn": "arn:aws:ecs:us-east-1:000000000000:task/ecs-demo-task/12345678",
			"lastStatus": "RUNNING",
			"containers": [
				{
					"name": "ecs-demo-container",
					"lastStatus": "RUNNING"
				}
			]
		}
	],
	"failures": []
}
```

## What to expect locally
-----------------------

- With LocalStack running and ECS mocked, the `run-task` call should start a container that maps host port 8080 to container port 8080. Curling `http://localhost:8080` should return the Flask response above.

## Lessons learned
-----------------------

- Containers encapsulate runtime dependencies and make deployments reproducible.
- ECR acts as an immutable artifact store for container images.
- ECS (task definitions) declares how containers should run (CPU/memory/ports).
- LocalStack is a great offline way to demonstrate the entire workflow without real AWS charges.


