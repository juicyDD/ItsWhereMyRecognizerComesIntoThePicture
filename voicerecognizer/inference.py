import torch
import numpy as np

from . import features_extraction, nhi_config
# from base.api.voice_recognizer.my_neural_network import MyEncoder


#---get embedding of a single utterance
def my_inference(features, encoder, is_full_sequence_inference = nhi_config.FULL_SEQUENCE_INFERENCE):
    if is_full_sequence_inference:
        batch_input = torch.unsqueeze(torch.from_numpy(features), dim=0).float().to(nhi_config.DEVICE)
        batch_output = encoder(batch_input)
        return batch_output[0, :].cpu().data.numpy()
    
    else:
        windows = features_extraction.extract_sliding_windows(features)
        if not windows:
            return None
        batch_input = torch.from_numpy(
            np.stack(windows)).float().to(nhi_config.DEVICE)
        batch_output = encoder(batch_input)

        #------Aggregate the inference outputs from sliding windows
        aggregated_output = torch.mean(batch_output, dim=0, keepdim=False).cpu()
        return aggregated_output.data.numpy()



# if __name__ == '__main__':
#     # x = torch.tensor([1,2,3,4])
#     # print(torch.unsqueeze(x,dim=0))
#     tempdir = r"D:\SpeechDataset\test\LibriSpeech\test-clean\672\122797\672-122797-0004.flac"
#     # tempdir=r"D:\DATN\myassistant\microphone-results2.flac"
#     temp = features_extraction.extract_mfcc(tempdir)
#     # encoder = get_speaker_encoder(nhi_config.SAVED_MODEL_PATH)
#     encoder = MyEncoder().encoder
#     embedding_temp = my_inference(temp, encoder)
    
#     tempdir2 = r"D:\SpeechDataset\test\LibriSpeech\test-clean\2830\3980\2830-3980-0008.flac"
#     # tempdir2=r"D:\DATN\myassistant\microphone-results.flac"
#     temp2 = features_extraction.extract_mfcc(tempdir2)
#     embedding_temp2 = my_inference(temp2, encoder)
    
    
#     print(embedding_temp)
#     print("shape: ", embedding_temp.shape)
#     # print("cos similarity: ", cosine_similarity(embedding_temp, embedding_temp2))
