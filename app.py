import streamlit as st
import requests
from PIL import Image
import google.generativeai as genai
import base64
from io import BytesIO

# Configure Gemini API (replace with your key)
GEMINI_API_KEY = "AIzaSyCtKdRGeA03fVIWKSJtko__ZBDE24Dys9g"
genai.configure(api_key=AIzaSyCtKdRGeA03fVIWKSJtko__ZBDE24Dys9g)

# Initialize Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")

st.title("RawRater - Unfiltered Style Check")

# Upload image
uploaded_file = st.file_uploader("Drop your pic, we’ll shred it", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # Load and display image
    image = Image.open(uploaded_file)
    st.image(image, caption="This is you, huh?")

    # Convert image to base64 for Gemini API
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    img_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

    # Categories to evaluate
    categories = [
        "Modern Indian Women",
        "Traditional Indian Women",
        "College Indian Women",
        "Intellectual Women",
        "Adventure-Seeking Women"
    ]

    # Craft prompt for Gemini
    prompt = (
        f"Analyze this image of a person's outfit and provide unfiltered, savage, detailed feedback "
        f"for how these groups would rate it out of 10: {', '.join(categories)}. "
        f"Explain the reasoning for each rating based on style, vibe, and trends. "
        f"Keep it raw and honest. Image data: [image]"
    )

    # Send request to Gemini with image and text
    response = model.generate_content(
        [prompt, {"mime_type": "image/png", "data": img_base64}],
        generation_config={
            "temperature": 0.9,  # High creativity
            "max_output_tokens": 500  # Detailed output
        }
    )

    # Display AI-generated feedback
    st.subheader("Unhinged AI Feedback")
    st.write(response.text)

    # Unsplash comparison
    url = "https://source.unsplash.com/random/300x200/?fashion"
    st.image(url, caption="Trend check—how you stack up")
