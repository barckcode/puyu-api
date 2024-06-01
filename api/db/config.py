from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os


database_connection_string = os.getenv('DATABASE_CONNECTION_STRING')

engine = create_engine(f'postgresql+psycopg2://{database_connection_string}')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
