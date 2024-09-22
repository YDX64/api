from fastapi import FastAPI, HTTPException, Request, Depends
from pydantic import BaseModel
from analysis.analyze import process_match
from api.get_list import fetch_soccer_data
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import redis
import json
import os
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

app = FastAPI()

# Rate Limiting için Limiter'ı ayarla
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Redis bağlantısını ayarla
redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = int(os.getenv("REDIS_PORT", 6379))
redis_password = os.getenv("REDIS_PASSWORD", None)

try:
    redis_client = redis.Redis(host=redis_host, port=redis_port, password=redis_password, db=0)
    redis_client.ping()
    print("Connected to Redis")
except redis.ConnectionError:
    print("Could not connect to Redis")
    redis_client = None

class MatchID(BaseModel):
    match_id: int

class DateRequest(BaseModel):
    date: str

async def verify_api_key(request: Request):
    api_key = request.headers.get("X-API-KEY")
    if api_key != os.getenv("API_KEY"):
        raise HTTPException(status_code=403, detail="Invalid API Key")

@app.get("/ping")
async def ping_redis():
    try:
        redis_client.ping()
        return {"status": "Connected to Redis"}
    except redis.ConnectionError:
        raise HTTPException(status_code=500, detail="Could not connect to Redis")

@app.post("/analyze-match")
@limiter.limit("80/minute")
async def analyze_match_endpoint(request: Request, match_id: MatchID, api_key: str = Depends(verify_api_key)):
    if not redis_client:
        raise HTTPException(status_code=500, detail="Redis connection is not available")
    
    try:
        cache_key = f"match:{match_id.match_id}"
        
        # Önbellekten veriyi kontrol et
        cached_data = redis_client.get(cache_key)
        if cached_data:
            result = json.loads(cached_data)
        else:
            # Önbellekte yoksa veriyi çek ve önbelleğe kaydet
            result = await process_match(match_id.match_id)
            if result is False:
                raise HTTPException(status_code=404, detail="Match data could not be processed")
            
            # Veriyi önbelleğe kaydet (1800 saniye = 30 dakika)
            redis_client.set(cache_key, json.dumps(result), ex=3600)

        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/fetch-matches")
@limiter.limit("50/minute")
async def fetch_matches_endpoint(request: Request, request_data: DateRequest, api_key: str = Depends(verify_api_key)):
    if not redis_client:
        raise HTTPException(status_code=500, detail="Redis connection is not available")
    
    try:
        tarih = request_data.date

        cached_data = redis_client.get(tarih)
        if cached_data:
            match_id_list = json.loads(cached_data)
        else:
            path = f"/ajax/SoccerAjax?type=6&date={tarih}&order=time&timezone=3&flesh=0.12689888719604503"
            match_id_list = await fetch_soccer_data(path)
            
            if not match_id_list:
                raise HTTPException(status_code=404, detail="No match data found for the given date")
            
            redis_client.set(tarih, json.dumps(match_id_list), ex=3600)

        return {"status": "success", "data": match_id_list}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
