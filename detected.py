import streamlit as st
from ultralytics import YOLO
import cv2
import numpy as np
import tempfile
import os
from fpdf import FPDF
from datetime import datetime

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="D.O.G Vision System",
    page_icon="🌿",
    layout="wide"
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "DOG.pt")

# ---------------- UI STYLE ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(
        rgba(0,0,0,0.7),
        rgba(0,0,0,0.9)
    ),
    url("https://images.unsplash.com/photo-1501004318641-b39e6451bec6");
    background-size: cover;
    background-position: center;
}

.main-title {
    text-align:center;
    font-size:4rem;
    font-weight:bold;
    background: linear-gradient(90deg,#00e676,#00c853,#69f0ae);
    -webkit-background-clip:text;
    color:transparent;
}

.glass {
    background: rgba(255,255,255,0.05);
    border-radius:20px;
    backdrop-filter: blur(20px);
    padding:25px;
    margin-top:20px;
}

.stButton>button {
    border-radius: 12px;
    background: #00c853;
    color: white;
    border: none;
}

.metric-card {
    background: rgba(255,255,255,0.05);
    padding: 10px;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- PDF CLASS ----------------
class PDF(FPDF):

    def header(self):
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, "D.O.G Vision System Report", 0, 1, "C")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")

# ---------------- SUGGESTIONS ----------------
def get_suggestion_and_cure(label):

    data = {
        "disease": (
            "Apply fungicide spray",
            "Use Carbendazim or Mancozeb weekly"
        ),

        "pest": (
            "Spray pesticide",
            "Use Imidacloprid or Neem oil treatment"
        ),

        "dry": (
            "Increase watering frequency",
            "Install drip irrigation system"
        ),

        "healthy": (
            "No action needed",
            "Maintain current care routine"
        )
    }

    return data.get(
        label.lower(),
        (
            "Monitor plant regularly",
            "General organic care recommended"
        )
    )

# ---------------- PDF GENERATION ----------------
def generate_pdf(original, detected, detections, filename):

    pdf = PDF()
    pdf.add_page()

    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as f1, \
         tempfile.NamedTemporaryFile(delete=False, suffix=".png") as f2:

        cv2.imwrite(f1.name, original)
        cv2.imwrite(f2.name, detected)

        pdf.image(f1.name, x=10, y=30, w=85)
        pdf.image(f2.name, x=110, y=30, w=85)

    pdf.set_y(120)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, f"File: {filename}", 0, 1)

    pdf.cell(0, 10, "Detection Analysis:", 0, 1)

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
        "Ensure regular monitoring of crops. Apply suggested treatments promptly to avoid disease spread."
    )

    pdf.ln(5)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Developed By:", 0, 1)

    pdf.set_font("Arial", "", 11)

    pdf.cell(0, 8, "Utkarsh Tripathi", 0, 1)
    pdf.cell(0, 8, "Aditya Kumar Raj", 0, 1)
    pdf.cell(0, 8, "Abhiyanshu Kumar", 0, 1)

    pdf.cell(
        0,
        8,
        f"Date: {datetime.now().strftime('%d-%m-%Y %H:%M')}",
        0,
        1
    )

    return pdf.output(dest="S").encode("latin-1")

# ---------------- LOAD MODEL ----------------
@st.cache_resource
def load_model():

    if not os.path.exists(MODEL_PATH):
        return None

    try:
        model = YOLO(MODEL_PATH)
        return model

    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

# ---------------- DETECTION ----------------
def detect(frame, model, conf_threshold):

    results = model(frame)

    output = frame.copy()

    detections = []

    for r in results:

        for box in r.boxes:

            confidence = float(box.conf[0])

            if confidence >= conf_threshold:

                cls = int(box.cls[0])

                label = model.names[cls]

                detections.append((label, confidence))

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
                    f"{label} {confidence:.2f}",
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 0),
                    2
                )

    return output, detections

# ---------------- MAIN ----------------
def main():

    st.markdown(
        '<div class="main-title">D.O.G Vision System</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <p style="text-align:center;color:white;">
        Utkarsh Tripathi | Aditya Kumar Raj | Abhiyanshu Kumar
        </p>
        """,
        unsafe_allow_html=True
    )

    model = load_model()

    if model is None:
        st.error("❌ DOG.pt model file not found.")
        return

    # Sidebar
    st.sidebar.title("⚙ Settings")

    confidence = st.sidebar.slider(
        "Confidence Threshold",
        0.0,
        1.0,
        0.5
    )

    mode = st.sidebar.selectbox(
        "Select Mode",
        ["Upload Image", "Camera Capture"]
    )

    st.markdown('<div class="glass">', unsafe_allow_html=True)

    # ---------------- IMAGE MODE ----------------
    if mode == "Upload Image":

        st.subheader("📤 Upload Image")

        uploaded_file = st.file_uploader(
            "Choose an image",
            type=["jpg", "jpeg", "png"]
        )

        if uploaded_file is not None:

            file_bytes = np.asarray(
                bytearray(uploaded_file.read()),
                dtype=np.uint8
            )

            image = cv2.imdecode(file_bytes, 1)

            detected_image, detections = detect(
                image,
                model,
                confidence
            )

            col1, col2 = st.columns(2)

            with col1:
                st.image(image, caption="Original Image")

            with col2:
                st.image(detected_image, caption="Detected Output")

            st.subheader("📊 Analysis")

            c1, c2, c3 = st.columns(3)

            c1.metric("Objects Found", len(detections))

            avg_conf = (
                np.mean([c for _, c in detections])
                if detections else 0
            )

            c2.metric("Average Confidence", f"{avg_conf:.2f}")

            status = "Healthy" if len(detections) == 0 else "Issue Found"

            c3.metric("Status", status)

            # Suggestions
            if detections:

                st.subheader("🌱 Suggestions & Cure")

                for label, conf in detections:

                    suggestion, cure = get_suggestion_and_cure(label)

                    st.write(f"### {label}")
                    st.write(f"Confidence: {conf:.2f}")
                    st.write(f"Suggestion: {suggestion}")
                    st.write(f"Cure: {cure}")
                    st.write("---")

            # PDF Download
            pdf = generate_pdf(
                image,
                detected_image,
                detections,
                uploaded_file.name
            )

            st.download_button(
                "📄 Download Report",
                pdf,
                file_name="DOG_Report.pdf",
                mime="application/pdf"
            )

    # ---------------- CAMERA MODE ----------------
    elif mode == "Camera Capture":

        st.subheader("📷 Capture Image From Camera")

        camera_image = st.camera_input("Take a Picture")

        if camera_image is not None:

            bytes_data = camera_image.getvalue()

            np_array = np.frombuffer(bytes_data, np.uint8)

            image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

            detected_image, detections = detect(
                image,
                model,
                confidence
            )

            col1, col2 = st.columns(2)

            with col1:
                st.image(image, caption="Captured Image")

            with col2:
                st.image(detected_image, caption="Detected Output")

            st.success("Detection Completed Successfully")

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        """
        <hr>
        <p style='text-align:center;color:gray;'>
        Developed by Utkarsh Tripathi • Aditya Kumar Raj • Abhiyanshu Kumar
        </p>
        """,
        unsafe_allow_html=True
    )

# ---------------- RUN APP ----------------
if __name__ == "__main__":
    main()
