from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Being(Base):
    __tablename__ = 'beings'
    
    ssn = Column('ssn', Integer, primary_key=True)
    name = Column('name', String)
    speaker_id = Column ('speakerId',String)
    
    def __init__(self, ssn, name, speaker_id=None):
        self.ssn = ssn
        self.name = name
        self.speaker_id = speaker_id
    
    def __repr__(self):
        return f"{self.ssn}: {self.name}"

engine = create_engine("sqlite:///mydb.db", echo=True)
# Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)

session = Session()


# being = Being(1, "K")
# session.add(being)
# session.commit()
# results =session.query(Being).all()
# print(results)
results = session.query(Being).filter(Being.name =='K')
for r in results:
    print(r)

# class VoiceEmbedding(Base):
#     __tablename__ = 'voiceEmbeddings'

"""Uyen Nhi on the dotted line"""