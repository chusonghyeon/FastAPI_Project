import jwt
import sqlalchemy.orm
import passlib.hash
import datetime

import database
import models
import schemas
import fastapi
import fastapi.security

# JWT토근 값 저장
oauth2schema = fastapi.security.OAuth2PasswordBearer(tokenUrl="/api/token")
JWT_SECRET = "myjwtsecret"

# DataBase 생성(Sqlite)
def create_database():
    return database.Base.metadata.create_all(bind = database.engine)

# SQlite에 있는 DB가져오기
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Email 가져오기
async def get_user_by_email(email: str, db: sqlalchemy.orm.Session):
    return db.query(models.User).filter(models.User.email == email).first()

# Email 만들고 db에 저장하기
async def create_user(user: schemas.UserCreate, db: sqlalchemy.orm.Session):
    user_obj = models.User(email = user.email, hashed_password = passlib.hash.bcrypt.hash(user.hashed_password))
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return user_obj

# 로그인 여부 확인하여서 확인하기
async def authenticate_user(email:str, password: str, db: sqlalchemy.orm.Session):
    user = await get_user_by_email(db=db, email=email)
    
    if not user:
        return False
    
    if not user.verify_password(password):
        return False
    
    return user

# JWT Token 발행
async def create_token(user: models.User):
    user_obj = schemas.User.from_orm(user)
    
    token = jwt.encode(user_obj.dict(), JWT_SECRET)
    
    return dict(access_token = token, token_type = "bearer")

# User에 TOken발행한 내용 가져오기
async def get_current_user(db: sqlalchemy.orm.session = fastapi.Depends(get_db), token: str = fastapi.Depends(oauth2schema)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        user = db.query(models.User).get(payload["id"])
    except:
        raise fastapi.HTTPException(status_code=401, detail="Invalid Email or Password")
    
    return schemas.User.from_orm(user)

# lead유저 만들기
async def create_lead(user: schemas.User, db: sqlalchemy.orm.Session, lead: schemas.LeadCrate):
    lead = models.Lead(**lead.dict(), owner_id = user.id)
    db.add(lead)
    db.commit()
    db.refresh(lead)
    return schemas.Lead.from_orm(lead)

# 모든 lead 가져오기
async def get_leads(user: schemas.User, db: sqlalchemy.orm.Session):
    leads = db.query(models.Lead).filter_by(owner_id=user.id) 
    
    return list(map(schemas.Lead.from_orm, leads))


async def _lead_selector(lead_id: int, user: schemas.User, db: sqlalchemy.orm.Session):
    lead = db.query(models.Lead).filter_by(owner_id = user.id).filter(models.Lead.id == lead_id).first()
    
    if lead is None:
        raise fastapi.HTTPException(status_code=404, detail="Lead does not exist")
    
    return lead

# lead 상세하게 불러오기
async def get_lead(lead_id: int, user: schemas.User, db: sqlalchemy.orm.Session):
    lead = await _lead_selector(lead_id=lead_id, user=user, db=db)
    
    return schemas.Lead.from_orm(lead)

# 삭제
async def delete_lead(lead_id: int, user: schemas.User, db: sqlalchemy.orm.Session):
    lead = await _lead_selector(lead_id, user, db)
    
    db.delete(lead)
    db.commit()
    
# 수정    
async def update_lead(lead_id: int, lead: schemas.LeadCrate, user: schemas.User, db: sqlalchemy.orm.Session):
    lead_db = await _lead_selector(lead_id, user, db)
    
    lead_db.first_name = lead.first_name
    lead_db.last_name = lead.last_name
    lead_db.email = lead.email
    lead_db.company = lead.company
    lead_db.note = lead.note
    lead_db.date_last_updated = datetime.datetime.utcnow()
    
    db.commit()
    db.refresh(lead_db)
    
    return schemas.Lead.from_orm(lead_db)
    
    
    
    