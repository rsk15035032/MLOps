# 🧠 ONNX Image Classification API (AWS Lambda + Docker)

A **production-ready ML inference system** for clothing classification using **ONNX Runtime**, deployed via **AWS Lambda container** and tested locally with an HTTP client.

---

## 🚀 Overview

This project demonstrates an **end-to-end inference pipeline**:
Client (requests) → Lambda Container → ONNX Model → Predictions


- ⚡ Fast inference with ONNX Runtime  
- 🐳 Containerized using AWS Lambda base image  
- 🔁 Robust client with retries & timeout  
- 📦 Clean, scalable, production-grade code  

---

## 🏗️ Project Structure
```
├── lambda_function.py # Inference logic (preprocess + predict + handler)
├── clothing-model-new.onnx
├── requirements.txt
├── Dockerfile
└── test.py # Client to invoke Lambda locally
```

---

## ⚙️ Setup & Run

### 1️⃣ Build Docker Image
```bash
docker build -t clothing-model .
```

### 2️⃣ Run Lambda Container
```bash
docker run -p 8080:8080 clothing-model
```

### 3️⃣ Invoke API
```
python test.py
```
### 📥 API Contract
```Json
Request
{
  "url": "http://bit.ly/mlbookcamp-pants"
}
Response
{
  "pants": 0.92,
  "shirt": 0.03,
  ...
}
```
### 🧠 Model Details
- Format: ONNX
- Input: 224x224 RGB image
- Preprocessing:
- Normalize [0,255] → [0,1]
- Convert NHWC → NCHW

### ImageNet normalization
🔥 Key Features
- ✅ Production-grade ONNX inference
- ✅ Optimized Lambda cold start
- ✅ Retry + timeout handling (client-side)
- ✅ Clean, modular architecture
- ✅ Fully containerized deployment
- 📈 Future Improvements
- 🔹 GPU support (CUDAExecutionProvider)
- 🔹 Async inference (FastAPI)
- 🔹 Batch prediction
- 🔹 Monitoring (Prometheus / CloudWatch)
-🔹 CI/CD pipeline
👨‍💻 Author

Ravi Shankar Kumar| Machine Learning Engineer | MLOps


---
