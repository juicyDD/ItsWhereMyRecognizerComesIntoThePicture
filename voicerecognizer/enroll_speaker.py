from . import my_neural_network, features_extraction, inference
def get_voiceprint(utterances_arr):
    kmeans_ = len(utterances_arr) if len(utterances_arr) < 5 else 5
    encoder = my_neural_network.MyEncoder().encoder
    embeddings = []
    
    for audio_file in utterances_arr:
        print(audio_file,":")
        features = features_extraction.extract_mfcc(audio_file)
        embedding = inference.my_inference(features, encoder)
        print(embedding)
        
# encoder = my_neural_network.MyEncoder()
    
"""Uyen Nhi on the dotted line"""