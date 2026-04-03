📦 kubernetes-ml-ai-engineer
📄 README.md
# 🚀 Kubernetes for ML/AI Engineers

![Kubernetes](https://img.shields.io/badge/Kubernetes-Production-blue)
![ML](https://img.shields.io/badge/ML-Deployment-green)
![License](https://img.shields.io/badge/license-MIT-orange)

---

## 🎯 Goal
Learn Kubernetes from **zero → advanced** with **real ML/AI use cases**:
- Model deployment
- Scaling inference
- Distributed training
- Pipelines
- Production-grade infra

---

## 🧠 Learning Roadmap


Basics → Core → Scaling → Networking → ML Deployment
→ Model Serving → Workflows → Distributed Training
→ Monitoring → Production


---

## 🏗️ Architecture (Simplified)

    ┌──────────────┐
    │   User/API   │
    └──────┬───────┘
           │
    ┌──────▼───────┐
    │  Ingress     │
    └──────┬───────┘
           │
    ┌──────▼───────┐
    │ Service      │
    └──────┬───────┘
           │
    ┌──────▼────────────┐
    │ Deployment (Pods) │
    └──────┬────────────┘
           │
    ┌──────▼───────┐
    │ Model + API  │
    └──────────────┘

---

## ⚙️ Prerequisites
- Docker
- kubectl
- Minikube / Kind

---

## 🛠️ Setup

### Start Cluster (Minikube)
```bash
minikube start
kubectl get nodes
Using Kind
kind create cluster
kubectl get nodes
```

#### 📂Sections
Folder	Topic
- 01-basics	Pods, Deployments
- 02-core-concepts	ConfigMaps, Secrets
- 03-scaling	HPA
- 05-ml-deployment	FastAPI ML
- 08-distributed-training	PyTorch/TensorFlow

#### 🔥 Real ML Use Cases
- Deploy ML model API (FastAPI)
- Autoscale inference
- Batch jobs
- Distributed GPU training
- Canary deployments

#### ⚠️ Common Mistakes
- Forgetting resource limits
- Not using namespaces
- Hardcoding secrets

#### 💡 Interview Questions
- Difference between Deployment & StatefulSet?
- How does HPA work?
- How to deploy ML model on Kubernetes?

#### 🧰 Debug Commands
```bash
kubectl get pods
kubectl describe pod <pod>
kubectl logs <pod>
kubectl delete pod <pod>
```

---

## 📄 .gitignore
```gitignore
__pycache__/
*.pyc
.env
*.log
venv/
```

## 📄 requirements.txt
```
fastapi
uvicorn
scikit-learn
numpy

```
## 📁 01-basics
📄 01-basics/README.md
# 📦 Kubernetes Basics

## Commands

```bash
kubectl apply -f pods.yaml
kubectl get pods
kubectl describe pod <pod>
kubectl logs <pod>
kubectl delete -f pods.yaml
```
---

## 📄 01-basics/pods.yaml
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: basic-pod
spec:
  containers:
    - name: nginx
      image: nginx
      ports:
        - containerPort: 80
```

## 📄 01-basics/deployments.yaml
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  replicas: 2
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
        - name: nginx
          image: nginx
          resources:
            limits:
              cpu: "500m"
              memory: "256Mi"
```              
## 📄 01-basics/services.yaml
```yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
spec:
  type: NodePort
  selector:
    app: nginx
  ports:
    - port: 80
      targetPort: 80
      nodePort: 30007
```

## 📄 01-basics/kubectl-commands.md
# Useful Commands
```bash
kubectl get pods
kubectl get svc
kubectl describe pod <pod>
kubectl logs <pod>
kubectl delete pod <pod>
```

## 📁 02-core-concepts
## 📄 namespaces.yaml
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: ml-namespace
```

## 📄 configmaps.yaml
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  MODEL_NAME: "iris-model"
```

## 📄 secrets.yaml
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-secret
type: Opaque
data:
  API_KEY: dGVzdA==  # base64 encoded
```

## 📄 volumes.yaml
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: volume-pod
spec:
  containers:
    - name: app
      image: busybox
      command: ["sleep", "3600"]
      volumeMounts:
        - mountPath: "/data"
          name: storage
  volumes:
    - name: storage
      emptyDir: {}
```      
## 📄 02-core-concepts/README.md
# ⚙️ Core Concepts
```bash
kubectl apply -f namespaces.yaml
kubectl get namespaces
```

## 📁 03-scaling
## 📄 hpa.yaml
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: ml-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: nginx-deployment
  minReplicas: 1
  maxReplicas: 5
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 50
```

## 📄 vpa.md
Vertical Pod Autoscaler adjusts CPU/memory automatically.

## 📁 05-ml-deployment
## 📄 fastapi-app/app.py
```python
from fastapi import FastAPI
import numpy as np

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "ML Model API"}

@app.post("/predict")
def predict(data: list):
    arr = np.array(data)
    return {"prediction": arr.mean()}

```    
## 📄 fastapi-app/Dockerfile
```Dockerfile
FROM python:3.10

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 📄 fastapi-app/requirements.txt
```
fastapi
uvicorn
numpy
```

## 📄 deployment.yaml
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ml-api
spec:
  replicas: 2
  selector:
    matchLabels:
      app: ml-api
  template:
    metadata:
      labels:
        app: ml-api
    spec:
      containers:
        - name: ml-api
          image: ml-api:latest
          ports:
            - containerPort: 8000
```            
## 📄 service.yaml
```yaml
apiVersion: v1
kind: Service
metadata:
  name: ml-service
spec:
  type: NodePort
  selector:
    app: ml-api
  ports:
    - port: 80
      targetPort: 8000
      nodePort: 30008
```

## 📁 08-distributed-training
## 📄 pytorch-job.yaml
```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: pytorch-training
spec:
  template:
    spec:
      containers:
        - name: trainer
          image: pytorch/pytorch
          command: ["python", "train.py"]
      restartPolicy: Never
```

## 📄 tf-job.yaml
```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: tf-training
spec:
  template:
    spec:
      containers:
        - name: trainer
          image: tensorflow/tensorflow
          command: ["python", "train.py"]
      restartPolicy: Never
```      
## 📁 09-monitoring
## 📄 prometheus.yaml
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: prometheus
spec:
  containers:
    - name: prometheus
      image: prom/prometheus
```

### 📄 grafana.yaml
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: grafana
spec:
  containers:
    - name: grafana
      image: grafana/grafana
```

## 📁 10-production
## 📄 helm/README.md
# Helm

** Helm helps package Kubernetes apps.
```bash
helm create ml-chart
helm install ml-app ./ml-chart
```

## 📄 ci-cd/github-actions.yaml
```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build Docker Image
        run: docker build -t ml-api .
```        
## 📁 assets
## 📄 architecture-diagrams.md
# Architecture Diagrams

** ML Deployment Flow:

User → Ingress → Service → Pods → Model

## 🚀 FINAL NOTES
** Deploy Full ML App
```bash
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl get pods
Debug
kubectl logs <pod>
kubectl describe pod <pod>
```