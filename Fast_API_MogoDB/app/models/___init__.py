# 몽고DB 연결하기 위한 모듈 import
from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine
from app.config import MONGO_DB_NAME, MONGO_URL



class MongoDB:
    def __init__(self):
        self.client = None
        self.engine = None
        
    
    def connect(self):
        self.client = AsyncIOMotorClient(MONGO_URL)
        self.engine = AIOEngine(motr_client = self, database = MONGO_DB_NAME)
    
    def close(self):
        self.client.close()
        

mongodb = MongoDB()