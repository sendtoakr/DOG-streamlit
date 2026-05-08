import streamlit as st
import cv2
import numpy as np
import os
from ultralytics import YOLO

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Plant Disease Detection",
    page_icon="🌿",
    layout="wide"
)

# ---------------------------------------------------
# MODEL PATH
# ---------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "DOG.pt")

# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------

st.markdown("""
<style>

/* Background */

.stApp {

    background:
    linear-gradient(
        rgba(0,0,0,0.65),
        rgba(0,40,0,0.75)
    ),
    url("https://images.unsplash.com/photo-1466692476868-aef1dfb1e735");

    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}


/* Main Container */

.main .block-container {

    padding-top: 2rem;
    padding-bottom: 2rem;
    padding-left: 3rem;
    padding-right: 3rem;
}


/* Hide Streamlit Branding */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}


/* Title */

.main-title {

    text-align: center;

    font-size: 4rem;

    font-weight: bold;

    color: #00ff99;

    text-shadow:
        0 0 10px #00ff99,
        0 0 20px #00ff99;

    margin-bottom: 10px;
}


/* Subtitle */

.subtitle {

    text-align: center;

    color: white;

    font-size: 1.2rem;

    margin-bottom: 30px;
}


/* Glass Box */

.glass-box {

    background: rgba(255,255,255,0.08);

    border-radius: 20px;

    padding: 25px;

    backdrop-filter: blur(10px);

    border: 1px solid rgba(255,255,255,0.15);

    box-shadow:
        0 4px 20px rgba(0,255,100,0.2);
}


/* Sidebar */

section[data-testid="stSidebar"] {

    background:
    linear-gradient(
        rgba(0,40,0,0.95),
        rgba(0,0,0,0.95)
    );
}


/* Sidebar Text */

section[data-testid="stSidebar"] * {

    color: white !important;
}


/* Upload Box */

[data-testid="stFileUploader"] {

    background: rgba(255,255,255,0.05);

    border: 2px dashed #00ff99;

    border-radius: 15px;

    padding: 20px;
}


/* Buttons */

.stButton > button {

    width: 100%;

    border-radius: 12px;

    border: none;

    padding: 12px;

    background: linear-gradient(
        90deg,
        #00c853,
        #00ff99
    );

    color: white;

    font-weight: bold;
}


/* Metric Cards */

[data-testid="metric-container"] {

    background: rgba(255,255,255,0.07);

    border-radius: 15px;

    padding: 15px;

    border: 1px solid rgba(255,255,255,0.1);
}


/* Text */

h1, h2, h3, h4, h5 {

    color: white !important;
}

p, label, div, span {

    color: white;
}


/* Images */

img {

    border-radius: 15px;
}


/* Footer */

.footer {

    text-align: center;

    color: #cccccc;

    margin-top: 30px;

    font-size: 14px;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# TITLE
# ---------------------------------------------------

st.markdown(
    """
    <div class="main-title">
        🌿 Plant Disease Detection System
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="subtitle">
        AI Powered Smart Crop Monitoring
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------
# LOAD MODEL
# ---------------------------------------------------

@st.cache_resource
def load_model():

    if not os.path.exists(MODEL_PATH):
        return None

    return YOLO(MODEL_PATH)

model = load_model()

# ---------------------------------------------------
# ERROR IF MODEL NOT FOUND
# ---------------------------------------------------

if model is None:

    st.error("DOG.pt model file not found.")
    st.stop()

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

st.sidebar.title("⚙ Detection Settings")

confidence = st.sidebar.slider(
    "Confidence Threshold",
    0.0,
    1.0,
    0.5
)

# ---------------------------------------------------
# MAIN CONTENT
# ---------------------------------------------------

st.markdown('<div class="glass-box">', unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "📤 Upload Plant Image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file:

    # Read Image
    file_bytes = np.asarray(
        bytearray(uploaded_file.read()),
        dtype=np.uint8
    )

    image = cv2.imdecode(file_bytes, 1)

    # Detect Objects
    results = model(image)

    output = image.copy()

    detections = []

    for result in results:

        for box in result.boxes:

            conf = float(box.conf[0])

            if conf >= confidence:

                cls = int(box.cls[0])

                label = model.names[cls]

                detections.append((label, conf))

                x1, y1, x2, y2 = map(int, box.xyxy[0])

                # Draw Box
                cv2.rectangle(
                    output,
                    (x1, y1),
                    (x2, y2),
                    (0,255,0),
                    2
                )

                # Label
                cv2.putText(
                    output,
                    f"{label} {conf:.2f}",
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0,255,0),
                    2
                )

    # Show Images
    col1, col2 = st.columns(2)

    with col1:
        st.image(image, caption="Original Image")

    with col2:
        st.image(output, caption="Detected Disease")

    st.divider()

    # Metrics
    m1, m2, m3 = st.columns(3)

    m1.metric("Detections", len(detections))

    avg_conf = (
        np.mean([c for _, c in detections])
        if detections else 0
    )

    m2.metric(
        "Average Confidence",
        f"{avg_conf:.2f}"
    )

    status = (
        "Healthy"
        if len(detections) == 0
        else "Disease Found"
    )

    m3.metric("Plant Status", status)

    # Results
    if detections:

        st.subheader("🌱 Detection Results")

        for label, conf in detections:

            st.success(
                f"{label} detected with confidence {conf:.2f}"
            )

    else:

        st.success("✅ No Disease Detected")

st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.markdown(
    """
    <div class="footer">
        Developed by Aditya Kumar Raj 🌱
    </div>
    """,
    unsafe_allow_html=True
)
