import os
import cv2
import tempfile
import numpy as np
import streamlit as st

from ultralytics import YOLO
from fpdf import FPDF
from datetime import datetime

# Optional webcam support
try:
    from streamlit_webrtc import webrtc_streamer
    WEBRTC_AVAILABLE = True
except Exception:
    WEBRTC_AVAILABLE = False


# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="D.O.G Vision System",
    page_icon="🌿",
    layout="wide"
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "DOG.pt")


# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------

st.markdown("""
<style>

.stApp {
    background: linear-gradient(
        rgba(0,0,0,0.75),
        rgba(0,0,0,0.92)
    ),
    url("https://images.unsplash.com/photo-1501004318641-b39e6451bec6");

    background-size: cover;
    background-position: center;
}

.main-title {
    text-align: center;
    font-size: 4rem;
    font-weight: bold;
    background: linear-gradient(90deg,#00e676,#00c853,#69f0ae);
    -webkit-background-clip: text;
    color: transparent;
}

.glass-box {
    background: rgba(255,255,255,0.06);
    border-radius: 20px;
    padding: 25px;
    backdrop-filter: blur(15px);
    margin-top: 20px;
}

</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------
# PDF REPORT
# ---------------------------------------------------

class PDF(FPDF):

    def header(self):
        self.set_font("Arial", "B", 15)
        self.cell(0, 10, "D.O.G Vision System Report", 0, 1, "C")

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")


# ---------------------------------------------------
# SUGGESTION SYSTEM
# ---------------------------------------------------

def get_suggestion_and_cure(label):

    data = {
        "disease": (
            "Apply fungicide spray",
            "Use Carbendazim or Mancozeb weekly"
        ),

        "pest": (
            "Spray pesticide",
            "Use Neem oil or Imidacloprid treatment"
        ),

        "dry": (
            "Increase watering frequency",
            "Install proper drip irrigation system"
        ),

        "healthy": (
            "No action required",
            "Maintain current plant care routine"
        )
    }

    return data.get(
        label.lower(),
        (
            "Monitor plant regularly",
            "Use general organic plant care"
        )
    )


# ---------------------------------------------------
# PDF GENERATOR
# ---------------------------------------------------

def generate_pdf(original, detected, detections, filename):

    pdf = PDF()
    pdf.add_page()

    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as f1, \
         tempfile.NamedTemporaryFile(delete=False, suffix=".png") as f2:

        cv2.imwrite(f1.name, original)
        cv2.imwrite(f2.name, detected)

        pdf.image(f1.name, x=10, y=30, w=90)
        pdf.image(f2.name, x=110, y=30, w=90)

    pdf.set_y(120)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, f"File: {filename}", 0, 1)

    pdf.cell(0, 10, "Detection Results:", 0, 1)

    pdf.set_font("Arial", "", 11)

    for label, conf in detections:

        suggestion, cure = get_suggestion_and_cure(label)

        pdf.cell(0, 8, f"{label} ({conf:.2f})", 0, 1)
        pdf.cell(0, 8, f"Suggestion: {suggestion}", 0, 1)
        pdf.cell(0, 8, f"Cure: {cure}", 0, 1)

        pdf.ln(2)

    pdf.ln(5)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Final Recommendation:", 0, 1)

    pdf.set_font("Arial", "", 11)

    pdf.multi_cell(
        0,
        8,
        "Monitor crops regularly and apply treatment early. "
        "Maintain proper irrigation, sunlight, and nutrition."
    )

    pdf.ln(5)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Developed By:", 0, 1)

    pdf.set_font("Arial", "", 11)

    
    pdf.cell(0, 8, "Aditya Kumar Raj", 0, 1)
    

    pdf.cell(0, 8, f"Generated: {datetime.now()}", 0, 1)

    return pdf.output(dest="S").encode("latin-1")


# ---------------------------------------------------
# LOAD MODEL
# ---------------------------------------------------

@st.cache_resource
def load_model():

    if not os.path.exists(MODEL_PATH):
        return None

    return YOLO(MODEL_PATH)


# ---------------------------------------------------
# DETECTION FUNCTION
# ---------------------------------------------------

def detect_objects(frame, model, confidence):

    results = model(frame)

    output = frame.copy()
    detections = []

    for r in results:

        for box in r.boxes:

            conf = float(box.conf[0])

            if conf >= confidence:

                cls = int(box.cls[0])
                label = model.names[cls]

                detections.append((label, conf))

                x1, y1, x2, y2 = map(int, box.xyxy[0])

                cv2.rectangle(
                    output,
                    (x1, y1),
                    (x2, y2),
                    (0, 255, 0),
                    2
                )

                cv2.putText(
                    output,
                    f"{label} {conf:.2f}",
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 0),
                    2
                )

    return output, detections


# ---------------------------------------------------
# MAIN APP
# ---------------------------------------------------

def main():

    st.markdown(
        '<div class="main-title">D.O.G Vision System</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        "<p style='text-align:center;color:white;'>"
         Aditya Kumar Raj 
        "</p>",
        unsafe_allow_html=True
    )

    model = load_model()

    if model is None:
        st.error("DOG.pt model file not found.")
        return

    st.sidebar.title("⚙ Settings")

    confidence = st.sidebar.slider(
        "Confidence Threshold",
        0.0,
        1.0,
        0.5
    )

    mode = st.sidebar.selectbox(
        "Select Mode",
        ["Image Detection", "Live Detection"]
    )

    st.markdown('<div class="glass-box">', unsafe_allow_html=True)

    # ---------------------------------------------------
    # IMAGE MODE
    # ---------------------------------------------------

    if mode == "Image Detection":

        st.subheader("📤 Upload Image")

        uploaded_file = st.file_uploader(
            "Choose an image",
            type=["jpg", "jpeg", "png"]
        )

        if uploaded_file:

            file_bytes = np.asarray(
                bytearray(uploaded_file.read()),
                dtype=np.uint8
            )

            image = cv2.imdecode(file_bytes, 1)

            detected_image, detections = detect_objects(
                image,
                model,
                confidence
            )

            col1, col2 = st.columns(2)

            col1.image(image, caption="Original Image")
            col2.image(detected_image, caption="Detected Image")

            st.divider()

            metric1, metric2, metric3 = st.columns(3)

            metric1.metric("Objects Found", len(detections))

            avg_conf = (
                np.mean([c for _, c in detections])
                if detections else 0
            )

            metric2.metric(
                "Average Confidence",
                f"{avg_conf:.2f}"
            )

            metric3.metric(
                "Status",
                "Healthy" if len(detections) == 0 else "Issue Found"
            )

            if detections:

                st.subheader("🌱 Suggestions & Treatment")

                for label, conf in detections:

                    suggestion, cure = get_suggestion_and_cure(label)

                    st.write(f"### {label}")
                    st.write(f"Confidence: {conf:.2f}")
                    st.write(f"Suggestion: {suggestion}")
                    st.write(f"Treatment: {cure}")

                    st.divider()

                pdf_data = generate_pdf(
                    image,
                    detected_image,
                    detections,
                    uploaded_file.name
                )

                st.download_button(
                    "📄 Download Report",
                    pdf_data,
                    file_name="DOG_Report.pdf",
                    mime="application/pdf"
                )

    # ---------------------------------------------------
    # LIVE MODE
    # ---------------------------------------------------

    elif mode == "Live Detection":

        if WEBRTC_AVAILABLE:

            st.success("Webcam initialized successfully.")

            webrtc_streamer(
                key="live-detection"
            )

        else:

            st.error(
                "streamlit-webrtc is not installed "
                "or not supported on this Python version."
            )

    st.markdown("</div>", unsafe_allow_html=True)


# ---------------------------------------------------
# RUN APP
# ---------------------------------------------------

if __name__ == "__main__":
    main()
