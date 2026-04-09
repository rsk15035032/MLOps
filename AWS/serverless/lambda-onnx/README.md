# 🧠 ONNX Image Classification API (AWS Lambda Ready)

A **production-ready image classification pipeline** built using **ONNX Runtime**, designed for **high-performance inference** and seamless deployment on **AWS Lambda (Docker-based)**.

---

## 🚀 Overview

This project provides an **end-to-end ML inference pipeline** that:

* 📥 Accepts an **image URL**
* 🧹 Applies **PyTorch-style preprocessing**
* ⚡ Runs inference using **ONNX Runtime**
* 📤 Returns **class probabilities (Top-K supported)**

---

## ✨ Features

* ⚡ Fast inference with **ONNX Runtime**
* ☁️ **AWS Lambda optimized** (cold-start friendly)
* 🧼 Clean & modular code structure
* 🛡️ Robust **error handling**
* 🎯 Supports **Top-K predictions**
* 🔌 Easily extendable (GPU, batch, API)

---

## 📁 Project Structure

```bash
project/
│
├── Dockerfile
├── requirements.txt
│
├── models/
│   └── clothing-model-new.onnx
│
├── src/
│   ├── lambda_function.py      # Lambda entry point
│   ├── inference.py            # Core pipeline (model + preprocessing)
│   └── utils.py                # Optional helpers
│
├── test.py                     # Local testing script
└── README.md
```

---

## ⚙️ How It Works

### 🔄 Pipeline Flow

```text
Image URL → Preprocessing → ONNX Model → Predictions → JSON Response
```

---

## 📦 Installation

```bash
pip install -r requirements.txt
```

**requirements.txt**

```txt
onnxruntime
keras-image-helper
numpy
```

---

## 🐳 Run with Docker (Lambda Local)

### 1️⃣ Build Image

```bash
docker build -t clothing-classifier .
```

### 2️⃣ Run Container

```bash
docker run -p 8080:8080 clothing-classifier
```

### 3️⃣ Test Locally

```bash
python test.py
```

---

## ▶️ Example Usage

```python
from lambda_invoker import LambdaInvoker

client = LambdaInvoker()

payload = {
    "url": "http://bit.ly/mlbookcamp-pants"
}

response = client.invoke(payload)
print(response)
```

---

## 📥 Input Format

```json
{
  "url": "https://example.com/image.jpg"
}
```

---

## 📤 Output Format

```json
{
  "predictions": {
    "pants": 0.92,
    "jeans": 0.05,
    "shorts": 0.03
  },
  "status": "success"
}
```

---

## 🧠 Model Details

* 📌 Format: **ONNX**
* 🖼 Input Size: **224x224**
* 🎯 Classes:

  * dress, hat, longsleeve, outwear, pants
  * shirt, shoes, shorts, skirt, t-shirt

---

## ⚡ Optimization Techniques

* 🔁 **Global model loading** (reduces cold start)
* 📦 Lightweight dependencies
* ⚙️ CPU/GPU provider support
* 🧠 Efficient preprocessing pipeline

---

## 🛠️ Configuration

| Parameter     | Description                    | Default    |
| ------------- | ------------------------------ | ---------- |
| `MODEL_PATH`  | Path to ONNX model             | models/... |
| `target_size` | Input image size               | (224,224)  |
| `use_gpu`     | Enable GPU inference           | False      |
| `top_k`       | Number of predictions returned | 3          |

---

## 🔥 Future Enhancements

* ⚡ Async API using FastAPI
* 🔁 Batch inference support
* ☁️ S3 image input support
* 📊 Monitoring & logging (CloudWatch)
* 🚀 GPU acceleration (CUDA / TensorRT)

---

## 🧪 Troubleshooting

### ❌ Model Not Found

* Ensure path: `models/clothing-model-new.onnx`

### ❌ Slow First Request

* Expected (Lambda cold start)

### ❌ Connection Refused

* Check Docker container is running on port `8080`

---

## 💡 Summary

This project demonstrates how to build a:

* 🧠 Scalable ML inference system
* ☁️ Cloud-native deployment (AWS Lambda)
* ⚡ High-performance ONNX pipeline

---

⭐ **Clean • Scalable • Production-Ready**
