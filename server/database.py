from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


DATABASE_URL="postgresql://postgres:Password%40123@localhost:5432/Music-app"

engine=create_engine(DATABASE_URL)
SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)

def get_db():
 db=SessionLocal()
 try:
  yield db
 finally:
  db.close()