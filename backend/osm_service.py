import requests

def get_osm_data(lat: float, lng: float, radius: int = 1000):
    overpass_url = "http://overpass-api.de/api/interpreter"
    
    # This query asks for all shops and bus stops within 'radius' meters of lat, lng
    overpass_query = f"""
    [out:json];
    (
      node["shop"](around:{radius},{lat},{lng});
      node["highway"="bus_stop"](around:{radius},{lat},{lng});
    );
    out body;
    """
    
    response = requests.get(overpass_url, params={'data': overpass_query})
    
    competitor_count = 0
    transit_count = 0
    
    if response.status_code == 200:
        data = response.json()
        for element in data.get("elements", []):
            tags = element.get("tags", {})
            if "shop" in tags:
                competitor_count += 1
            if "highway" in tags and tags["highway"] == "bus_stop":
                transit_count += 1
                
    return {
        "competitors_within_1km": competitor_count,
        "transit_stops_within_1km": transit_count
    }

