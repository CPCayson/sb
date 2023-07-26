from sqlalchemy import Column, Integer, String, Boolean, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./test.db"  # Use SQL
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Thumbnail(Base):
    __tablename__ = "thumbnails"

    id = Column(String, primary_key=True)
    like = Column(Boolean, default=False)
    dislike = Column(Boolean, default=False)
    bookmark = Column(Boolean, default=False)
