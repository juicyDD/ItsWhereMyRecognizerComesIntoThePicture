from . import my_neural_network, features_extraction, inference
from sklearn.cluster import KMeans
import numpy as np
def get_voiceprint(utterances_arr,results, callback_=None):
    kmeans_ = len(utterances_arr) if len(utterances_arr) < 5 else 5
    encoder = my_neural_network.MyEncoder().encoder
    embeddings = []
    mean_vecs = []
    
    for audio_file in utterances_arr:
        # print(audio_file,":")
        features = features_extraction.extract_mfcc(audio_file)
        embedding = inference.my_inference(features, encoder)
        if embedding is not None:
            embeddings.append(embedding)
    
    classify_results = k_means_clustering(embeddings, kmeans_)
    mean_vecs = get_means(embeddings, classify_results, kmeans_)
    results.append(mean_vecs)
    if callback_ is not None:
        callback_()
    print('Results:',results)
    # return mean_vecs
    
"""phân loại giọng nói của speaker vào 5 cluster"""        
def k_means_clustering(embeddings, k=5):
    kmeans = KMeans(n_clusters=k, random_state=0, n_init=10).fit(embeddings)
    return kmeans.labels_
"""Sau khi đánh nhãn cluster thì tìm vector mean của mỗi cluster"""

def get_means(embeddings, classify_results, num_k):
    means = []
    # print(len(embeddings),len(embeddings[0]))
    for i in range(num_k):
        # print('Mean voiceprint of cluster',i,":")
        indices = np.argwhere(classify_results==i)
        indices = np.squeeze(indices)
        embeddings_by_cluster = np.array(embeddings)[indices].reshape(128,-1)
        mean_vec = np.mean(embeddings_by_cluster, axis=1)
        # print(mean_vec)
        means.append(mean_vec)
        # print(np.mean(embeddings_by_cluster, axis=1).shape)
        # vector_mean = np.mean(np.array(embeddings)[indices])
        # means.append(vector_mean)
    # print(means)
    return means
        
# encoder = my_neural_network.MyEncoder()
    
"""Uyen Nhi on the dotted line"""