# ...existing code...
from fastapi import FastAPI, File, UploadFile, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import tensorflow as tf
from tensorflow.keras.models import load_model
import numpy as np
import json
import cv2
import os

# ------------------------
# FastAPI App Setup
# ------------------------
app = FastAPI()
# Allow CORS for a React frontend (adjust origins in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# ------------------------
# Load Model and Class Map
# ------------------------
MODEL_PATH = "saved_models/vgg16_medical.h5"
CLASS_MAP_PATH = "saved_models/classes.json"
IMG_SIZE = (224, 224)

model = load_model(MODEL_PATH)

with open(CLASS_MAP_PATH, "r") as f:
    class_map = json.load(f)
# inverse mapping: index -> class name
inv_class_map = {v: k for k, v in class_map.items()}

# ensure upload folder exists
UPLOAD_DIR = "app/static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# ------------------------
# HTML Routes (for browser)
# ------------------------
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "result": None})


@app.post("/predict", response_class=HTMLResponse)
async def predict(request: Request, file: UploadFile = File(...)):
    try:
        contents = await file.read()
        np_arr = np.frombuffer(contents, np.uint8)
        bgr_image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        if bgr_image is None:
            raise ValueError("Could not decode image")

        rgb_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)
        resized = cv2.resize(rgb_image, IMG_SIZE)
        img_array = np.expand_dims(resized / 255.0, axis=0)

        preds = model.predict(img_array)
        probs = preds[0]

        top_idx = int(np.argmax(probs))
        pred_class = inv_class_map[top_idx]
        confidence = float(np.max(probs)) * 100.0

        filename = os.path.basename(file.filename)
        save_path = os.path.join(UPLOAD_DIR, filename)
        cv2.imwrite(save_path, bgr_image)

        result_text = f"🩺 Prediction: {pred_class} ({confidence:.2f}%)"
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "result": result_text, "filename": filename},
        )

    except Exception as e:
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "result": f"Error: {str(e)}"},
        )


# ------------------------
# JSON API for React frontend
# ------------------------
@app.post("/api/predict")
async def api_predict(file: UploadFile = File(...)):
    """
    Accepts multipart/form-data with an 'file' field and returns JSON:
    { "label": "...", "confidence": 92.34, "filename": "..." }
    """
    try:
        contents = await file.read()
        np_arr = np.frombuffer(contents, np.uint8)
        bgr_image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        if bgr_image is None:
            raise HTTPException(status_code=400, detail="Could not decode image")

        rgb_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)
        resized = cv2.resize(rgb_image, IMG_SIZE)
        img_array = np.expand_dims(resized / 255.0, axis=0)

        preds = model.predict(img_array)
        probs = preds[0]

        top_idx = int(np.argmax(probs))
        pred_class = inv_class_map[top_idx]
        confidence = float(np.max(probs)) * 100.0

        filename = os.path.basename(file.filename)
        save_path = os.path.join(UPLOAD_DIR, filename)
        cv2.imwrite(save_path, bgr_image)

        return {
            "label": pred_class,
            "confidence": round(confidence, 2),
            "filename": filename,
            # "probs": probs.tolist()  # optional
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
# ...existing code...