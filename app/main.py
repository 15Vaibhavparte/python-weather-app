from fastapi import FastAPI, HTTPException
import requests

app = FastAPI(title="Weather API")

@app.get("/weather/{city}")
def get_weather(city: str):
    # Using a mock API for demonstration
    response = requests.get(f"https://wttr.in/{city}?format=j1")
    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="City not found")
    data = response.json()
    return {"city": city, "temperature": data["current_condition"][0]["temp_C"]}