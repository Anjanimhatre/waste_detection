import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
from tensorflow.keras.applications.vgg16 import preprocess_input

# Load the trained model
model = tf.keras.models.load_model("model_checkpoint.keras")

# Define the function to preprocess the image
def preprocess_image(image):
    image = image.resize((150, 150))  # Resize image to match model input size
    image = np.array(image)  # Convert to numpy array
    image = preprocess_input(image)  # Apply VGG16 preprocessing
    image = np.expand_dims(image, axis=0)  # Expand dimensions for batch processing
    return image

# Define the Streamlit UI
st.title("Waste Classification using Deep Learning")
st.write("Upload an image to classify it as Organic or Recyclable waste.")

# Upload image
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    
    # Preprocess the image
    processed_image = preprocess_image(image)
    
    # Predict using the model
    prediction = model.predict(processed_image)[0][0]
    
    # Display classification result
    category = "Organic Waste" if prediction < 0.5 else "Recyclable Waste"
    confidence = (1 - prediction) if prediction < 0.5 else prediction
    
    st.write(f"Prediction: **{category}**")
    st.write(f"Confidence: **{confidence * 100:.2f}%**")

st.write("Developed ❤️ by Anjani and Team")
