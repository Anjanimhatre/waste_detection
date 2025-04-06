import numpy as np
import streamlit as st
import tensorflow as tf
from PIL import Image
import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key="AIzaSyCC9Q07JTA-Kc0xCFZltYHQGrYsiSjDePk")  # Replace with actual API key

# Load trained waste classification model
model = tf.keras.models.load_model("model_checkpoint.keras")  

# Define class labels
class_labels = {0: "Organic Waste", 1: "Recyclable Waste"}

# Function to get recycling suggestions using Gemini API
def get_recycling_suggestions():
    prompt = "Suggest creative ways to upcycle plastic bottles, cans, glass, or paper."
    
    try:
        model = genai.GenerativeModel("models/gemini-1.5-pro-latest")  
        response = model.generate_content(prompt)
        return response.text if response and hasattr(response, "text") else "No suggestions available."
    except Exception as e:
        return f"Error fetching suggestions: {str(e)}"

# Function to preprocess image for model
def preprocess_image(image):
    image = image.convert("RGB")  # Convert to RGB
    image = image.resize((150, 150))  # Resize to model input size
    image = np.array(image) / 255.0  # Normalize pixel values
    image = np.expand_dims(image, axis=0)  # Add batch dimension
    return image

# Streamlit UI
st.title("♻️ Smart Waste Classification & Recycling Assistant")

uploaded_file = st.file_uploader("📤 Upload a waste image", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # Display uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Waste Image", use_column_width=True)

    # Preprocess the image
    processed_image = preprocess_image(image)

    # Predict using the model
    prediction = model.predict(processed_image)
    prediction_score = prediction[0][0]  # Get probability

    # Print raw output to debug
    st.write(f"🔍 **Raw Model Prediction:** {prediction_score:.4f}")

    # Determine class
    threshold = 0.5
    predicted_class = 1 if prediction_score > threshold else 0
    waste_type = class_labels[predicted_class]

    # Display prediction
    st.subheader(f"🗑️ **Prediction: {waste_type}**")

    # Show suggestions only for recyclable waste
    if predicted_class == 1:
        st.subheader("♻️ Upcycling & Recycling Ideas:")
        suggestions = get_recycling_suggestions()
        st.write(suggestions)