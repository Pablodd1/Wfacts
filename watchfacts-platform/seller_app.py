import streamlit as st
import time
from database import SessionLocal, Listing, Dealer
from datetime import datetime

# --- Theming & Styling ---
st.set_page_config(page_title="WatchFacts Seller App", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    .stApp {
        background-color: #050505;
        color: #e8e8e8;
    }
    h1, h2, h3 {
        color: #d4af37 !important;
        font-family: 'Playfair Display', serif;
        text-align: center;
    }
    .stButton>button {
        background-color: #d4af37;
        color: #050505;
        border: None;
        border-radius: 8px;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        font-weight: bold;
        width: 100%;
        padding: 1rem;
    }
    .stButton>button:hover {
        background-color: #f0d878;
        color: #000;
    }
    div[data-testid="stFileUploader"] {
        border: 1px dashed #d4af37;
        border-radius: 8px;
        padding: 1rem;
        background-color: #0a0a0a;
    }
</style>
""", unsafe_allow_html=True)

st.title("Hermes AI Seller App")

# Navigation via session state
if 'stage' not in st.session_state:
    st.session_state.stage = 'capture'
if 'parsed_data' not in st.session_state:
    st.session_state.parsed_data = {}

def set_stage(stage):
    st.session_state.stage = stage

# --- Stage 1: Photo Capture ---
if st.session_state.stage == 'capture':
    st.header("Step 1: Snap Photos")
    st.markdown("<p style='text-align: center; color: #888;'>Upload Dial, Case, and Caseback photos.</p>", unsafe_allow_html=True)

    uploaded_files = st.file_uploader("Upload watch photos", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'])

    if uploaded_files:
        if st.button("Analyze with Hermes AI"):
            with st.spinner("Analyzing visual features..."):
                time.sleep(1.5) # Simulate processing

                # Mock AI visual recognition based on filename
                filenames = [f.name.lower() for f in uploaded_files]

                parsed = {
                    "brand": "Rolex",
                    "model": "Unknown",
                    "reference": "Unknown",
                    "dial_color": "Unknown",
                    "confidence": 0.85
                }

                if any("hulk" in name for name in filenames):
                    parsed.update({"model": "Submariner", "reference": "116610LV", "dial_color": "Green", "confidence": 0.94})
                elif any("pepsi" in name for name in filenames):
                    parsed.update({"model": "GMT-Master II", "reference": "126710BLRO", "dial_color": "Black", "confidence": 0.96})
                else:
                    parsed.update({"model": "Submariner", "reference": "116610LN", "dial_color": "Black", "confidence": 0.88})

                st.session_state.parsed_data = parsed
                st.success(f"Detected: {parsed['brand']} {parsed['model']} {parsed['reference']}, {parsed['dial_color']} Dial")
                time.sleep(1)
                set_stage('details')
                st.rerun()

# --- Stage 2: Details & Price ---
elif st.session_state.stage == 'details':
    st.header("Step 2: Set Price & Details")

    parsed = st.session_state.parsed_data

    st.markdown(f"**Detected Watch:** {parsed['brand']} {parsed['model']} {parsed['reference']} ({parsed['dial_color']})")

    voice_input = st.text_area("Voice Transcript (Speak price & condition)", placeholder="e.g. Eighteen five full set mint condition")

    col1, col2 = st.columns(2)
    with col1:
        price = st.number_input("Price (USD)", min_value=0, step=100)
    with col2:
        condition = st.slider("Condition Score", 0, 100, 95)

    col3, col4 = st.columns(2)
    with col3:
        box = st.checkbox("Original Box", value=True)
    with col4:
        papers = st.checkbox("Original Papers", value=True)

    if st.button("Review Listing"):
        # Very basic NLP simulation
        if "eighteen" in voice_input.lower() and "five" in voice_input.lower():
            price = 18500
        if "full set" in voice_input.lower():
            box = True
            papers = True

        st.session_state.parsed_data.update({
            "price_usd": price,
            "condition_score": condition,
            "box": box,
            "papers": papers,
            "voice_input": voice_input
        })
        set_stage('review')
        st.rerun()

# --- Stage 3: Review & Submit ---
elif st.session_state.stage == 'review':
    st.header("Step 3: Review & Submit")

    data = st.session_state.parsed_data

    st.json(data)

    st.info("Market Comp: Similar listings are asking $17,800 - $19,200.")

    certify = st.checkbox("Request WatchFacts Certification (+$150)", value=True)

    if st.button("Submit Listing"):
        with st.spinner("Submitting to WatchFacts..."):
            session = SessionLocal()
            try:
                # Get a dummy dealer
                dealer = session.query(Dealer).first()
                if dealer:
                    listing = Listing(
                        dealer_id=dealer.id,
                        brand=data['brand'],
                        model=data['model'],
                        reference=data['reference'],
                        dial_color=data['dial_color'],
                        price_usd=data['price_usd'],
                        condition_score=data['condition_score'],
                        box=data['box'],
                        papers=data['papers'],
                        status="pending_certification" if certify else "live",
                        source_type="seller_app",
                        raw_text=data.get('voice_input', ''),
                        exception_flags=0,
                        ai_confidence=data['confidence'],
                        certification_status="requested" if certify else "none",
                        created_at=datetime.utcnow()
                    )
                    session.add(listing)
                    session.commit()
                    st.success("Listing Submitted Successfully!")
                    time.sleep(2)
                    set_stage('capture')
                    st.rerun()
            finally:
                session.close()
