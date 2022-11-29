import sqlalchemy
import sqlalchemy.ext.declarative
import sqlalchemy.orm

DATABASE_URL = "sqlite:///./database.db"

engine = sqlalchemy.create_engine(DATABASE_URL, connect_args = {"check_same_thread": False})

SessionLocal = sqlalchemy.orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = sqlalchemy.ext.declarative.declarative_base()



