from sqlalchemy.orm import declarative_base,sessionmaker
from sqlalchemy import Column,String,DateTime,Integer,create_engine
from datetime import datetime
import os


BASE_DIR=os.path.dirname(os.path.realpath(__file__))

connection_string="sqlite:///"+os.path.join(BASE_DIR,'mydb.db')

Base=declarative_base()

engine=create_engine(connection_string,echo=True)

Session=sessionmaker()
    
class EmbeddingVector(Base):
    __tablename__ = 'embedding_vectors'
    
    id_ = Column('id',Integer, primary_key=True)
    embedding = Column('embedding',String)
    speaker_ssn = Column('speaker_ssn', String)
    
    def __init__(self,embedding,speaker_ssn):
        self.embedding = embedding
        self.speaker_ssn = speaker_ssn
    
    def __repr__(self):
        return f"Speaker id {self.id}: {self.embedding}"

class Being(Base):
    __tablename__ = 'beings'
    
    ssn = Column('ssn', String, primary_key=True)
    name = Column('name', String)
    speaker_id = Column ('speakerId',String)
    
    def __init__(self, ssn, name, speaker_id=None):
        self.ssn = ssn
        self.name = name
        self.speaker_id = speaker_id
    
    def __repr__(self):
        return f"{self.ssn}: {self.name}"
