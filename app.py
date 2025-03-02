import streamlit as st
import requests
from PIL import Image
import google.generativeai as genai
import base64
from io import BytesIO
from streamlit_cropper import st_cropper

# Configure Gemini API with your key
GEMINI_API_KEY = "AIzaSyCtKdRGeA03fVIWKSJtko__ZBDE24Dys9g"
genai.configure(api_key=GEMINI_API_KEY)

# Initialize Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")

# Initialize session state
if "mode" not in st.session_state:
    st.session_state.mode = None
if "cropped_images" not in st.session_state:
    st.session_state.cropped_images = []
if "image_data" not in st.session_state:
    st.session_state.image_data = []

st.title("RawRater - Unfiltered Man Showdown")

# Pre-upload choice: Individual or Group Rating
st.subheader("Choose Your Rating Mode")
col_mode1, col_mode2 = st.columns(2)
with col_mode1:
    if st.button("Individual Rating"):
        st.session_state.mode = "individual"
with col_mode2:
    if st.button("Group Rating"):
        st.session_state.mode = "group"

# Only show uploader and proceed if mode is selected
if st.session_state.mode is not None:
    upload_text = (
        "Drop 1 pic of a man to crop and judge his vibe" if st.session_state.mode == "individual"
        else "Drop up to 3 pics of men (solo or groups), crop them, and we’ll rank them"
    )

    # Multiple photo upload
    uploaded_files = st.file_uploader(
        upload_text,
        type=["jpg", "png", "jpeg"],
        accept_multiple_files=(st.session_state.mode == "group"),
        key="uploader"
    )

    # Only proceed if files are uploaded
    if uploaded_files is not None and len(uploaded_files) <= (1 if st.session_state.mode == "individual" else 3):
        # Process and crop images
        st.session_state.cropped_images = []
        st.session_state.image_data = []
        for i, uploaded_file in enumerate(uploaded_files, 1):
            img = Image.open(uploaded_file)
            st.write(f"Crop Image {i}")
            cropped_img = st_cropper(img, realtime_update=True, box_color="#FF0000", aspect_ratio=None, key=f"cropper_{i}")
            if cropped_img:
                st.session_state.cropped_images.append(cropped_img)
                # Convert to base64 for Gemini
                buffer = BytesIO()
                cropped_img.save(buffer, format="PNG")
                img_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
                st.session_state.image_data.append({"mime_type": "image/png", "data": img_base64})

        # Display cropped images if they exist
        if st.session_state.cropped_images:
            st.subheader("The Contenders")
            cols = st.columns(len(st.session_state.cropped_images))
            for i, (col, cropped_img) in enumerate(zip(cols, st.session_state.cropped_images), 1):
                col.image(cropped_img, caption=f"Image {i}", use_container_width=True)

            # Categories to evaluate
            categories = [
                "Modern Indian Women",
                "Traditional Indian Women",
                "College Indian Women",
                "Intellectual Women",
                "Adventure-Seeking Women"
            ]

            # Button-specific prompts with chain of thought
            prompts = {
                "Rate": (
                    f"You’re a balanced critic. {'This image shows one man' if st.session_state.mode == 'individual' else f'These {len(uploaded_files)} cropped images show men (solo or groups)'}. "
                    f"For each man (label as Man 1, Man 2, etc., across images), analyze their overall appeal—outfit, facial features, expression, vibe, etc. Use this chain of thought: "
                    f"1) Assess the outfit’s style and fit, 2) Evaluate facial features and grooming, 3) Interpret expression and body language, 4) Combine into a general vibe. "
                    f"Rate each out of 10 for these groups: {', '.join(categories)}, reflecting a typical Indian woman’s view in 2025. "
                    f"Add: First Impression (initial vibe), Hidden Flaws (subtle weaknesses), Ideal Match (who they’d attract). "
                    f"Explain with neutral reasoning. {'Rank them (1st, 2nd, etc.) per category with a quick comparison.' if st.session_state.mode == 'group' else ''}"
                ),
                "Unhinged Rating": (
                    f"You’re a wild, unhinged critic. {'This image shows one man' if st.session_state.mode == 'individual' else f'These {len(uploaded_files)} cropped images show men (solo or groups)'}. "
                    f"For each man (label as Man 1, Man 2, etc.), analyze their outfit, face, expression, vibe—everything. Chain of thought: "
                    f"1) Spot standout outfit traits, 2) Judge facial features with flair, 3) Read expression like a drama, 4) Craft an over-the-top vibe. "
                    f"Rate each out of 10 for these groups: {', '.join(categories)}, based on extreme Indian women’s tastes in 2025. "
                    f"Add: First Impression (snap judgment), Hidden Flaws (exaggerated digs), Ideal Match (wild pairing). "
                    f"Go nuts with reasoning—exaggerate everything. {'Rank them (1st, 2nd, etc.) per category with savage comparisons.' if st.session_state.mode == 'group' else ''}"
                ),
                "Feedback": (
                    f"You’re a blunt, helpful critic. {'This image shows one man' if st.session_state.mode == 'individual' else f'These {len(uploaded_files)} cropped images show men (solo or groups)'}. "
                    f"For each man (label as Man 1, Man 2, etc.), analyze their outfit, facial features, expression, vibe, etc. Chain of thought: "
                    f"1) Break down outfit strengths/weaknesses, 2) Assess facial grooming potential, 3) Critique expression impact, 4) Suggest vibe tweaks. "
                    f"Give detailed feedback on improvements—style, grooming, posture—for these groups: {', '.join(categories)}, based on 2025 Indian trends. "
                    f"Add: First Impression (what’s working), Hidden Flaws (fixable issues), Ideal Match (who they could target with changes)."
                ),
                "Roast Me Dead": (
                    f"You’re a merciless roasting machine. {'This image shows one man' if st.session_state.mode == 'individual' else f'These {len(uploaded_files)} cropped images show men (solo or groups)'}. "
                    f"For each man (label as Man 1, Man 2, etc.), tear apart their outfit, face, expression, vibe—everything. Chain of thought: "
                    f"1) Trash the outfit’s every stitch, 2) Rip into facial flaws, 3) Mock the expression, 4) Bury the vibe. "
                    f"Rate each out of 10 for these groups: {', '.join(categories)}, with brutal, lowest-blow roasting. "
                    f"Add: First Impression (instant burn), Hidden Flaws (deep cuts), Ideal Match (who’d even bother). "
                    f"{'Rank them (1st, 2nd, etc.) per category with the harshest comparisons.' if st.session_state.mode == 'group' else ''}"
                )
            }

            # Buttons for different analyses with spacing
            st.subheader("Pick Your Poison")
            st.markdown("""
                <style>
                div[data-testid='column'] {
                    margin-right: 20px;
                }
                div[data-testid='column']:last-child {
                    margin-right: 0;
                }
                </style>
            """, unsafe_allow_html=True)
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
                content = [{"text": selected_prompt}] + st.session_state.image_data
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

    elif uploaded_files is not None and len(uploaded_files) > (1 if st.session_state.mode == "individual" else 3):
        st.error(f"Chill, bro—max {1 if st.session_state.mode == 'individual' else 3} image{'s' if st.session_state.mode == 'group' else ''}.")
