from .models import Being,EmbeddingVector, Session,engine
def createBeing(ssn,name,speaker_id=None):
    local_session=Session(bind=engine)
    
    new_being = Being(ssn=ssn,name=name,speaker_id=speaker_id)
    local_session.add(new_being)

    local_session.commit()
    print('user added')
def getAllBeings():
    local_session=Session(bind=engine)
    beings = local_session.query(Being).all()
    return beings
def createEmbedding(embeddings, speaker_ssn):
    i=1
    local_session = Session(bind=engine)
    
    for emb in embeddings:
        
        new_embedding = EmbeddingVector(embedding=arrayToString(emb),speaker_ssn=speaker_ssn)
        local_session.add(new_embedding)
        local_session.commit()
    
        print('Added successfully',i)
        i+=1

def deleteBeing(ssn):
    local_session=Session(bind=engine)
    item_to_delete=local_session.query(Being).filter(Being.ssn==ssn).first()
    local_session.delete(item_to_delete)
    local_session.commit()   
    
def deleteEmbeddingsBySSn(ssn):
    local_session=Session(bind=engine)
    embs_to_delete=local_session.query(EmbeddingVector).filter(EmbeddingVector.speaker_ssn==ssn)
    for emb in embs_to_delete:
        local_session.delete(emb)
    local_session.commit()
def arrayToString(embedding):
    embeddingstr = ''
    for _ in embedding:
        embeddingstr+= str(_)
        embeddingstr+= '//'
    return embeddingstr

def stringToArray(embeddingstr):
    embedding = embeddingstr.split('//')
    result = []
    for bar in embedding:
        try:
            bar = float(bar)
            result.append(bar)
        except (Exception) as error:
            continue
    return result
    
"""Uyen Nhi on the dotted line"""
