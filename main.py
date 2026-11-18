import os
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from curl_cffi import requests as c_requests

app = FastAPI(title="Cloudflare Bypass Proxy API", version="2.0")

class ScrapeRequest(BaseModel):
    url: str

@app.get("/")
def home():
    return {"status": "online", "message": "Cloudflare Bypass Proxy API is running perfectly!"}

@app.get("/scrape")
def scrape_get(url: str = Query(..., description="Target URL to bypass Cloudflare")):
    try:
        # curl_cffi mimics real browser TLS fingerprints to bypass Cloudflare automatically
        response = c_requests.get(url, impersonate="chrome120", timeout=30)
        
        if response.status_code >= 400:
            raise HTTPException(status_code=response.status_code, detail=f"Target site returned status {response.status_code}")
            
        return {
            "status": True,
            "url": url,
            "solution": {
                "status": response.status_code,
                "html": response.text
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/scrape")
def scrape_post(req: ScrapeRequest):
    try:
        response = c_requests.get(req.url, impersonate="chrome120", timeout=30)
        
        if response.status_code >= 400:
            raise HTTPException(status_code=response.status_code, detail=f"Target site returned status {response.status_code}")
            
        return {
            "status": True,
            "url": req.url,
            "solution": {
                "status": response.status_code,
                "html": response.text
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
