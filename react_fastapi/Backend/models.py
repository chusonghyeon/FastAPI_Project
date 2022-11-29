import datetime
import sqlalchemy
import sqlalchemy.orm
import passlib.hash

import database

class User(database.Base):
    __tablename__ = "users"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key = True, index = True)
    email = sqlalchemy.Column(sqlalchemy.String, unique = True, index = True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String)
    
    leads = sqlalchemy.orm.relationship("Lead", back_populates = "owner")
    
    def verify_password(self, password: str):
        return passlib.hash.bcrypt.verify(password, self.hashed_password)
    
class Lead(database.Base):
    __tablename__ = "leads"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key = True, index = True)
    owner_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    first_name = sqlalchemy.Column(sqlalchemy.String, index = True)
    last_name = sqlalchemy.Column(sqlalchemy.String, index = True)
    email = sqlalchemy.Column(sqlalchemy.String, index = True)
    company =  sqlalchemy.Column(sqlalchemy.String, index = True, default = "")
    note = sqlalchemy.Column(sqlalchemy.String, default = "")
    date_created = sqlalchemy.Column(sqlalchemy.DateTime, default = datetime.datetime.utcnow)
    date_last_updated = sqlalchemy.Column(sqlalchemy.DateTime, default = datetime.datetime.utcnow)
    
    owner = sqlalchemy.orm.relationship("User", back_populates = "leads")
    