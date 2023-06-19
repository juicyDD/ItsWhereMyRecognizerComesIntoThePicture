import torch
import os
import multiprocessing
TRAIN_DATASET_DIR = r"D:\SpeechDataset\train\train-clean-100" #train-clean-100 of LibriSpeech has 251 different speakers
TEST_DATASET_DIR = r"D:\SpeechDataset\test\LibriSpeech\test-clean"

# PRETRAINED_MODEL = r"D:\DATN\currentcode_secondenvironment\models_transformer_mfcc_100k_specaug\saved_model.ckpt-100000.pt"
PRETRAINED_MODEL =''
# SAVED_MODEL_PATH = '/app/models/saved_model.pt'

SAVED_MODEL_PATH = r"voicerecognizer\models_lstm_mfcc_100k_specaug_batch_8\saved_model.pt"

# SAVED_MODEL_PATH = "models\saved_model.pt"
N_MFCC = 40

SEQ_LENGTH = 100  #1 ele = 512 samples; 100~3.2 seconds

# Whether we are going to train with SpecAugment
SPECAUG_TRAINING = True

# Parameters for SpecAugment training.
SPECAUG_FREQ_MASK_PROB = 0.3
SPECAUG_TIME_MASK_PROB = 0.3
SPECAUG_IMAGE_WARP_PROB = 0

SPECAUG_FREQ_MASK_MAX_WIDTH = N_MFCC // 5
SPECAUG_TIME_MASK_MAX_WIDTH = SEQ_LENGTH // 5
SPECAUG_IMAGE_WARP_MAX_WIDTH = SEQ_LENGTH // 5

# How many triplets do we train in a single batch.
BATCH_SIZE = 8

# Learning rate.
LEARNING_RATE = 0.0001

# Whether to use GPU or CPU.
DEVICE = torch.device("cpu") #"cuda:0" if torch.cuda.is_available() else 

#hidden states vs hidden layers: https://stackoverflow.com/questions/63294347/difference-between-hidden-dimension-and-n-layers-in-rnn-using-pytorch 
# Hidden size of LSTM layers.
LSTM_HIDDEN_SIZE = 64

# Number of LSTM layers.
LSTM_NUM_LAYERS = 3

# Whether to use bi-directional LSTM.
BI_LSTM = True

# False = use last frame of LSTM inference as output
# True = use mean frame of LSTM inference as aggregated output
FRAME_AGGREGATION_MEAN = True

# True = use transformer instead of LSTM.
USE_TRANSFORMER = False

# Dimension of transformer layers.
TRANSFORMER_DIM = 32

# Number of encoder layers for transformer
TRANSFORMER_ENCODER_LAYERS = 2

# Number of heads in transformer layers.
TRANSFORMER_HEADS = 8


# Whether to use full sequence inference or sliding window inference.
FULL_SEQUENCE_INFERENCE = False

# Sliding window step for sliding window inference.
SLIDING_WINDOW_STEP = 50  # 1.6 seconds

NUM_EVAL_TRIPLETS = 10000

# Triplet loss, Alpha hyperparam
TRIPLET_ALPHA = 0.1

#Equal Error Rate threshold step
EER_THRESHOLD_STEP = 0.001 

# Training steps
TRAINING_STEPS = 100000

# Number of processes for multi-processing.
NUM_PROCESSES = min(multiprocessing.cpu_count(), BATCH_SIZE)

# SAVED_MODEL_PATH = r"C:\Users\DELL\Desktop\DATN\currentcode_secondenvironment\models\saved_model.pt"

# Save a model to disk every these many steps.
SAVE_MODEL_FREQUENCY = 10000