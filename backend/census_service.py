import os
import requests
from dotenv import load_dotenv

load_dotenv()
CENSUS_API_KEY = os.getenv("CENSUS_API_KEY")

def get_fips_from_coords(lat: float, lng: float):
    url = f"https://geo.fcc.gov/api/census/block/find?latitude={lat}&longitude={lng}&format=json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        fips = data['Block']['FIPS']
        # Extract State (2 digits), County (3 digits), Tract (6 digits)
        state = fips[0:2]
        county = fips[2:5]
        tract = fips[5:11]
        return state, county, tract
    return None, None, None
def get_demographics(lat: float, lng: float):
    state, county, tract = get_fips_from_coords(lat, lng)
    
    if not state:
        return {"error": "Could not find Census data for this location"}

    # We ask for Income and Population
    url = f"https://api.census.gov/data/2021/acs/acs5?get=B19013_001E,B01003_001E&for=tract:{tract}&in=state:{state}%20county:{county}&key={CENSUS_API_KEY}"
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # data[0] is headers, data[1] is the actual numbers
        income = data[1][0]
        population = data[1][1]
        
        return {
            "median_income": int(income) if income and income != "-666666666" else 0,
            "population": int(population) if population else 0
        }
    return {"error": "Census API request failed"}