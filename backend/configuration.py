from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base

url = "mysql+pymysql://root:GKmQ12@localhost:3206/db"

engine = create_engine(url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
