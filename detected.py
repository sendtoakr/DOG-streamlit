import streamlit as st

# ---------------------------------------------------
# ADVANCED CSS
# ---------------------------------------------------

st.markdown("""
<style>

/* Background */

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


/* Hide Streamlit Menu */

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

    background: linear-gradient(
        90deg,
        #00ff87,
        #60efff,
        #00ff87
    );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;

    animation: glow 3s infinite alternate;
}


/* Glow Animation */

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


/* Glass Box */

.glass-box {

    background: rgba(255,255,255,0.06);

    border-radius: 20px;

    padding: 25px;

    backdrop-filter: blur(20px);

    margin-top: 20px;

    border: 1px solid rgba(255,255,255,0.1);
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
}


/* Metrics */

[data-testid="metric-container"] {

    background: rgba(255,255,255,0.07);

    border-radius: 15px;

    padding: 15px;
}


/* Images */

img {

    border-radius: 20px;
}

</style>
""", unsafe_allow_html=True)
