from fastapi import Request, HTTPException
import time

_limits = {}

async def rate_limit_middleware(request: Request, call_next):
    client_ip = request.client.host
    now = time.time()
    
    if client_ip not in _limits:
        _limits[client_ip] = []
    
    _limits[client_ip] = [t for t in _limits[client_ip] if now - t < 60]
    
    if len(_limits[client_ip]) > 100:
        raise HTTPException(status_code=429, detail="Too many requests")
    
    _limits[client_ip].append(now)
    return await call_next(request)
