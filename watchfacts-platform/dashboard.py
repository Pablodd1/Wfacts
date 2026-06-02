import streamlit as st
import pandas as pd
import plotly.express as px
from database import SessionLocal, Listing, ExceptionRecord
from resolver import resolve_exception, decode_flags

# --- Theming & Styling ---
st.set_page_config(page_title="WatchFacts Hermes Admin", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
    /* Dark Luxury Theme */
    .stApp {
        background-color: #050505;
        color: #e8e8e8;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #d4af37 !important; /* Gold */
        font-family: 'Playfair Display', serif;
    }
    .stButton>button {
        background-color: #d4af37;
        color: #050505;
        border: None;
        border-radius: 4px;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #f0d878;
        color: #000;
        border: None;
    }
    .stDataFrame {
        background-color: #0a0a0a;
        border: 1px solid rgba(212,175,55,0.15);
    }
    /* Metric Cards */
    div[data-testid="metric-container"] {
        background-color: #0a0a0a;
        border: 1px solid rgba(212,175,55,0.15);
        padding: 1rem;
        border-radius: 8px;
    }
    div[data-testid="metric-container"] > div > div > div > div > p {
        color: #d4af37; /* Title */
    }
    div[data-testid="metric-container"] > div > div > div > div > div {
        color: #e8e8e8; /* Value */
    }
</style>
""", unsafe_allow_html=True)

def get_data():
    session = SessionLocal()
    try:
        listings_df = pd.read_sql(session.query(Listing).statement, session.bind)
        exceptions_df = pd.read_sql(session.query(ExceptionRecord).statement, session.bind)
        return listings_df, exceptions_df
    finally:
        session.close()

listings_df, exceptions_df = get_data()

st.sidebar.title("Hermes AI")
page = st.sidebar.radio("Navigation", ["Metrics", "Exception Queue", "Seller App Simulator"])

if page == "Metrics":
    st.title("Platform Metrics")

    col1, col2, col3, col4 = st.columns(4)
    total_listings = len(listings_df)
    total_exceptions = len(exceptions_df)
    exception_rate = (total_exceptions / total_listings * 100) if total_listings > 0 else 0
    auto_resolved = len(exceptions_df[exceptions_df['status'] == 'ai_resolved'])
    auto_clear_rate = (auto_resolved / total_exceptions * 100) if total_exceptions > 0 else 0
    pending_exceptions = len(exceptions_df[exceptions_df['status'] == 'pending'])

    col1.metric("Total Listings", f"{total_listings:,}")
    col2.metric("Exception Rate", f"{exception_rate:.1f}%")
    col3.metric("Auto-Clear Rate", f"{auto_clear_rate:.1f}%")
    col4.metric("Backlog Queue", f"{pending_exceptions:,}")

    st.subheader("Listings by Status")
    status_counts = listings_df['status'].value_counts().reset_index()
    status_counts.columns = ['Status', 'Count']
    fig = px.pie(status_counts, values='Count', names='Status', hole=0.4,
                 color_discrete_sequence=['#d4af37', '#22c55e', '#ef4444', '#eab308', '#888888'])
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='#e8e8e8')
    st.plotly_chart(fig, use_container_width=True)

elif page == "Exception Queue":
    st.title("Exception Queue")

    pending_df = exceptions_df[exceptions_df['status'] == 'pending']

    if pending_df.empty:
        st.success("No pending exceptions!")
    else:
        st.write(f"Showing {len(pending_df)} pending exceptions.")

        # Display data
        display_cols = ['id', 'listing_id', 'exception_flags', 'status', 'created_at']
        st.dataframe(pending_df[display_cols])

        st.subheader("Resolve Exception")
        selected_id = st.selectbox("Select Exception ID to resolve", pending_df['id'].tolist())

        if selected_id:
            ex_row = pending_df[pending_df['id'] == selected_id].iloc[0]
            listing_row = listings_df[listings_df['id'] == ex_row['listing_id']].iloc[0]

            st.markdown("**Raw Listing Text:**")
            st.code(listing_row['raw_text'])

            flags = decode_flags(ex_row['exception_flags'])
            st.markdown(f"**Flags:** `{', '.join(flags)}`")

            if st.button("Run AI Resolver"):
                with st.spinner("Simon AI is analyzing..."):
                    proposal = resolve_exception(selected_id)

                if proposal.get('confidence', 0) > 0:
                    st.success(f"Resolution found! (Confidence: {proposal['confidence']:.2f})")
                    st.json(proposal)
                    st.markdown("**Reasoning:**")
                    st.info(proposal['reasoning'])

                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("Approve AI Proposal", type="primary"):
                             # In a real app, we'd update DB here
                             st.success("Proposal approved and listing updated.")
                    with col2:
                        if st.button("Reject Proposal"):
                             st.error("Proposal rejected. Escalated for manual review.")
                else:
                    st.warning("AI could not resolve this exception automatically.")

elif page == "Seller App Simulator":
    st.title("Seller App Simulator (Text Input)")

    raw_input = st.text_area("Paste WhatsApp Listing Text", placeholder="e.g. Rolex Submariner Hulk 2019 full set $18.5k")

    if st.button("AI Parse Listing"):
        if raw_input:
            with st.spinner("Hermes AI processing..."):
                # Simulate AI parsing (mock logic based on our resolver)
                parsed = {
                    "brand": "Rolex" if "rolex" in raw_input.lower() else "Unknown",
                    "model": "Unknown",
                    "reference": "Unknown",
                    "dial_color": "Unknown",
                    "price_usd": None,
                    "confidence": 0.85
                }

                if "hulk" in raw_input.lower():
                    parsed["model"] = "Submariner"
                    parsed["reference"] = "116610LV"
                    parsed["dial_color"] = "Green"
                elif "pepsi" in raw_input.lower():
                    parsed["model"] = "GMT-Master II"
                    parsed["reference"] = "126710BLRO"
                    parsed["dial_color"] = "Black"

                if "k" in raw_input.lower():
                     import re
                     match = re.search(r'\$(\d+(?:\.\d+)?)k', raw_input.lower())
                     if match:
                         parsed["price_usd"] = float(match.group(1)) * 1000

            st.json(parsed)
            if parsed["reference"] == "Unknown":
                st.warning("Could not identify reference. This would trigger an exception.")
            else:
                st.success("Successfully parsed listing!")
        else:
            st.error("Please enter listing text.")
