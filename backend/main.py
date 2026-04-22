from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="AI Site Selector API")

# This allows our future React frontend to talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "Backend is running!"}

@app.get("/api/analyze")
def analyze_location(lat: float, lng: float):
    # We will put the real AI and Data logic here later
    return {
        "message": f"Received coordinates: {lat}, {lng}",
        "score": 0
    }
