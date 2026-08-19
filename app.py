"""LinkSentinel — Real-Time Malicious URL Detection Web Interface.

Stealth Obsidian Monochrome Enterprise UI with Zero Jarring Blue Elements.
SAFETY GUARANTEE: Never accesses the destination website or issues network requests.
"""

import time
import pandas as pd
import joblib
import streamlit as st

from src.features.extract_features import URLLexicalFeatureExtractor

# Page Configuration
st.set_page_config(
    page_title="LinkSentinel — Enterprise URL Risk Engine",
    page_icon="🛡️",
    layout="centered"
)

# Stealth Dark Monochrome CSS Suite (No Blue Accent Colors)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }

    /* Main Container Background */
    .stApp {
        background-color: #0B0F17;
        color: #E2E8F0;
    }

    /* Header Container */
    .enterprise-header {
        background-color: #111827;
        border: 1px solid #1E293B;
        border-radius: 8px;
        padding: 20px 24px;
        margin-bottom: 24px;
    }

    .header-top {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 8px;
    }

    .header-title-group {
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .header-title {
        font-size: 1.75rem;
        font-weight: 700;
        color: #F8FAFC;
        margin: 0;
        letter-spacing: -0.02em;
    }

    /* Version Tag (Monochrome Stealth) */
    .version-tag {
        background: #1E293B;
        border: 1px solid #334155;
        color: #E2E8F0;
        font-size: 0.75rem;
        font-weight: 600;
        padding: 4px 10px;
        border-radius: 4px;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }

    .header-desc {
        color: #94A3B8;
        font-size: 0.9rem;
        margin: 0;
        line-height: 1.5;
    }

    /* Input Label */
    .input-label {
        font-size: 0.85rem;
        font-weight: 600;
        color: #CBD5E1;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 8px;
    }

    /* Streamlit Input Overrides (Stealth Dark Focus) */
    div.stTextInput > div > div > input {
        background-color: #0F172A !important;
        color: #F8FAFC !important;
        border: 1px solid #334155 !important;
        border-radius: 6px !important;
        font-size: 0.95rem !important;
    }

    div.stTextInput > div > div > input:focus {
        border-color: #64748B !important;
        box-shadow: 0 0 0 1px #64748B !important;
    }

    /* Primary Stealth Button (Dark Slate/Black Accent) */
    div.stButton > button {
        width: 100%;
        background-color: #1E293B;
        color: #F8FAFC;
        border: 1px solid #475569;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.95rem;
        padding: 10px 16px;
        transition: all 0.15s ease;
        box-shadow: 0 2px 4px rgba(0,0,0,0.4);
    }

    div.stButton > button:hover {
        background-color: #334155;
        border-color: #64748B;
        color: #FFFFFF;
    }

    /* Result Panel */
    .result-panel {
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 20px;
    }

    .panel-suspicious {
        background-color: #1A0F14;
        border: 1px solid #9F1239;
    }

    .panel-safe {
        background-color: #061A14;
        border: 1px solid #065F46;
    }

    .panel-top {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 12px;
    }

    .status-group {
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .status-title-suspicious {
        color: #FCA5A5;
        font-size: 1.25rem;
        font-weight: 700;
        letter-spacing: -0.01em;
    }

    .status-title-safe {
        color: #6EE7B7;
        font-size: 1.25rem;
        font-weight: 700;
        letter-spacing: -0.01em;
    }

    .prob-val {
        font-size: 1.5rem;
        font-weight: 700;
        color: #F8FAFC;
    }

    .prob-sub {
        font-size: 0.75rem;
        color: #94A3B8;
        text-align: right;
    }

    /* Risk Bar */
    .risk-bar-track {
        background-color: #1E293B;
        border-radius: 4px;
        height: 6px;
        width: 100%;
        overflow: hidden;
    }

    .risk-bar-fill-suspicious {
        background-color: #F43F5E;
        height: 100%;
    }

    .risk-bar-fill-safe {
        background-color: #10B981;
        height: 100%;
    }

    /* Metrics Grid */
    .metrics-container {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 10px;
        margin-bottom: 20px;
    }

    .metric-card {
        background-color: #111827;
        border: 1px solid #1E293B;
        border-radius: 6px;
        padding: 12px;
        text-align: center;
    }

    .metric-name {
        font-size: 0.7rem;
        font-weight: 600;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 4px;
    }

    .metric-number {
        font-size: 1.1rem;
        font-weight: 700;
        color: #F1F5F9;
    }

    /* Footer Info Bar */
    .footer-bar {
        background-color: #111827;
        border: 1px solid #1E293B;
        border-radius: 6px;
        padding: 10px 14px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        font-size: 0.8rem;
        color: #94A3B8;
    }

    .footer-item {
        display: flex;
        align-items: center;
        gap: 6px;
    }

    .highlight-val {
        color: #F8FAFC;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# SVG Icons (Monochrome & Professional)
SVG_SHIELD = """<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#F8FAFC" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/></svg>"""
SVG_ALERT = """<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#F43F5E" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>"""
SVG_CHECK = """<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#10B981" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22c5.523 0 10-4.477 10-10S17.523 2 12 2 2 6.477 2 12s4.477 10 10 10z"/><path d="m9 12 2 2 4-4"/></svg>"""
SVG_ZAP = """<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#94A3B8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>"""
SVG_LOCK = """<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#10B981" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="11" x="3" y="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>"""

# Header Banner
st.markdown(f"""
<div class="enterprise-header">
    <div class="header-top">
        <div class="header-title-group">
            {SVG_SHIELD}
            <h1 class="header-title">LinkSentinel</h1>
        </div>
        <span class="version-tag">INLINE ML ENGINE</span>
    </div>
    <p class="header-desc">
        Real-Time Static URL Risk Assessment Architecture. Analysis executes 100% in-memory without initiating destination network connections.
    </p>
</div>
""", unsafe_allow_html=True)

# Load Extractor & Trained Model Artifacts
@st.cache_resource
def load_resources():
    extractor = URLLexicalFeatureExtractor()
    models = joblib.load("models/linksentinel_models.joblib")
    rf_model = models["engine_rf"]
    feature_names = models["feature_names"]
    return extractor, rf_model, feature_names

try:
    extractor, model, feature_names = load_resources()
    resources_loaded = True
except Exception as e:
    st.error(f"Error loading model artifacts: {e}")
    resources_loaded = False

# Input Section
st.markdown("""
<div class="input-label">Target URL Input</div>
""", unsafe_allow_html=True)

url_input = st.text_input(
    label="Target URL",
    label_visibility="collapsed",
    value="http://login.paypal.account-verify.com/update?id=123",
    placeholder="https://example.com/login"
)

if st.button("RUN STATIC RISK ANALYSIS") and resources_loaded:
    if not url_input.strip():
        st.warning("Please enter a valid URL.")
    else:
        # Start timer
        start_time = time.perf_counter()

        # 1. Extract static features
        features_dict = extractor.extract(url_input)
        X_input = pd.DataFrame([features_dict])[feature_names]

        # 2. Predict probability via Random Forest model
        prob_suspicious = float(model.predict_proba(X_input)[0])
        prediction = 1 if prob_suspicious >= 0.30 else 0
        prob_pct = prob_suspicious * 100.0

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        # Classification Result Panel
        if prediction == 1:
            panel_class = "panel-suspicious"
            title_class = "status-title-suspicious"
            status_icon = SVG_ALERT
            status_text = "SUSPICIOUS"
            bar_fill = "risk-bar-fill-suspicious"
        else:
            panel_class = "panel-safe"
            title_class = "status-title-safe"
            status_icon = SVG_CHECK
            status_text = "SAFE-LOOKING"
            bar_fill = "risk-bar-fill-safe"

        st.markdown(f"""
        <div class="result-panel {panel_class}">
            <div class="panel-top">
                <div class="status-group">
                    {status_icon}
                    <span class="{title_class}">CLASSIFICATION: {status_text}</span>
                </div>
                <div>
                    <div class="prob-sub">Risk Score</div>
                    <div class="prob-val">{prob_pct:.1f}%</div>
                </div>
            </div>
            <div class="risk-bar-track">
                <div class="{bar_fill}" style="width: {max(4.0, prob_pct):.1f}%;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Feature Metrics Summary Grid
        st.markdown(f"""
        <div class="metrics-container">
            <div class="metric-card">
                <div class="metric-name">Length</div>
                <div class="metric-number">{features_dict.get('url_length', 0)}</div>
            </div>
            <div class="metric-card">
                <div class="metric-name">Subdomains</div>
                <div class="metric-number">{features_dict.get('num_subdomains', 0)}</div>
            </div>
            <div class="metric-card">
                <div class="metric-name">Lures</div>
                <div class="metric-number">{features_dict.get('suspicious_keyword_count', 0)}</div>
            </div>
            <div class="metric-card">
                <div class="metric-name">HTTPS</div>
                <div class="metric-number">{'Yes' if features_dict.get('has_https')==1 else 'No'}</div>
            </div>
            <div class="metric-card">
                <div class="metric-name">Digits</div>
                <div class="metric-number">{features_dict.get('num_digits', 0)}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Footer Information Bar
        st.markdown(f"""
        <div class="footer-bar">
            <div class="footer-item">
                {SVG_ZAP}
                <span>Inference Latency: <span class="highlight-val">{elapsed_ms:.2f} ms</span> (Target: &lt;50 ms)</span>
            </div>
            <div class="footer-item">
                {SVG_LOCK}
                <span>Static Parsing Engine (Zero Destination Access)</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='margin-top: 16px;'></div>", unsafe_allow_html=True)
        with st.expander("View Full Static Feature Matrix"):
            st.json(features_dict)
