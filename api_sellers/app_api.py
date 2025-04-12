from fastapi import FastAPI, HTTPException
import pandas as pd
import pickle
from pydantic import BaseModel
from typing import Literal
import uvicorn
from threading import Thread

app = FastAPI()

with open('model.pkl', 'rb') as f:
    model = pickle.load(f)


class InsuranceInput(BaseModel):
    Pclass: int
    Age: int
    CarAge: int
    InsuranceCost: int
    DaysWithCompany: int
    HasLicence: int
    HasDamage: int

@app.get("/health")
def health():
    return {"status": "OK"}

@app.post("/predict")
async def predict_insurance(data: InsuranceInput):
    try:
        model_data = {
            "Gender": 1 if data.Pclass == 1 else 0,
            "Driving_License": data.HasLicence,
            "Vehicle_Age": data.CarAge,
            "Annual_Premium": data.InsuranceCost,
            "Vintage": data.DaysWithCompany,
            "Age Above 38": 1 if data.Age < 38 else 0,
            "Not_Insured and Damaged": data.HasDamage
        }

        df = pd.DataFrame([model_data])[model.feature_names_in_]
        prediction = model.predict(df)
        return {"result": "Купит страховку" if prediction == 1 else "Не купит"}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

        

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
