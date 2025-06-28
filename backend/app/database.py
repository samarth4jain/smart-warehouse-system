from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# For development, use SQLite if PostgreSQL is not available
DB_TYPE = os.getenv('DB_TYPE', 'sqlite')

if DB_TYPE == 'sqlite':
    # SQLite database for development
    DATABASE_URL = "sqlite:///./smart_warehouse.db"
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    # PostgreSQL database for production
    DATABASE_URL = f"postgresql://{os.getenv('DB_USER', 'warehouse_user')}:{os.getenv('DB_PASSWORD', 'warehouse_password')}@{os.getenv('DB_HOST', 'localhost')}:{os.getenv('DB_PORT', '5432')}/{os.getenv('DB_NAME', 'smart_warehouse')}"
    engine = create_engine(DATABASE_URL)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class
Base = declarative_base()

# Metadata
metadata = MetaData()

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
