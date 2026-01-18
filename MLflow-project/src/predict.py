import mlflow.sklearn
import pandas as pd

model_name = "HousePriceModel"
model_alias = "champion"


model = mlflow.sklearn.load_model(
    model_uri=f"models:/{model_name}@{model_alias}"
)

sample = pd.DataFrame({
    "avg_income": [79248.64245],
    "avg_area_house_age": [6.002899808],
    "avg_area_num_rooms": [6.730821019],
    "avg_bedrooms": [3.09],
    "avg_population": [40173.07217]
})

prediction = model.predict(sample)
print("Predicted price:", prediction[0])
