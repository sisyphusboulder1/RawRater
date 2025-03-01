import streamlit as st
import cv2
from PIL import Image
import numpy as np
import requests

st.title("RawRater - Unfiltered Style Check")

uploaded_file = st.file_uploader("Drop your pic, let’s tear it apart", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Here’s your mess")

    img_array = np.array(image)
    img_cv = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)

    brightness = int(np.mean(img_cv))
    st.write(f"Brightness score: {brightness} (higher = flashier)")

    # Unsplash API (no key for basic random image)
    url = "https://source.unsplash.com/random/300x200/?fashion"
    st.image(url, caption="Trendy look for comparison")

    if brightness > 100:
        st.write("Rating: 7/10. Flashy and loud.")
        st.write("- **Modern Indian Women**: Vibe with it (8/10).")
        st.write("- **Traditional Indian Women**: Too brash (3/10).")
        st.write("- **College Indian Women**: Cute but bold (7/10).")
        st.write("- **Intellectual Women**: Too much (5/10).")
        st.write("- **Adventure-Seeking Women**: Dig it (8/10).")
    else:
        st.write("Rating: 5/10. Subtle and tame.")
        st.write("- **Modern Indian Women**: Not enough edge (4/10).")
        st.write("- **Traditional Indian Women**: Like the calm (7/10).")
        st.write("- **College Indian Women**: Cute, safe (6/10).")
        st.write("- **Intellectual Women**: Respect the chill (6/10).")
        st.write("- **Adventure-Seeking Women**: No spark (3/10).")
