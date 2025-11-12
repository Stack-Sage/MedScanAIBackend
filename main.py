import argparse
import json
import os
import cv2
import tensorflow as tf
import gdown
from config import *
from data.dataloader import make_generators
from model.build_vgg16 import build_vgg_classifier
from train.trainer import train_classifier
from inference.inferencer import classify_image

# ======================================================
# ⚙️ Configuration
# ======================================================
MODEL_DIR = "saved_models"
MODEL_NAME = "vgg16_medical.h5"
MODEL_SAVE_PATH = os.path.join(MODEL_DIR, MODEL_NAME)
os.makedirs(MODEL_DIR, exist_ok=True)

# 🔗 Google Drive model info (replace with your own)
FILE_ID = "1h6HIRU2gwGQMJTLCxvHWNtWzjQpq_ZFP"
URL = f"https://drive.google.com/uc?id={FILE_ID}"

# ======================================================
# 🧠 Model Handling Utilities
# ======================================================
def ensure_model_downloaded():
    """
    Downloads model from Google Drive if not already cached locally.
    Ensures file integrity and sufficient size (>100 MB sanity check).
    """
    if os.path.exists(MODEL_SAVE_PATH):
        size_mb = os.path.getsize(MODEL_SAVE_PATH) / 1e6
        if size_mb > 100:
            print(f"✅ Model cached ({size_mb:.2f} MB). Skipping download.")
            return
        else:
            print(f"⚠️ Cached file too small ({size_mb:.2f} MB). Re-downloading...")

    print("⬇️ Downloading model from Google Drive...")
    gdown.download(URL, MODEL_SAVE_PATH, quiet=False, fuzzy=True)

    if not os.path.exists(MODEL_SAVE_PATH):
        raise FileNotFoundError("❌ Download failed — file not found.")

    size_mb = os.path.getsize(MODEL_SAVE_PATH) / 1e6
    if size_mb < 100:
        raise ValueError(
            f"❌ Download incomplete ({size_mb:.2f} MB). Check Google Drive link."
        )
    print(f"✅ Model downloaded successfully ({size_mb:.2f} MB).")

def load_model_cached(input_shape, num_classes):
    """
    Ensures model exists, loads it into memory (cached), and returns it.
    """
    ensure_model_downloaded()
    print("⚙️ Loading model into memory...")
    model = build_vgg_classifier(input_shape, num_classes)
    model.load_weights(MODEL_SAVE_PATH)
    print("✅ Model loaded and ready.")
    return model

# ======================================================
# 🧪 Inference / Training Entry Point
# ======================================================
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["train", "infer"], required=True)
    parser.add_argument("--image", help="Path to image for inference")
    args = parser.parse_args()

    # -----------------------------
    # TRAINING MODE
    # -----------------------------
    if args.mode == "train":
        train_gen, val_gen = make_generators(TRAIN_DIR, VAL_DIR, IMG_SIZE, BATCH_SIZE)
        model = build_vgg_classifier(
            (*IMG_SIZE, 3), len(train_gen.class_indices), FINE_TUNE_AT
        )
        print("🧩 Classes detected:", train_gen.class_indices)

        train_classifier(
            model, train_gen, val_gen, MODEL_SAVE_PATH, CLASS_MAP_PATH, EPOCHS
        )
        print("✅ Training complete and model saved.")

    # -----------------------------
    # INFERENCE MODE
    # -----------------------------
    elif args.mode == "infer":
        if not args.image:
            raise ValueError("❌ Please provide an image path using --image")

        # Load class map
        if not os.path.exists(CLASS_MAP_PATH):
            raise FileNotFoundError("❌ Class map not found. Train first or add manually.")
        with open(CLASS_MAP_PATH) as f:
            class_map = json.load(f)
        inv_class_map = {v: k for k, v in class_map.items()}
        num_classes = len(class_map)

        # Load model (cached)
        model = load_model_cached((*IMG_SIZE, 3), num_classes)

        # Run inference
        detections = classify_image(MODEL_SAVE_PATH, CLASS_MAP_PATH, args.image, IMG_SIZE)
        print("🩺 Inference Result:", detections)

# ======================================================
# 🚀 Run Entry
# ======================================================
if __name__ == "__main__":
    main()
