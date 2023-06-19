import soundfile as sf
import librosa

from . import nhi_config
# import nhi_config

'''read an arbitrary *.flac file, return waveform and sample rate'''
def read_audio(audio_dir):
    waveform, sample_rate = sf.read(audio_dir)
    
    #if number of channels of the target audio file is greater than 1
    if len(waveform.shape)>1: 
        waveform = librosa.to_mono(waveform.transpose())
        
    # Convert to 16kHz.
    if sample_rate != 16000:
        # print(sample_rate)
        waveform = librosa.resample(waveform, orig_sr=sample_rate, target_sr=16000)
        sample_rate = 16000
    return waveform, sample_rate
    
'''extract mfcc feature from an audio file, a frame = 512 samples'''
def extract_mfcc(audio_dir):
    waveform, sample_rate = read_audio(audio_dir)
    
    #mfcc standard frame length = 512 samples
    features = librosa.feature.mfcc(y=waveform, sr=sample_rate, n_mfcc=nhi_config.N_MFCC)
    return features.transpose()

'''Extract sliding windows from features, dùng cho sliding window inference'''
def extract_sliding_windows(features):
    windows = []
    start_idx = 0
    while (start_idx + nhi_config.SEQ_LENGTH) <= features.shape[0]:
        _ = features[start_idx: (start_idx + nhi_config.SEQ_LENGTH), :]
        windows.append(_)
        start_idx += nhi_config.SLIDING_WINDOW_STEP
    return windows


