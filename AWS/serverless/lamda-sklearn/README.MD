# 🚀 Churn Prediction System (Production-Ready)

## Overview
End-to-end ML system for predicting customer churn using:
- AWS Lambda (Docker)
- Scikit-learn pipeline
- Kubernetes (scaling)
- uv (dependency management)

## Features
- Serverless inference (Lambda)
- Auto-scaling (K8s HPA)
- Reproducible builds (uv.lock)
- Robust error handling & logging

## Run Locally

```bash
docker build -t churn-model .
docker run -p 8080:8080 churn-model
python test_local.py
```

## Deploy to AWS Lambda
```bash
aws ecr create-repository --repository-name churn-model
docker tag churn-model:latest <ECR_URI>
docker push <ECR_URI>
Kubernetes Deployment
kubectl apply -f k8s/
```

## API Example
```json
POST /predict

{
  "customer": {...}
}
Output
{
  "churn_probability": 0.72,
  "churn": true
}
```

## Future Improvements
- Model monitoring (drift)
- CI/CD pipeline
- Feature store integration
- API Gateway + IAM security

---

# 🔥 Final Verdict

This version is:

✅ Clean  
✅ Scalable  
✅ Production-ready  
✅ Interview-ready (FAANG level)  

---

Author:

👉 Ravi Shankar Kumar | ML Engg.
