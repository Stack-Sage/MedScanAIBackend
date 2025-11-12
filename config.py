# ==== Configuration Settings ====

# Dataset paths
TRAIN_DIR = "dataset/train"
VAL_DIR = "dataset/val"

# Model saving
MODEL_SAVE_PATH = "saved_models/vgg16_medical.h5"
CLASS_MAP_PATH = "saved_models/classes.json"

# Model params
IMG_SIZE = (224, 224)
BATCH_SIZE = 16
EPOCHS = 20
LEARNING_RATE = 1e-4
FINE_TUNE_AT = 15  # unfreeze last 15 layers for fine-tuning

# R-CNN params
PROPOSAL_STEP = 64
CONF_THRESH = 0.5
