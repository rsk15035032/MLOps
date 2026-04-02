# 📦 docker-ml-ai-engineer

A complete, production-ready repository to learn Docker from **basic → advanced** with **real ML/AI use cases**.

---

## 🎯 Overview

This repository is designed for:

* ML Engineers
* AI Engineers
* Data Scientists moving to production

You will learn:

* Docker fundamentals
* Containerizing ML models
* Multi-container systems
* Model deployment
* Optimization & scaling
* Intro to Kubernetes

---

## 🧭 Learning Roadmap

1. Basics
2. Dockerfiles
3. Images & Containers
4. Volumes & Networking
5. Docker Compose
6. ML Projects
7. Model Deployment
8. Optimization
9. Kubernetes Intro

---

## ⚙️ Prerequisites

* Python 3.9+
* Basic Linux commands
* Git

---

## 🚀 How to Use

```bash
git clone https://github.com/yourname/docker-ml-ai-engineer.git
cd docker-ml-ai-engineer
```

Follow folders in order.

---

## 🤝 Contribution

PRs are welcome!

---

# 📁 FULL REPOSITORY STRUCTURE

```
docker-ml-ai-engineer/
│── README.md
│── .gitignore
│── cheatsheet/docker_commands.md
│
│── 01_basics/
│   ├── README.md
│
│── 02_dockerfiles/
│   ├── README.md
│   ├── app.py
│   ├── Dockerfile
│
│── 03_images_containers/
│   ├── README.md
│
│── 04_volumes_networking/
│   ├── README.md
│
│── 05_docker_compose/
│   ├── README.md
│   ├── docker-compose.yml
│   ├── app/
│       ├── main.py
│       ├── requirements.txt
│
│── 06_ml_projects/
│   ├── sklearn_model/
│   │   ├── model.py
│   │   ├── requirements.txt
│   │   ├── Dockerfile
│   ├── pytorch_training/
│   │   ├── train.py
│   │   ├── requirements.txt
│   │   ├── Dockerfile
│
│── 07_model_deployment/
│   ├── app.py
│   ├── model.pkl
│   ├── Dockerfile
│   ├── requirements.txt
│
│── 08_optimization/
│   ├── Dockerfile
│   ├── .dockerignore
│   ├── README.md
│
│── 09_kubernetes_intro/
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── README.md
│
│── projects/
│   ├── ml_api_project/
│   ├── data_pipeline/
│   ├── inference_service/
```

---

# ============================

# 01_basics/README.md

# ============================

## What is Docker?

Docker is a containerization platform that packages applications with dependencies.

## Install (Ubuntu)

```bash
sudo apt update
sudo apt install docker.io
sudo systemctl start docker
sudo systemctl enable docker
```

## Basic Commands

```bash
docker run hello-world
```

### Expected Output

```
Hello from Docker!
```

```bash
docker ps
```

```bash
docker images
```

---

# ============================

# 02_dockerfiles/

# ============================

## app.py

```python
print("Hello from Docker ML App")
```

## Dockerfile

```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY app.py .
CMD ["python", "app.py"]
```

## Commands

```bash
docker build -t ml-basic .
docker run ml-basic
```

---

# ============================

# 03_images_containers/README.md

# ============================

## Build Image

```bash
docker build -t myapp .
```

## Tag Image

```bash
docker tag myapp myapp:v1
```

## Run Container

```bash
docker run -d myapp
```

---

# ============================

# 04_volumes_networking/README.md

# ============================

## Volumes (Important for ML)

```bash
docker run -v $(pwd)/data:/app/data myapp
```

## Networking

```bash
docker network create mynet
```

---

# ============================

# 05_docker_compose/

# ============================

## docker-compose.yml

```yaml
version: '3.9'
services:
  api:
    build: ./app
    ports:
      - "8000:8000"
  redis:
    image: redis
```

## app/main.py

```python
from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def read_root():
    return {"msg": "Hello"}
```

## requirements.txt

```
fastapi
uvicorn
```

## Run

```bash
docker-compose up
```

---

# ============================

# 06_ml_projects/

# ============================

## sklearn_model/model.py

```python
from sklearn.linear_model import LinearRegression
import numpy as np

X = np.array([[1],[2],[3]])
y = np.array([2,4,6])
model = LinearRegression().fit(X,y)
print(model.predict([[5]]))
```

## requirements.txt

```
scikit-learn
numpy
```

## Dockerfile

```dockerfile
FROM python:3.10
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "model.py"]
```

---

## PyTorch Training

## train.py

```python
import torch
x = torch.tensor([1.0,2.0,3.0])
print(x * 2)
```

## Dockerfile (GPU Support)

```dockerfile
FROM nvidia/cuda:12.1.0-runtime-ubuntu22.04
WORKDIR /app
COPY . .
RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip3 install torch
CMD ["python3", "train.py"]
```

---

# ============================

# 07_model_deployment/

# ============================

## app.py

```python
from fastapi import FastAPI
import pickle

app = FastAPI()
model = pickle.load(open("model.pkl", "rb"))

@app.get("/predict")
def predict(x: float):
    return {"result": model.predict([[x]]).tolist()}
```

## Dockerfile

```dockerfile
FROM python:3.10
WORKDIR /app
COPY . .
RUN pip install fastapi uvicorn scikit-learn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

# ============================

# 08_optimization/

# ============================

## Multi-stage Dockerfile

```dockerfile
FROM python:3.10 as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM python:3.10-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH
COPY . .
CMD ["python", "app.py"]
```

## .dockerignore

```
__pycache__
*.pyc
.git
```

---

# ============================

# 09_kubernetes_intro/

# ============================

## deployment.yaml

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ml-app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: ml
  template:
    metadata:
      labels:
        app: ml
    spec:
      containers:
      - name: ml-container
        image: ml-app:latest
        ports:
        - containerPort: 8000
```

## service.yaml

```yaml
apiVersion: v1
kind: Service
metadata:
  name: ml-service
spec:
  type: NodePort
  selector:
    app: ml
  ports:
    - port: 80
      targetPort: 8000
```

---

# ============================

# CHEATSHEET

# ============================

## docker_commands.md

```bash
docker build -t image .
docker run -p 8000:8000 image
docker ps
docker images
docker exec -it container bash
```

---

# 🧠 Bonus Tips

* Use GPU: `--gpus all`
* Debug: `docker logs <id>`
* Env vars:

```bash
docker run -e ENV=prod image
```

---

🔥 This repo = Full Docker course for ML Engineers