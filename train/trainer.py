import tensorflow as tf
import json
import os
from utils.helpers import save_class_indices

def train_classifier(model, train_gen, val_gen, model_path, class_map_path, epochs):
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    os.makedirs(os.path.dirname(class_map_path), exist_ok=True)

    # Save class map
    save_class_indices(train_gen.class_indices, class_map_path)

    callbacks = [
        tf.keras.callbacks.ModelCheckpoint(model_path, save_best_only=True, monitor='val_accuracy', mode='max'),
        tf.keras.callbacks.EarlyStopping(patience=5, restore_best_weights=True)
    ]

    history = model.fit(
        train_gen,
        validation_data=val_gen,
        epochs=epochs,
        callbacks=callbacks
    )

    print("Training complete. Model saved at:", model_path)
    return history
