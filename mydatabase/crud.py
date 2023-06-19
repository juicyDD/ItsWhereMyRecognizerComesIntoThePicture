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
    
    # _ = local_session.query(EmbeddingVector).filter(EmbeddingVector.speaker_ssn==speaker_ssn).all()
    
    # '''Nếu embedding của speaker này đã có trong db thì drop trước khi lưu các cluster mới vào db'''
    # if _ is not None:
    #     local_session.delete(_)
    #     local_session.commit()
    i=1
    local_session = Session(bind=engine)
    
    for emb in embeddings:
        
        new_embedding = EmbeddingVector(embedding=arrayToString(emb),speaker_ssn=speaker_ssn)
        local_session.add(new_embedding)
        local_session.commit()
    
        print('Added successfully',i)
        i+=1
    
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
