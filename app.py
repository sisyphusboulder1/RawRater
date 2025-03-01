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

st.title("RawRater - Unfiltered Style Showdown")

# Multiple photo upload (up to 3)
uploaded_files = st.file_uploader(
    "Drop up to 3 pics of people in outfits, we’ll shred their style",
    type=["jpg", "png", "jpeg"],
    accept_multiple_files=True
)

if uploaded_files and len(uploaded_files) <= 3:
    # Display uploaded images in a single row
    st.subheader("Your Contenders")
    cols = st.columns(len(uploaded_files))  # Create columns based on number of images
    image_data = []
    for i, (col, uploaded_file) in enumerate(zip(cols, uploaded_files), 1):
        image = Image.open(uploaded_file)
        col.image(image, caption=f"Outfit {i}", use_column_width=True)  # Display in column
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

    # Refined prompt for clothing focus
    prompt = (
        f"You are an unfiltered, savage fashion critic. These {len(uploaded_files)} images show people wearing outfits. "
        f"Analyze the clothing on each person (label them Outfit 1, Outfit 2, etc., matching upload order). "
        f"For each outfit, give a detailed breakdown of the style, vibe, colors, fit, and overall impression—focus only on what they’re wearing. "
        f"Rate each outfit out of 10 for these groups: {', '.join(categories)}. "
        f"Explain the reasoning for each rating with brutal honesty, drawing from fashion trends, cultural preferences, and raw reactions as of March 2025. "
        f"Then, rank the outfits (1st, 2nd, 3rd) for each category, comparing them head-to-head and explaining why one outshines the others. "
        f"Push the detail to the max—roast the bad, hype the good, no holding back. Here are the images:"
    )

    # Structure content
    content = [{"text": prompt}] + image_data

    # Send request to Gemini with error handling
    try:
        with st.spinner("AI is ripping your style apart..."):
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
        st.write("Check the logs or try clearer images with visible outfits.")

    # Unsplash comparison
    url = "https://source.unsplash.com/random/300x200/?fashion"
    st.image(url, caption="Trend check—how you stack up to the pros")

elif uploaded_files and len(uploaded_files) > 3:
    st.error("Chill, bro—max 3 outfits. Pick your best shots.")
