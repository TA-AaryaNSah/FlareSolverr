import os
import requests
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

app = FastAPI(title="FlareSolverr Proxy API", version="1.0")

# Production URL configured via environment variable (No localhost fallback)
FLARESOLVERR_URL = os.getenv("FLARESOLVERR_URL", "https://flaresolverr-cifj.onrender.com/v1")

class ScrapeRequest(BaseModel):
    url: str
    maxTimeout: int = 60000

@app.get("/")
def home():
    return {"status": "online", "message": "FlareSolverr Proxy API is running successfully!"}

@app.get("/scrape")
def scrape_get(url: str = Query(..., description="Target URL to bypass Cloudflare")):
    payload = {
        "cmd": "request.get",
        "url": url,
        "maxTimeout": 60000
    }
    
    try:
        response = requests.post(FLARESOLVERR_URL, json=payload, timeout=70)
        data = response.json()
        
        if data.get("status") == "ok":
            return {
                "status": True,
                "url": url,
                "solution": data.get("solution")
            }
        else:
            raise HTTPException(status_code=502, detail=data)
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/scrape")
def scrape_post(req: ScrapeRequest):
    payload = {
        "cmd": "request.get",
        "url": req.url,
        "maxTimeout": req.maxTimeout
    }
    
    try:
        response = requests.post(FLARESOLVERR_URL, json=payload, timeout=70)
        data = response.json()
        
        if data.get("status") == "ok":
            return {
                "status": True,
                "url": req.url,
                "solution": data.get("solution")
            }
        else:
            raise HTTPException(status_code=502, detail=data)
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
