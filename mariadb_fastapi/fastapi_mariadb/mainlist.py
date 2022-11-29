from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from typing import List
from starlette.middleware.cors import CORSMiddleware

from db import session
from model import UserTable, User


templates = Jinja2Templates(directory="templates")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers=["*"]
)


@app.get("/users", response_class=HTMLResponse)
async def read_users(request : Request):
    context = {}
    users = session.query(UserTable).all()
    
    context["request"] = request
    context["users"] = users
    
    return templates.TemplateResponse("user_list.html", context)


@app.get("/users/{user_id}", response_class=HTMLResponse)
async def read_user(request : Request, user_id : int):
    context = {}
    
    user = session.query(UserTable).filter(UserTable.id == user_id).first()
    
    context['name'] = user.name
    context['age'] = user.age
    context['request'] = request
    
    return templates.TemplateResponse("user_detail.html", context)

@app.post("/users")
async def create_users(users: User):
    # data = {(id:0), (name:uname), (age: uage)}
    
    userlist = list(users)
    uname = userlist[1][1]
    uage = userlist[2][1]
    
    user = UserTable()
    user.name = uname
    user.age = uage
    
    session.add(user)
    session.commit()
    
    return {"result_msg",f"{uname} created ..."}

@app.put("/users")
async def modify_users(users: User):
    
    userlist = list(users)
    uid = userlist[0][1]
    uname = userlist[1][1]
    uage = userlist[2][1]
    
    user = session.query(UserTable).filter(UserTable.id == uid).first()
    user.name = uname
    user.age = uage
    session.commit()
        
    # users[0].name
    
    return {"result_msg",f"{uname} updated ..."}

@app.delete("/users")
async def delete_users(users: User):
    
    userlist = list(users)
    uid = userlist[0][1]
    
    user = session.query(UserTable).filter(UserTable.id == uid).delete()
    session.commit()
    
    return {"result_msg",f"{user} deleted ..."}