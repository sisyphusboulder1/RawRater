import streamlit as st
import requests
from PIL import Image
import google.generativeai as genai
import base64
from io import BytesIO

# Configure Gemini API (use your key)
GEMINI_API_KEY = "AIzaSyCtKdRGeA03fVIWKSJtko__ZBDE24Dys9g"  # Replace with your key
genai.configure(api_key=GEMINI_API_KEY)

# Initialize Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")

st.title("RawRater - Unfiltered Style Showdown")

# Multiple photo upload (up to 3)
uploaded_files = st.file_uploader(
    "Drop up to 3 pics, we’ll shred them and rank them", 
    type=["jpg", "png", "jpeg"], 
    accept_multiple_files=True
)

if uploaded_files and len(uploaded_files) <= 3:
    # Display uploaded images
    st.subheader("Your Contenders")
    images = []
    img_base64_list = []
    for i, uploaded_file in enumerate(uploaded_files, 1):
        image = Image.open(uploaded_file)
        st.image(image, caption=f"Outfit {i}")
        # Convert to base64 for Gemini
        buffer = BytesIO()
        image.save(buffer, format="PNG")
        img_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
        images.append({"mime_type": "image/png", "data": img_base64})
        img_base64_list.append(f"Outfit {i}")

    # Categories to evaluate
    categories = [
        "Modern Indian Women",
        "Traditional Indian Women",
        "College Indian Women",
        "Intellectual Women",
        "Adventure-Seeking Women"
    ]

    # Craft a detailed, savage prompt for Gemini
    prompt = (
        f"Analyze these {len(uploaded_files)} outfit images and provide unfiltered, savage, "
        f"detailed feedback for how these groups would rate each one out of 10: {', '.join(categories)}. "
        f"For each outfit, describe the style, vibe, colors, and overall impression in depth. "
        f"Explain the reasoning for each rating based on fashion trends, cultural preferences, and raw gut reactions. "
        f"Then, rank the outfits (1st, 2nd, 3rd) for each category with a brutal comparison—tell me why one beats the others. "
        f"Push the detail to the max—roast them, hype them, whatever’s real. "
        f"Label the outfits as Outfit 1, Outfit 2, etc., matching the order they’re uploaded. "
        f"Image data follows: [image1, image2, ...]"
    )

    # Combine prompt and images for Gemini
    content = [prompt] + images

    # Send request to Gemini
    with st.spinner("AI is tearing your style apart..."):
        response = model.generate_content(
            content,
            generation_config={
                "temperature": 1.0,  # Max creativity
                "max_output_tokens": 1000  # Super detailed output
            }
        )

    # Display AI-generated feedback
    st.subheader("Unhinged AI Showdown")
    st.markdown(response.text)

    # Unsplash comparison
    url = "https://source.unsplash.com/random/300x200/?fashion"
    st.image(url, caption="Trend check—how you stack up to the pros")

elif uploaded_files and len(uploaded_files) > 3:
    st.error("Chill, bro—max 3 outfits. Pick your best shots.")
