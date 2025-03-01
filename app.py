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
    "Drop up to 3 pics of men (solo or groups), we’ll judge their whole deal",
    type=["jpg", "png", "jpeg"],
    accept_multiple_files=True
)

if uploaded_files and len(uploaded_files) <= 3:
    # Display uploaded images in a single row
    st.subheader("The Contenders")
    cols = st.columns(len(uploaded_files))
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

    # Button-specific prompts
    prompts = {
        "Rate": (
            f"You’re a balanced, no-nonsense critic. These {len(uploaded_files)} images show men (solo or groups). "
            f"For each man (label as Man 1, Man 2, etc., across images), analyze their overall appeal—outfit, facial features, expression, vibe, etc. "
            f"Rate each out of 10 for these groups: {', '.join(categories)}, reflecting how a typical Indian woman might judge them as of March 2025. "
            f"Explain briefly with neutral reasoning. Rank them (1st, 2nd, etc.) per category with a quick comparison."
        ),
        "Unhinged Rating": (
            f"You’re a wild, unhinged critic. These {len(uploaded_files)} images show men (solo or groups). "
            f"For each man (label as Man 1, Man 2, etc.), analyze their outfit, face, expression, vibe—everything—with over-the-top flair. "
            f"Rate each out of 10 for these groups: {', '.join(categories)}, based on extreme Indian women’s preferences in 2025. "
            f"Go crazy with reasoning—exaggerate likes and dislikes. Rank them (1st, 2nd, etc.) per category with savage comparisons."
        ),
        "Feedback": (
            f"You’re a blunt but helpful critic. These {len(uploaded_files)} images show men (solo or groups). "
            f"For each man (label as Man 1, Man 2, etc.), analyze their outfit, facial features, expression, vibe, etc. "
            f"Give detailed feedback on what they can improve—style, grooming, posture, whatever stands out—for appeal to these groups: {', '.join(categories)}. "
            f"Keep it raw and practical, based on 2025 Indian trends."
        ),
        "Roast Me Dead": (
            f"You’re a merciless roasting machine. These {len(uploaded_files)} images show men (solo or groups). "
            f"For each man (label as Man 1, Man 2, etc.), tear apart their outfit, face, expression, vibe—everything. "
            f"Rate each out of 10 for these groups: {', '.join(categories)}, but focus on brutal, lowest-blow roasting. "
            f"Rank them (1st, 2nd, etc.) per category with the harshest comparisons imaginable. No mercy, 2025 Indian style."
        )
    }

    # Buttons for different analyses
    st.subheader("Pick Your Poison")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        rate_btn = st.button("Rate")
    with col2:
        unhinged_btn = st.button("Unhinged Rating")
    with col3:
        feedback_btn = st.button("Feedback")
    with col4:
        roast_btn = st.button("Roast Me Dead")

    # Handle button clicks
    selected_prompt = None
    if rate_btn:
        selected_prompt = prompts["Rate"]
    elif unhinged_btn:
        selected_prompt = prompts["Unhinged Rating"]
    elif feedback_btn:
        selected_prompt = prompts["Feedback"]
    elif roast_btn:
        selected_prompt = prompts["Roast Me Dead"]

    if selected_prompt:
        content = [{"text": selected_prompt}] + image_data
        try:
            with st.spinner("AI is judging these clowns..."):
                response = model.generate_content(
                    content,
                    generation_config={
                        "temperature": 1.0,  # Max creativity
                        "max_output_tokens": 1000  # Detailed output
                    }
                )
            st.subheader("Unhinged AI Verdict")
            st.markdown(response.text)
        except Exception as e:
            st.error(f"AI choked: {str(e)}")
            st.write("Check logs or ensure men are visible.")

    # Unsplash comparison
    url = "https://source.unsplash.com/random/300x200/?man,fashion"
    st.image(url, caption="Trend check—how they stack up")

elif uploaded_files and len(uploaded_files) > 3:
    st.error("Chill, bro—max 3 images. Pick your best shots.")
