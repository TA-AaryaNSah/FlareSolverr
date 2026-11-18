import os
from fastapi import FastAPI, HTTPException, Query
import cloudscraper

app = FastAPI(title="Cloudflare Bypass API", version="1.0")

# Cloudscraper automatically handles Cloudflare JavaScript challenges without heavy browsers
scraper = cloudscraper.create_scraper(
    browser={
        'browser': 'chrome',
        'platform': 'windows',
        'desktop': True
    }
)

@app.get("/")
def home():
    return {"status": "online", "message": "Bypass API is running!"}

@app.get("/scrape")
def scrape(url: str = Query(..., description="Target URL")):
    try:
        response = scraper.get(url, timeout=35)
        
        if response.status_code >= 400:
            raise HTTPException(status_code=response.status_code, detail=f"Blocked with status {response.status_code}")
            
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
