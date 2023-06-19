import numpy as np
import operator

from voicerecognizer import my_neural_network, features_extraction, inference
from mydatabase import crud
from env import GLOBAL_THRESHOLD


def cosine_similarity(x1,x2):
    return np.dot(x1,x2)/(np.linalg.norm(x1)*np.linalg.norm(x2))

def recognize_speaker(audio_file):
    similarities_dict = {}
    encoder = my_neural_network.MyEncoder().encoder
    
    features = features_extraction.extract_mfcc(audio_file)
    recognizing_embedding = inference.my_inference(features, encoder)
    
    if recognizing_embedding is None:
        return None
    
    enrolled_embeddings = crud.getAllEmbeddings()
    for emb in enrolled_embeddings:
        emb_arr = crud.stringToArray(emb.embedding)
        similarity_score = cosine_similarity(recognizing_embedding, emb_arr)
        
        if emb.speaker_ssn not in similarities_dict:
            similarities_dict[emb.speaker_ssn] = similarity_score
        elif similarities_dict[emb.speaker_ssn] < similarity_score:
            similarities_dict[emb.speaker_ssn] = similarity_score
            
    print(similarities_dict)
    max_similarity = max(similarities_dict.items(), key=operator.itemgetter(1))[1]
    keys = [k for k,v in similarities_dict.items() if v==max_similarity]
    print(keys[0], max_similarity)
    
    if max_similarity < GLOBAL_THRESHOLD:
        return None
    return keys[0]
    
# if __name__ == '__main__':
#     recognize_speaker(r"D:\SpeechDataset\test\LibriSpeech\test-clean\672\122797\672-122797-0072.flac")
    
    