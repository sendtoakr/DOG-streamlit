# ---------------------------------------------------
# ADVANCED PLANT DISEASE DETECTION CSS
# ---------------------------------------------------

st.markdown("""
<style>

/* Main Background */

.stApp {
    background:
    linear-gradient(
        rgba(0, 20, 0, 0.82),
        rgba(0, 0, 0, 0.90)
    ),
    url("https://images.unsplash.com/photo-1466692476868-aef1dfb1e735");

    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}


/* Hide Streamlit Branding */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}


/* Main Title */

.main-title {

    text-align: center;
    font-size: 4.5rem;
    font-weight: 900;
    letter-spacing: 3px;

    background: linear-gradient(
        90deg,
        #00ff87,
        #60efff,
        #00ff87
    );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;

    text-shadow:
        0px 0px 15px rgba(0,255,135,0.4);

    animation: glow 3s infinite alternate;
}


/* Title Glow Animation */

@keyframes glow {

    from {
        text-shadow:
        0 0 10px #00ff87,
        0 0 20px #00ff87;
    }

    to {
        text-shadow:
        0 0 20px #60efff,
        0 0 40px #60efff;
    }
}


/* Subtitle */

.subtitle {

    text-align: center;
    color: #d4ffd4;
    font-size: 1.2rem;
    margin-top: -10px;
    margin-bottom: 30px;
    letter-spacing: 1px;
}


/* Glassmorphism Main Container */

.glass-box {

    background: rgba(255,255,255,0.06);

    border: 1px solid rgba(255,255,255,0.15);

    border-radius: 25px;

    padding: 30px;

    backdrop-filter: blur(20px);

    box-shadow:
        0 8px 32px rgba(0,255,100,0.18);

    margin-top: 20px;
}


/* Sidebar */

section[data-testid="stSidebar"] {

    background:
    linear-gradient(
        180deg,
        rgba(0,50,0,0.95),
        rgba(0,20,0,0.95)
    );

    border-right: 1px solid rgba(255,255,255,0.1);
}


/* Sidebar Text */

section[data-testid="stSidebar"] * {
    color: #d8ffd8 !important;
}


/* Upload Box */

[data-testid="stFileUploader"] {

    background: rgba(255,255,255,0.05);

    border: 2px dashed #00ff87;

    border-radius: 20px;

    padding: 20px;

    transition: 0.3s;
}

[data-testid="stFileUploader"]:hover {

    border-color: #60efff;

    box-shadow:
        0 0 20px rgba(0,255,135,0.5);
}


/* Buttons */

.stButton > button,
.stDownloadButton > button {

    width: 100%;

    border-radius: 15px;

    border: none;

    padding: 12px;

    font-size: 16px;

    font-weight: bold;

    background: linear-gradient(
        90deg,
        #00c853,
        #00e676
    );

    color: white;

    transition: 0.3s ease-in-out;

    box-shadow:
        0 4px 15px rgba(0,255,100,0.3);
}


/* Button Hover */

.stButton > button:hover,
.stDownloadButton > button:hover {

    transform: scale(1.03);

    background: linear-gradient(
        90deg,
        #00e676,
        #69f0ae
    );

    box-shadow:
        0 6px 20px rgba(0,255,120,0.5);
}


/* Metrics Cards */

[data-testid="metric-container"] {

    background: rgba(255,255,255,0.07);

    border: 1px solid rgba(255,255,255,0.12);

    padding: 20px;

    border-radius: 20px;

    box-shadow:
        0 4px 15px rgba(0,255,100,0.15);

    transition: 0.3s;
}


/* Metrics Hover */

[data-testid="metric-container"]:hover {

    transform: translateY(-5px);

    box-shadow:
        0 8px 20px rgba(0,255,120,0.3);
}


/* Image Styling */

img {

    border-radius: 20px;

    border: 3px solid rgba(255,255,255,0.1);

    box-shadow:
        0 5px 20px rgba(0,255,100,0.2);
}


/* Headings */

h1, h2, h3 {

    color: #d8ffd8 !important;
}


/* Text */

p, label, span, div {

    color: #f0fff0;
}


/* Divider */

hr {

    border: none;

    height: 1px;

    background: linear-gradient(
        to right,
        transparent,
        #00ff87,
        transparent
    );

    margin-top: 30px;
    margin-bottom: 30px;
}


/* Scrollbar */

::-webkit-scrollbar {
    width: 10px;
}

::-webkit-scrollbar-track {
    background: rgba(0,0,0,0.3);
}

::-webkit-scrollbar-thumb {

    background: linear-gradient(
        #00c853,
        #69f0ae
    );

    border-radius: 10px;
}


/* Detection Result Cards */

.result-card {

    background: rgba(255,255,255,0.05);

    border-left: 5px solid #00ff87;

    padding: 20px;

    border-radius: 15px;

    margin-bottom: 15px;

    box-shadow:
        0 5px 15px rgba(0,255,100,0.15);
}


/* Footer */

.footer {

    text-align: center;

    color: #b2ffb2;

    padding-top: 20px;

    font-size: 15px;

    letter-spacing: 1px;
}

</style>
""", unsafe_allow_html=True)
