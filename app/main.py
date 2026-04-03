from fastapi import FastAPI, HTTPException
import requests
import os
app = FastAPI(title="Weather API")

@app.get("/weather/{city}")
def get_weather(city: str):
    # Using a mock API for demonstration
    response = requests.get(f"https://wttr.in/{city}?format=j1")
    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="City not found")
    data = response.json()
    return {"city": city, "temperature": data["current_condition"][0]["temp_C"]}


# A deliberate "Code Smell" and Security Vulnerability
def insecure_function():
    # Unused variable (Code Smell)
    unused_var = "I am not used"
    
    # Hardcoded sensitive-looking string (Security Hotspot)
    db_password = "admin_password_123"
    
    # Using an insecure print in a web app
    print("This is a bad practice for logging")
    return True