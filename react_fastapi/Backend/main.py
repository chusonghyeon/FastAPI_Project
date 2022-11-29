from typing import List
import fastapi
import fastapi.security

import sqlalchemy.orm

import services
import schemas

app = fastapi.FastAPI()

# user api 만들기
@app.post("/api/users")
async def create_user(user: schemas.UserCreate, db: sqlalchemy.orm.Session = fastapi.Depends(services.get_db)):
    db_user = await services.get_user_by_email(user.email, db)
    if db_user:
        raise fastapi.HTTPException(status_code=400, detail="Email already in use")
    
    user = await services.create_user(user, db)

    return await services.create_token(user)


# user Token 발행받고 로그인 확인하기
@app.post("/api/token")
async def generate_token(form_data: fastapi.security.OAuth2PasswordRequestForm = fastapi.Depends(), db: sqlalchemy.orm.Session = fastapi.Depends(services.get_db)):
    user = await services.authenticate_user(form_data.username, form_data.password, db)
    
    if not user:
        raise fastapi.HTTPException(status_code=401, detail="InValid Credentials")
    
    return await services.create_token(user)

# user의 정보 확인
@app.get("/api/users/me", response_model=schemas.User)
async def get_user(user: schemas.User = fastapi.Depends(services.get_current_user)):
    return user


# lead 만들기
@app.post("/api/leads", response_model= schemas.Lead)
async def create_lead(lead: schemas.LeadCrate, user: schemas.User = fastapi.Depends(services.get_current_user), db: sqlalchemy.orm.session = fastapi.Depends(services.get_db)):
    return await services.create_lead(user=user, db=db, lead=lead)


# 
@app.get("/api/leads", response_model=List[schemas.Lead])
async def get_leads(user: schemas.User = fastapi.Depends(services.get_current_user), db: sqlalchemy.orm.session = fastapi.Depends(services.get_db)):
    return await services.get_leads(user=user, db=db)


# lead 상세정보 보기
@app.get("/api/leads/{lead_id}", status_code=200)
async def get_lead(lead_id: int ,user: schemas.User = fastapi.Depends(services.get_current_user), db: sqlalchemy.orm.session = fastapi.Depends(services.get_db)):
    return await services.get_lead(lead_id, user, db)


# lead 삭제
@app.delete("/api/leads/{lead_id}", status_code=204)
async def delete_lead(lead_id: int ,user: schemas.User = fastapi.Depends(services.get_current_user), db: sqlalchemy.orm.session = fastapi.Depends(services.get_db)):
    await services.delete_lead(lead_id, user, db)
    
    return {"message", "Successfully Deleted"}


# lead 수정
@app.put("/api/leads/{lead_id}", status_code=200)
async def update_lead(lead_id: int, lead: schemas.LeadCrate,user: schemas.User = fastapi.Depends(services.get_current_user), db: sqlalchemy.orm.session = fastapi.Depends(services.get_db)):
    await services.update_lead(lead_id, lead, user, db)
    return {"message", "Successfully Updated"}


@app.get("/api")
async def root():
    return {"message": "Awesome Leads Manager"}