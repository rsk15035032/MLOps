import mlflow
import mlflow.sklearn
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import joblib

# Load data
data = pd.read_csv("data\house_price_prediction.csv")
data = data.fillna(0)

X = data[["avg_income", "avg_area_house_age", "avg_area_num_rooms",
       "avg_bedrooms", "avg_population"]]
y = data["price"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Start MLflow run
with mlflow.start_run():

    # Parameters
    model = LinearRegression()
    mlflow.log_param("model_type", "LinearRegression")

    # Train
    model.fit(X_train, y_train)

    # Predict
    preds = model.predict(X_test)

    # Metrics
    mse = mean_squared_error(y_test, preds)
    r2 = r2_score(y_test, preds)

    mlflow.log_metric("mse", mse)
    mlflow.log_metric("r2_score", r2)

    # Save model
    joblib.dump(model, "model.joblib")

    # Log artifacts
    mlflow.log_artifact("model.joblib")

    # Log model to MLflow
    mlflow.sklearn.log_model(
        sk_model=model,
        artifact_path="house_price_model",
        registered_model_name="HousePriceModel"
    )

    print("Training completed and logged to MLflow")
