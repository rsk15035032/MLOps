## 🚀 System Architecture
```text
Git Push → CI Pipeline → Train Model → Evaluate → Register Model
        → CD Pipeline → Build Docker → Deploy API → Monitor
```

We’ll use:

- MLflow → tracking + registry
- GitHub Actions → automation
- Docker → packaging
- Kubernetes → deployment
- FastAPI → serving

## 🧱 Project Structure (Production Grade)
```
mlops-cicd/
│
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── cd.yml
│
├── src/
│   ├── train.py
│   ├── evaluate.py
│   ├── predict.py
│
├── app/
│   └── main.py
│
├── tests/
│   └── test_model.py
│
├── Dockerfile
├── requirements.txt
├── k8s/
│   ├── deployment.yaml
│   └── service.yaml
└── README.md
```
## ⚙️ Step 1: Training Script (MLflow Integrated)
src/train.py
```python
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

mlflow.set_experiment("iris-exp")

def train():
    data = load_iris()
    X_train, X_test, y_train, y_test = train_test_split(data.data, data.target)

    with mlflow.start_run():
        model = RandomForestClassifier(n_estimators=100)
        model.fit(X_train, y_train)

        acc = model.score(X_test, y_test)

        mlflow.log_metric("accuracy", acc)
        mlflow.sklearn.log_model(model, "model")

        return acc

if __name__ == "__main__":
    train()
```    
## 🧪 Step 2: Evaluation Gate (VERY IMPORTANT)
src/evaluate.py
```python
import sys
import mlflow

THRESHOLD = 0.85

def check_model():
    client = mlflow.tracking.MlflowClient()
    runs = client.search_runs(experiment_ids=["0"], order_by=["metrics.accuracy DESC"])

    best_run = runs[0]
    acc = best_run.data.metrics["accuracy"]

    print(f"Best Accuracy: {acc}")

    if acc < THRESHOLD:
        print("Model rejected ❌")
        sys.exit(1)
    else:
        print("Model accepted ✅")

if __name__ == "__main__":
    check_model()
```
## 🌐 Step 3: FastAPI Serving

app/main.py
```python
from fastapi import FastAPI
import mlflow.pyfunc
import numpy as np

app = FastAPI()

model = mlflow.pyfunc.load_model("models:/iris-classifier/Production")

@app.post("/predict")
def predict(data: list):
    preds = model.predict(np.array(data))
    return {"prediction": preds.tolist()}
```

## 🐳 Step 4: Dockerfile
```Dockerfile
FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## ☸️ Step 5: Kubernetes Deployment
k8s/deployment.yaml
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
        image: your-dockerhub/ml-api:latest
        ports:
        - containerPort: 8000
```
k8s/service.yaml

```yaml
apiVersion: v1
kind: Service
metadata:
  name: ml-service
spec:
  type: LoadBalancer
  selector:
    app: ml-api
  ports:
    - port: 80
      targetPort: 8000
```

## 🔁 Step 6: CI Pipeline (GitHub Actions)
.github/workflows/ci.yml
```yaml
name: CI Pipeline

on:
  push:
    branches: [ "main" ]

jobs:
  train:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout
      uses: actions/checkout@v3

    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: "3.10"

    - name: Install dependencies
      run: pip install -r requirements.txt

    - name: Train Model
      run: python src/train.py

    - name: Evaluate Model
      run: python src/evaluate.py
```

👉 If evaluation fails → pipeline stops ❌

## 🚀 Step 7: CD Pipeline
.github/workflows/cd.yml

```yaml
name: CD Pipeline

on:
  workflow_run:
    workflows: ["CI Pipeline"]
    types:
      - completed

jobs:
  deploy:
    if: ${{ github.event.workflow_run.conclusion == 'success' }}
    runs-on: ubuntu-latest

    steps:
    - name: Checkout
      uses: actions/checkout@v3

    - name: Build Docker Image
      run: docker build -t your-dockerhub/ml-api:latest .

    - name: Push to DockerHub
      run: |
        echo "${{ secrets.DOCKER_PASSWORD }}" | docker login -u ${{ secrets.DOCKER_USERNAME }} --password-stdin
        docker push your-dockerhub/ml-api:latest

    - name: Deploy to Kubernetes
      run: |
        kubectl apply -f k8s/deployment.yaml
        kubectl apply -f k8s/service.yaml
```
## 🧪 Step 8: Testing (Optional but FAANG-level)
tests/test_model.py
```python
def test_basic():
    assert 1 + 1 == 2
```

## 💻 Command Line (End-to-End)
🔹 Local Run
```bash
# Train
python src/train.py

# Evaluate
python src/evaluate.py

# Run API
uvicorn app.main:app --reload
```
🔹 Docker
```bash
docker build -t ml-api .
docker run -p 8000:8000 ml-api
```

🔹 Kubernetes
```bash
kubectl apply -f k8s/
kubectl get pods
kubectl get svc
```

## 🧠 FAANG-Level Enhancements
✅ 1. Separate Environments
Dev / Staging / Production clusters
✅ 2. Model Promotion Workflow
Auto → Staging
Manual approval → Production
✅ 3. Data Versioning
DVC or LakeFS
✅ 4. Feature Store
Feast
✅ 5. Monitoring
Prometheus + Grafana
Drift detection (Evidently)
✅ 6. Rollback Strategy
kubectl rollout undo deployment/ml-api