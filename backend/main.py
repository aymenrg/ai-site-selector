from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from census_service import get_demographics
from osm_service import get_osm_data

app = FastAPI(title="AI Site Selector API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/analyze")
def analyze_location(payload: dict):
    # Extract lat/lng from the JSON payload sent by React
    lat = payload.get("lat")
    lng = payload.get("lng")

    # 1. Fetch Demographics
    demographics = get_demographics(lat, lng)
    
    # 2. Fetch Map Data
    osm_data = get_osm_data(lat, lng)
    
    # 3. Combine into one master dictionary
    final_result = {
        "coordinates": {"lat": lat, "lng": lng},
        "demographics": demographics,
        "market_ecosystem": osm_data,
        "status": "Success"
    }
    
    return final_result