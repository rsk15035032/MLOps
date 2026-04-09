# 📘 End-to-End AWS for AI/ML Engineers: Beanstalk, Lambda, SageMaker & Bedrock

![AWS](https://img.shields.io/badge/AWS-232F3E?logo=amazonaws&logoColor=white&style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white&style=for-the-badge)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white&style=for-the-badge)
![SageMaker](https://img.shields.io/badge/Amazon%20SageMaker-FF9900?logo=amazonsagemaker&logoColor=white&style=for-the-badge)

**Master production ML deployment on AWS — from traditional models to GenAI — with real, copy-paste-ready code.**

---

## 🎯 Objectives

By the end of this repository, you will be able to:

- **🚀 Deploy** full ML web applications using **AWS Elastic Beanstalk**
- **⚡ Build** serverless ML inference APIs with **AWS Lambda + API Gateway**
- **🧠 Train, tune, and deploy** models end-to-end with **Amazon SageMaker**
- **🤖 Build** production GenAI applications using **Amazon Bedrock** (Claude, embeddings, RAG)
- **🏗️ Architect** complete production ML systems on AWS
- Understand **when to choose** each service and how to combine them

**Real-world ready.** FAANG-level depth. Zero fluff.

---

## 🌟 Introduction

This repository is your complete hands-on guide to deploying AI/ML workloads on AWS — from simple model serving to sophisticated GenAI applications.

### Why AWS for AI/ML?
- **Managed services** that remove infrastructure headaches
- **Seamless integration** between services
- **Pay-as-you-go** with massive cost optimization options
- **Enterprise-grade** security, scaling, and monitoring
- **Bedrock + SageMaker** gives you both foundation models and full custom ML control

### Real-World Use Cases
- Customer churn prediction API (Beanstalk/Lambda)
- Real-time fraud detection (SageMaker endpoints)
- Intelligent document Q&A system (Bedrock RAG)
- AI Resume Analyzer or Product Recommendation Engine (End-to-End)

**This repo teaches you exactly how production teams at scale build and ship ML systems.**

---
## 🏗️ Architecture Overview (Production)

```
                ┌────────────────────┐
                │   Frontend (UI)    │
                └─────────┬──────────┘
                          │
                          ▼
                ┌────────────────────┐
                │   API Gateway      │
                └─────────┬──────────┘
                          │
        ┌─────────────────┼─────────────────┐
        ▼                 ▼                 ▼
 ┌────────────┐   ┌──────────────┐   ┌──────────────┐
 │  Lambda    │   │  Beanstalk   │   │ StepFunctions│
 │ (Inference)│   │  (Backend)   │   │ (Pipelines)  │
 └────┬───────┘   └──────┬───────┘   └──────┬───────┘
      │                  │                  │
      ▼                  ▼                  ▼
 ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
 │ SageMaker    │  │   Bedrock    │  │   S3 / DB    │
 │ (ML Models)  │  │ (LLMs)       │  │ Storage      │
 └──────────────┘  └──────────────┘  └──────────────┘
                          │
                          ▼
                   ┌────────────┐
                   │ Response   │
                   └────────────┘
```

---

Typical End-to-End Flow (Section 5):

* User submits request via Frontend
* API Gateway routes to Lambda
* Lambda calls SageMaker endpoint or Bedrock
* Results stored in S3 + returned with low latency
* Everything monitored via CloudWatch

--- 

## 📂 Project Structure

```
.
├── 01-elastic-beanstalk/          # Traditional web ML apps
│   ├── app.py
│   ├── model.pkl
│   ├── requirements.txt
│   └── Procfile
├── 02-aws-lambda/                 # Serverless inference
│   ├── lambda_function.py
│   └── deploy.sh
├── 03-sagemaker/                  # Full ML lifecycle
│   ├── train.py
│   ├── inference.py
│   └── pipeline.py
├── 04-bedrock/                    # Generative AI
│   ├── rag.py
│   ├── embeddings.py
│   └── chatbot.py
├── 05-end-to-end-project/         # Production AI Resume Analyzer
│   ├── architecture.md
│   ├── lambda/
│   ├── frontend/
│   └── infra/
├── README.md
└── .github/workflows/             # Bonus CI/CD
```
---
## ⚙️ Prerequisites
1. AWS Account & IAM

* Create a free AWS account
* Create an IAM user with AdministratorAccess (for learning) or least-privilege roles in production

---

## 2. Install Tools
# AWS CLI
```bash
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# Configure
aws configure
# Enter Access Key, Secret Key, region (us-east-1), output (json)

# Verify
aws sts get-caller-identity
```
---
## 3. Other Requirements

* Python 3.10+
* pip install fastapi uvicorn scikit-learn boto3 joblib
* Docker (optional but recommended)
* Git
---
# ☁️ SECTION 1: AWS Elastic Beanstalk — Easy Web ML Apps
## What is Elastic Beanstalk?
Platform-as-a-Service (PaaS) that handles capacity provisioning, load balancing, auto-scaling, and monitoring for you.

## When to use in ML?

- Full web applications with UI + backend
- Moderate traffic traditional ML models
- When you want "deploy and forget" simplicity

## Hands-on: Deploy FastAPI + Scikit-Learn Model
### 01-elastic-beanstalk/app.py

```python
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

app = FastAPI(title="Iris Prediction API")

model = joblib.load("model.pkl")

class IrisFeatures(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

@app.post("/predict")
def predict(features: IrisFeatures):
    data = np.array([[features.sepal_length, features.sepal_width,
                      features.petal_length, features.petal_width]])
    prediction = model.predict(data)
    return {"prediction": int(prediction[0])}

@app.get("/")
def home():
    return {"message": "Iris ML API running on Beanstalk!"}
```
--- 
### requirements.txt
```
fastapi
uvicorn[standard]
scikit-learn
joblib
```
---
### Procfile
```
web: uvicorn app:app --host 0.0.0.0 --port 8080
```
---
## Deployment Commands
```bash
cd 01-elastic-beanstalk

# Initialize
eb init -p python-3.11 my-iris-app --region us-east-1

# Create environment
eb create my-iris-env

# Deploy
eb deploy

# Open in browser
eb open
```
- 🚀 Test it: POST to /predict with JSON body.
- 💡 Tip: Add .ebextensions/ for custom Nginx or environment variables.

# ⚡ SECTION 2: AWS Lambda — Serverless ML Inference
## Why Lambda for ML?
Event-driven, auto-scales to zero, pay-per-millisecond. Perfect for sporadic inference.
Challenges & Solutions:

* Cold starts → Use Provisioned Concurrency or SnapStart
* Package size → Download model from S3 at runtime (recommended)

- Hands-on: Serverless Prediction API
## 02-aws-lambda/lambda_function.py
```python
Pythonimport json
import boto3
import joblib
import numpy as np
from io import BytesIO

s3 = boto3.client('s3')

def load_model():
    # Download model from S3 on first invocation (cached afterward)
    response = s3.get_object(Bucket='your-bucket', Key='model.pkl')
    model_data = response['Body'].read()
    model = joblib.load(BytesIO(model_data))
    return model

model = None

def lambda_handler(event, context):
    global model
    if model is None:
        model = load_model()
    
    body = json.loads(event['body'])
    features = np.array([[
        body['sepal_length'], body['sepal_width'],
        body['petal_length'], body['petal_width']
    ]])
    
    prediction = model.predict(features)[0]
    
    return {
        'statusCode': 200,
        'body': json.dumps({'prediction': int(prediction)})
    }
```    
## Deployment
Bash cd 02-aws-lambda

# Zip (or use AWS SAM for complex apps)
- zip function.zip lambda_function.py
```python
aws lambda create-function \
  --function-name ml-inference \
  --runtime python3.11 \
  --role arn:aws:iam::...:role/lambda-role \
  --handler lambda_function.lambda_handler \
  --zip-file fileb://function.zip \
  --memory-size 1024 \
  --timeout 30
``` 
* Integrate with API Gateway (console or CDK) for REST endpoint.
* ⚠️ Optimization: Use Lambda Layers for large dependencies or EFS for bigger models.

## 🧠 SECTION 3: AWS SageMaker — Full ML Lifecycle
SageMaker is the complete platform: notebooks, training jobs, hyperparameter tuning, model registry, endpoints, and pipelines.
Hands-on: Train & Deploy Scikit-Learn Model

## 03-sagemaker/train.py (Script Mode)
```python
Pythonimport argparse
import joblib
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris

def model_fn(model_dir):
    return joblib.load(os.path.join(model_dir, "model.joblib"))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # Add arguments for hyperparameters...
    
    iris = load_iris()
    X, y = iris.data, iris.target
    
    clf = RandomForestClassifier(n_estimators=100)
    clf.fit(X, y)
    
    joblib.dump(clf, "/opt/ml/model/model.joblib")
Training & Deployment (via SageMaker Python SDK)
Pythonfrom sagemaker.sklearn.estimator import SKLearn
from sagemaker import get_execution_role

role = get_execution_role()

sklearn_estimator = SKLearn(
    entry_point='train.py',
    role=role,
    instance_count=1,
    instance_type='ml.m5.large',
    framework_version='1.2-1',
    py_version='py3'
)

sklearn_estimator.fit({'train': 's3://your-bucket/data/'})

# Deploy
predictor = sklearn_estimator.deploy(
    initial_instance_count=1,
    instance_type='ml.t2.medium'
)
```
Hyperparameter Tuning: Use HyperparameterTuner with multiple jobs.
💰 Cost Tip: Use Managed Spot Training (up to 90% savings) and Serverless Inference endpoints.

## 🤖 SECTION 4: AWS Bedrock — Generative AI Made Simple
Amazon Bedrock gives you access to top foundation models (Claude 3, Llama, Titan, etc.) via API — no infrastructure to manage.
Hands-on: Invoke Claude
## 04-bedrock/chatbot.py
```python
Pythonimport boto3
import json

bedrock = boto3.client(service_name='bedrock-runtime', region_name='us-east-1')

def invoke_claude(prompt):
    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 512,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "top_p": 0.9
    })
    
    response = bedrock.invoke_model(
        modelId="anthropic.claude-3-haiku-20240307-v1:0",
        body=body,
        contentType="application/json",
        accept="application/json"
    )
    
    response_body = json.loads(response.get('body').read())
    return response_body['content'][0]['text']

print(invoke_claude("Explain AWS Bedrock in one paragraph."))
```
* RAG Example (rag.py)
* Use Titan Embeddings + Amazon OpenSearch or PGVector for retrieval.
* Key Steps:
```
Generate embeddings with bedrock-runtime.invoke_model (Titan Embeddings)
Store in vector DB
Retrieve relevant chunks → Augment prompt → Call Claude
```
* Prompt Engineering Tip:
textYou are a helpful assistant. Use only the following context to answer:
```
{context}

Question: {question}
Answer:
```
## 🔥 SECTION 5: End-to-End Project — AI Resume Analyzer
Project Goal: Upload resume → Extract skills, experience, and get AI-powered matching score against job description.
Architecture

* Frontend: React/Vite (in frontend/)
* Backend: API Gateway → Lambda
* GenAI: Amazon Bedrock (Claude 3 Sonnet)
* Storage: S3 + DynamoDB
* Optional: SageMaker for custom skill extraction model

## Full Flow:
```
User uploads PDF resume
Lambda triggers Textract or Bedrock multimodal
RAG retrieves job requirements
Claude analyzes match + suggests improvements
Results stored and returned

Deployment: Use AWS CDK or SAM for infrastructure-as-code (see infra/).
Detailed architecture and steps are in 05-end-to-end-project/architecture.md.
```

## 💰 Cost Optimization Tips

* Lambda: Use Graviton2, provisioned concurrency only when needed, download models from S3
* SageMaker: Spot instances for training (up to 90% off), Serverless Inference, Savings Plans
* Bedrock: Choose right model (Haiku for speed/cost, Sonnet for quality), Prompt Caching, * * *
* Intelligent Prompt Routing
* Beanstalk: Right-size instances, use Reserved Instances
* General: Monitor with CloudWatch + Budgets, delete idle resources, use S3 Intelligent-Tiering

Rule of thumb: Start with Bedrock/Lambda for prototypes → Move to SageMaker for heavy customization.

## 🔐 Security Best Practices

* IAM: Least privilege + service-linked roles
* Secrets: Use AWS Secrets Manager or SSM Parameter Store
* VPC: Run sensitive workloads in private subnets
* Encryption: Enable at-rest and in-transit everywhere
* Model Access: Use Bedrock IAM policies to restrict models
* Audit: Enable CloudTrail + GuardDuty


## 📚 Learning Roadmap
```
Beginner

Complete Sections 1 & 2
Deploy your first API

Intermediate

Sections 3 & 4
Build RAG chatbot

Advanced

Section 5 full project
Add monitoring + CI/CD

Production

Multi-account setup, Blue/Green deployments, Model Monitoring, A/B testing
```

## 🛠️ Bonus Topics

* CI/CD: GitHub Actions workflow included (build → test → deploy to Beanstalk/Lambda)
* Docker: Containerize everything for consistency
* Monitoring: CloudWatch dashboards + SageMaker Model Monitor
* Orchestration: Step Functions for complex pipelines
* MLOps: Use SageMaker Pipelines + Model Registry


💡 Pro Tip: Use AWS Cloud9 or SageMaker Studio for a cloud-based dev environment.

⭐ Star this repo if it helped you!
