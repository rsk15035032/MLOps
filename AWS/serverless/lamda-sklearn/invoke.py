import boto3
import json

lambda_client = boto3.client("lambda")

with open("customer.json", "r") as f:
    payload = json.load(f)

response = lambda_client.invoke(
    FunctionName="churn-prediction-docker",
    InvocationType="RequestResponse",
    Payload=json.dumps(payload)
)

result = json.loads(response["Payload"].read())

print(json.dumps(result, indent=2))