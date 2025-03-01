import streamlit as st
import requests
from PIL import Image
import google.generativeai as genai
import base64
from io import BytesIO

# Configure Gemini API
GEMINI_API_KEY = "AIzaSyCtKdRGeA03fVIWKSJtko__ZBDE24Dys9g"  # Replace with your key
genai.configure(api_key=GEMINI_API_KEY)

# Initialize Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")

st.title("RawRater - Unfiltered Man Showdown")

# Multiple photo upload (up to 3)
uploaded_files = st.file_uploader(
    "Drop up to 3 pics of men (solo or groups), we’ll shred their whole vibe",
    type=["jpg", "png", "jpeg"],
    accept_multiple_files=True
)

if uploaded_files and len(uploaded_files) <= 3:
    # Display uploaded images in a single row
    st.subheader("The Contenders")
    cols = st.columns(len(uploaded_files))  # Horizontal layout
    image_data = []
    for i, (col, uploaded_file) in enumerate(zip(cols, uploaded_files), 1):
        image = Image.open(uploaded_file)
        col.image(image, caption=f"Image {i}", use_column_width=True)
        # Convert to base64
        buffer = BytesIO()
        image.save(buffer, format="PNG")
        img_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
        image_data.append({"mime_type": "image/png", "data": img_base64})

    # Categories to evaluate
    categories = [
        "Modern Indian Women",
        "Traditional Indian Women",
        "College Indian Women",
        "Intellectual Women",
        "Adventure-Seeking Women"
    ]

    # Comprehensive prompt for full analysis
    prompt = (
        f"You are an unfiltered, savage critic of men’s overall appeal. These {len(uploaded_files)} images contain men (solo or multiple per image). "
        f"For each man visible, analyze EVERYTHING women notice: outfit (style, fit, colors), facial features (jawline, eyes, etc.), expression (confident, aloof, etc.), "
        f"body language, vibe, and any other traits that stand out. Label them as Man 1, Man 2, etc., across all images (e.g., Image 1 might have Man 1 and Man 2, Image 2 has Man 3). "
        f"Rate each man out of 10 for these groups: {', '.join(categories)}. "
        f"Provide a detailed, brutal breakdown for each rating—explain how their look, vibe, and presence hit or miss based on fashion trends, cultural preferences, and raw attraction as of March 2025. "
        f"Then, rank all identified men (1st, 2nd, 3rd, etc.) for each category, comparing them head-to-head and justifying why one outshines the others. "
        f"Maximize the detail—roast the weak, hype the strong, no mercy. Here are the images:"
    )

    # Structure content
    content = [{"text": prompt}] + image_data

    # Send request to Gemini with error handling
    try:
        with st.spinner("AI is tearing these dudes apart..."):
            response = model.generate_content(
                content,
                generation_config={
                    "temperature": 1.0,  # Max creativity
                    "max_output_tokens": 1000  # Detailed output
                }
            )
        st.subheader("Unhinged AI Showdown")
        st.markdown(response.text)
    except Exception as e:
        st.error(f"AI choked: {str(e)}")
        st.write("Check the logs or ensure men are visible in the images.")

    # Unsplash comparison (generic male style)
    url = "https://source.unsplash.com/random/300x200/?man,fashion"
    st.image(url, caption="Trend check—how they stack up to the pros")

elif uploaded_files and len(uploaded_files) > 3:
    st.error("Chill, bro—max 3 images. Pick your best shots.")
