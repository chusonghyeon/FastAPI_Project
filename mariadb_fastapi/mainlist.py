from typing  import Optional

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
# Jinja Templates 사용
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

import requests

app = FastAPI()

db =[]

# 클래스 형식으로 BaseModel 정의
class City(BaseModel):
    name : str
    timezone : str

class CityModify(BaseModel):
    id : int
    name : str
    timezone : str

# templates설정
templates = Jinja2Templates(directory="templates")


@app.get("/")
def read_root():
    return {"Hello": "World"}

# GET메서드
@app.get('/cities', response_class=HTMLResponse)
def get_cities(request: Request):
    context = {}
    
    cnt = 0
    
    rsCity = []
    for city in db:
        # strs = f"http://worldtimeapi.org/timezone/{city['timezone']}"
        strs = f"http://worldtimeapi.org/api/timezone/{city['timezone']}"
        r = requests.get(strs)
        cur_time = r.json()['datetime']
        
        cnt +=1
        
        rsCity.append({'id': cnt,'name':city['name'],'timezone':city['timezone'], 'current_time':cur_time})
    
    context['request'] = request
    context['rsCity'] = rsCity
    return templates.TemplateResponse('city_list.html', context)

# DETAIL매서드
@app.get('/cities/{city_id}')    
def get_city(request: Request, city_id : int):
    city = db[city_id-1]
    r = requests.get(f"http://worldtimeapi.org/api/timezone/{city['timezone']}")
    cur_time = r.json()['datetime']
    
    context = {'request': request, 'name':city['name'], 'timezone':city['timezone'], 'current_time': cur_time}

    return templates.TemplateResponse('city_detail.html', context)
    

# POST매서드
@app.post('/cities')
def create_city(city : City):
    
    db.append(city.dict())
        
    return db[-1]

# PUT매서드
@app.put('/cities')
def modify_city(city : CityModify):
    db[city.id-1] = {'name': city.name, 'timezone': city.timezone}
    
    return db[city.id-1]

# DELETE매서드    
@app.delete('/cities/{city_id}')
def delete_city(city_id : int):
    db.pop(city_id-1)
    return {}