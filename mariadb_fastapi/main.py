from typing  import Optional

from fastapi import FastAPI
from pydantic import BaseModel
import os
import requests

app = FastAPI()

db =[]

class City(BaseModel):
    name : str
    timezone : str


@app.get("/")
async def read_root():
    return {"Hello": "World"}

# 도시전체보기
@app.get('/cities')
async def get_cities():
    results = []
    for city in db:
        # strs = f"http://worldtimeapi.org/timezone/{city['timezone']}"
        strs = f"http://worldtimeapi.org/api/timezone/{city['timezone']}"
        r = requests.get(strs)
        cur_time = r.json()['datetime']
        results.append({'name':city['name'],'timezone':city['timezone'], 'current_time':cur_time})
    
    return results

# 도시 세부사항
@app.get('/cities{city_id}')    
async def get_city(city_id : int):
    city = db[city_id-1]
    strs = f"http://worldtimeapi.org/api/timezone/{city['timezone']}"
    r = requests.get(strs)
    
    cur_time = r.json()['datetime']
    return {'name':city['name'], 'timezone':city['timezone'], 'current_time': cur_time}
    

# 도시 만들기
@app.post('/cities')
async def create_city(city : City):
    db.append(city.dict())
    
    return db[-1]

# 도시 삭제하기
@app.delete('/cities/{city_id}')
async def delete_city(city_id : int):
    db.pop(city_id-1)
    return {}