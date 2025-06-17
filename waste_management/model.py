import os
import numpy as np
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from PIL import UnidentifiedImageError, Image  # Import PIL to handle image errors

# Load pre-trained MobileNetV2
base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

# Add custom classification layers
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(1024, activation='relu')(x)  # Dense layer with 1024 units
predictions = Dense(5, activation='softmax')(x)  # 5 categories for waste types

# Build the model
model = Model(inputs=base_model.input, outputs=predictions)

# Freeze the base model layers
for layer in base_model.layers:
    layer.trainable = False

# Compile the model
model.compile(optimizer=Adam(learning_rate=0.001), loss='categorical_crossentropy', metrics=['accuracy'])

# Function to check for valid images
def verify_image(file_path):
    try:
        img = Image.open(file_path)
        img.verify()  # Verify if it's a valid image
        img.close()  # Close the image file after verifying
        return True
    except (UnidentifiedImageError, OSError):  # Catch invalid image or OS-related errors
        print(f"Skipping invalid image: {file_path}")
        return False

# Clean the dataset by filtering valid images
def clean_dataset(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if not verify_image(file_path):
                os.remove(file_path)  # Remove invalid images from the directory

# Clean training and validation datasets
clean_dataset('waste_management/waste_dataset/train')
clean_dataset('waste_management/waste_dataset/val')

# Image data generators for training and validation datasets
train_datagen = ImageDataGenerator(rescale=1./255, rotation_range=30, zoom_range=0.2, horizontal_flip=True)
val_datagen = ImageDataGenerator(rescale=1./255)

# Load training and validation datasets
train_generator = train_datagen.flow_from_directory('waste_management/waste_dataset/train', target_size=(224, 224), batch_size=32, class_mode='categorical')
val_generator = val_datagen.flow_from_directory('waste_management/waste_dataset/val', target_size=(224, 224), batch_size=32, class_mode='categorical')

# Train the model
model.fit(train_generator, epochs=10, validation_data=val_generator)

# Save the trained model
model.save('waste_classification_model.h5')
