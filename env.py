from sqlalchemy.orm import declarative_base,sessionmaker
from sqlalchemy import Column,String,DateTime,Integer,create_engine
from datetime import datetime
import os

BASE_DIR=os.path.dirname(os.path.realpath(__file__))

GLOBAL_THRESHOLD = 0.577
connection_string="sqlite:///"+'mydatabase/site.db'

Base=declarative_base()
engine=create_engine(connection_string,echo=True)
Session=sessionmaker()