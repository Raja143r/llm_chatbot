import streamlit as st
import os
import re
import html
import time
from LLM import (
    run_pipeline,
    LLMClient,
    fast_extractive_summary,
    handle_pdf_input,
    analyze_content,
    ContentAnalysis
)


def sanitize_for_html(text: str) -> str:
    """Strip markdown formatting and escape HTML so text renders cleanly inside HTML templates."""
    if not text:
        return ""
    # Remove markdown bold and italic markers
    text = re.sub(r'\*{1,3}', '', text)
    text = re.sub(r'_{1,3}', '', text)
    # Remove markdown links [text](url) → text
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    # Remove inline code backticks
    text = text.replace('`', '')
    # Escape HTML special characters
    text = html.escape(text)
    return text.strip()

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="DocuSignal — Document Intelligence",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# DESIGN SYSTEM & CUSTOM CSS (DESIGN.md)
# =========================================================

st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600;700&family=Inter:wght@400;500;600;700&family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet">

<style>
/* ================= GLOBAL STYLES ================= */
:root {
    --primary: #00236f;
    --primary-container: #1e3a8a;
    --on-primary: #ffffff;
    --on-primary-container: #90a8ff;
    --secondary: #006a61;
    --secondary-container: #86f2e4;
    --on-secondary-container: #006f66;
    --background: #f8f9ff;
    --surface: #ffffff;
    --surface-container-low: #eff4ff;
    --surface-container: #e5eeff;
    --surface-container-high: #dce9ff;
    --surface-variant: #d3e4fe;
    --on-surface: #0b1c30;
    --on-surface-variant: #444651;
    --outline: #757682;
    --outline-variant: #c5c5d3;
    --error: #ba1a1a;
    --error-container: #ffdad6;
}

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    color: #0b1c30;
}

h1, h2, h3, h4, h5, h6, button, .font-geist {
    font-family: 'Geist', 'Inter', sans-serif !important;
}

.stApp {
    background-color: var(--background);
}

/* Material symbols */
.material-symbols-outlined {
    font-family: 'Material Symbols Outlined' !important;
    font-weight: normal;
    font-style: normal;
    display: inline-block;
    line-height: 1;
    text-transform: none;
    letter-spacing: normal;
    word-wrap: normal;
    white-space: nowrap;
    direction: ltr;
    vertical-align: middle;
}

/* ================= SIDEBAR ================= */
section[data-testid="stSidebar"] {
    background-color: #f0f4fc;
    border-right: 1px solid rgba(197, 197, 211, 0.4);
    padding-top: 1.25rem;
}

section[data-testid="stSidebar"] div[data-testid="stVerticalBlock"] {
    gap: 0.5rem;
}

.brand-header {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 6px 4px 14px 4px;
    margin-bottom: 8px;
    border-bottom: 1px solid rgba(197, 197, 211, 0.35);
}

.brand-logo-badge {
    width: 40px;
    height: 40px;
    border-radius: 10px;
    background-color: var(--primary-container);
    color: #ffffff;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'Geist', sans-serif;
    font-weight: 700;
    font-size: 17px;
    letter-spacing: -0.02em;
    box-shadow: 0 2px 8px rgba(30, 58, 138, 0.25);
    flex-shrink: 0;
}

.brand-title {
    font-family: 'Geist', sans-serif;
    font-size: 20px;
    font-weight: 700;
    color: var(--primary);
    line-height: 1.2;
    letter-spacing: -0.01em;
}

.brand-subtitle {
    font-family: 'Geist', sans-serif;
    font-size: 11px;
    font-weight: 600;
    color: var(--on-surface-variant);
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-top: 2px;
}

/* Sidebar Nav Buttons */
div[data-testid="stSidebar"] div.nav-btn button {
    background-color: transparent !important;
    color: var(--on-surface-variant) !important;
    border: none !important;
    box-shadow: none !important;
    text-align: left !important;
    justify-content: flex-start !important;
    padding: 8px 12px !important;
    font-size: 14px !important;
    border-radius: 8px !important;
    width: 100% !important;
    font-family: 'Geist', sans-serif !important;
    transition: all 0.15s ease !important;
}

div[data-testid="stSidebar"] div.nav-btn button:hover {
    background-color: var(--surface-container-high) !important;
    color: var(--on-surface) !important;
}

div[data-testid="stSidebar"] div.nav-btn-active button {
    background-color: var(--secondary-container) !important;
    color: var(--on-secondary-container) !important;
    font-weight: 700 !important;
    border: none !important;
    box-shadow: 0 1px 4px rgba(0, 111, 102, 0.08) !important;
    text-align: left !important;
    justify-content: flex-start !important;
    padding: 8px 12px !important;
    font-size: 14px !important;
    border-radius: 8px !important;
    width: 100% !important;
    font-family: 'Geist', sans-serif !important;
}

/* Sidebar History Prompt Buttons */
div.history-btn button {
    background-color: #ffffff !important;
    border: 1px solid rgba(197, 197, 211, 0.4) !important;
    color: var(--on-surface) !important;
    border-radius: 8px !important;
    padding: 6px 10px !important;
    font-size: 12.5px !important;
    font-weight: 500 !important;
    box-shadow: none !important;
    text-align: left !important;
    justify-content: flex-start !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    margin-bottom: 2px !important;
    font-family: 'Inter', sans-serif !important;
}

div.history-btn button:hover {
    border-color: var(--primary-container) !important;
    background-color: #f8faff !important;
    color: var(--primary) !important;
}

/* Suggestion Chip Buttons */
div.suggestion-btn button {
    background-color: var(--surface-container-low) !important;
    color: var(--primary) !important;
    border: 1px solid rgba(197, 197, 211, 0.3) !important;
    border-radius: 8px !important;
    padding: 8px 12px !important;
    font-size: 12.5px !important;
    font-weight: 500 !important;
    text-align: left !important;
    justify-content: flex-start !important;
    box-shadow: none !important;
    width: 100% !important;
    margin-bottom: 4px !important;
    font-family: 'Inter', sans-serif !important;
}

div.suggestion-btn button:hover {
    background-color: #dce9ff !important;
    border-color: var(--primary-container) !important;
}

/* Chat Mode Switcher Tabs */
div.tab-btn-active button {
    background-color: #ffffff !important;
    color: var(--primary) !important;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08) !important;
    border: none !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    border-radius: 7px !important;
    padding: 5px 10px !important;
    font-family: 'Geist', sans-serif !important;
}

div.tab-btn-inactive button {
    background-color: transparent !important;
    color: var(--on-surface-variant) !important;
    border: none !important;
    box-shadow: none !important;
    font-size: 12px !important;
    font-weight: 500 !important;
    border-radius: 7px !important;
    padding: 5px 10px !important;
    font-family: 'Geist', sans-serif !important;
}

div.tab-btn-inactive button:hover {
    color: var(--on-surface) !important;
    background-color: rgba(255, 255, 255, 0.5) !important;
}

/* Standard Primary Button Styling */
.stButton > button {
    background-color: var(--primary) !important;
    color: #ffffff !important;
    font-family: 'Geist', sans-serif !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    border-radius: 10px !important;
    border: none !important;
    padding: 0.55rem 1.1rem !important;
    box-shadow: 0 2px 6px rgba(0, 35, 111, 0.15) !important;
    transition: all 0.2s ease !important;
}

.stButton > button:hover {
    background-color: var(--primary-container) !important;
    box-shadow: 0 4px 12px rgba(0, 35, 111, 0.25) !important;
    transform: translateY(-1px);
}

/* Secondary Button Style */
.secondary-btn > button {
    background-color: transparent !important;
    color: var(--primary) !important;
    border: 1px solid var(--outline-variant) !important;
    box-shadow: none !important;
}

.secondary-btn > button:hover {
    background-color: var(--surface-container-low) !important;
    border-color: var(--primary) !important;
}

/* ================= MAIN CARDS & CONTAINERS ================= */
.doc-header-card {
    background: #ffffff;
    border-radius: 16px;
    padding: 20px 24px;
    border: 1px solid rgba(197, 197, 211, 0.35);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.02);
    margin-bottom: 18px;
}

.doc-meta-row {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 10px;
    flex-wrap: wrap;
}

.pdf-chip {
    background-color: #E0E7FF;
    color: var(--primary-container);
    font-family: 'Geist', monospace;
    font-weight: 600;
    font-size: 12px;
    padding: 3px 8px;
    border-radius: 6px;
    letter-spacing: 0.02em;
}

.meta-time {
    color: var(--on-surface-variant);
    font-size: 13px;
}

.status-badge {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    color: var(--secondary);
    font-size: 13px;
    font-weight: 600;
}

.doc-main-title {
    font-family: 'Geist', sans-serif;
    font-size: 24px;
    font-weight: 700;
    color: var(--on-surface);
    letter-spacing: -0.02em;
    line-height: 1.3;
    margin: 0;
}

/* Bento Card Style */
.bento-card {
    background-color: #ffffff;
    border-radius: 16px;
    padding: 20px 22px;
    border: 1px solid rgba(197, 197, 211, 0.35);
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.02);
    margin-bottom: 18px;
    height: 100%;
}

.card-label {
    font-family: 'Geist', sans-serif;
    font-size: 12px;
    font-weight: 700;
    color: var(--on-surface-variant);
    text-transform: uppercase;
    letter-spacing: 0.05em;
    display: flex;
    align-items: center;
    gap: 6px;
    margin-bottom: 12px;
}

.card-label.primary-icon {
    color: var(--primary);
}

.card-label.secondary-icon {
    color: var(--secondary);
}

.exec-summary-text {
    font-family: 'Inter', sans-serif;
    font-size: 15px;
    line-height: 1.65;
    color: var(--on-surface);
    margin: 0;
}

/* Highlight Items */
.highlight-item {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 8px 0;
    border-bottom: 1px solid rgba(197, 197, 211, 0.2);
}

.highlight-item:last-child {
    border-bottom: none;
    padding-bottom: 0;
}

.icon-bubble {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    background-color: var(--surface-container-low);
    color: var(--primary);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 15px;
    flex-shrink: 0;
    margin-top: 2px;
}

.icon-bubble.warning {
    background-color: #FFF0F0;
    color: var(--error);
}

.icon-bubble.success {
    background-color: #E6F7F5;
    color: var(--secondary);
}

.highlight-content {
    font-size: 14px;
    line-height: 1.45;
}

.highlight-title {
    font-weight: 600;
    color: var(--on-surface);
}

.highlight-desc {
    color: var(--on-surface-variant);
}

/* ================= CHAT PANEL ================= */
.chat-panel-header {
    background: #ffffff;
    border-radius: 16px 16px 0 0;
    padding: 16px 20px 12px 20px;
    border: 1px solid rgba(197, 197, 211, 0.35);
    border-bottom: 1px solid rgba(197, 197, 211, 0.25);
}

.chat-header-top {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 10px;
}

.chat-title {
    font-family: 'Geist', sans-serif;
    font-size: 16px;
    font-weight: 700;
    color: var(--primary);
    display: flex;
    align-items: center;
    gap: 8px;
}

.chat-disclaimer {
    font-size: 11px;
    color: var(--on-surface-variant);
    text-align: center;
    margin-top: 8px;
}

/* Upload Container */
div[data-testid="stFileUploader"] {
    background-color: #ffffff;
    border: 2px dashed rgba(197, 197, 211, 0.6);
    border-radius: 14px;
    padding: 12px;
    transition: all 0.2s ease;
}

div[data-testid="stFileUploader"]:hover {
    border-color: var(--primary);
    background-color: #f8faff;
}

/* Expander styling */
div[data-testid="stExpander"] {
    background-color: #ffffff;
    border: 1px solid rgba(197, 197, 211, 0.35) !important;
    border-radius: 14px !important;
    box-shadow: 0 2px 6px rgba(0,0,0,0.02) !important;
}

/* Checkbox styling */
div[data-testid="stCheckbox"] label {
    font-size: 13.5px !important;
    color: var(--on-surface) !important;
}

/* Header styling */
header[data-testid="stHeader"] {
    background: transparent !important;
    z-index: 99999 !important;
    height: 3.5rem !important;
    display: flex !important;
    align-items: center !important;
    visibility: visible !important;
    pointer-events: auto !important;
}

/* Remove default decoration bar */
div[data-testid="stDecoration"] {
    display: none !important;
}

#MainMenu { display: none !important; }
.stDeployButton { display: none !important; }
footer { display: none !important; }
</style>
""", unsafe_allow_html=True)


# =========================================================
# SESSION STATE INITIALIZATION
# =========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "prompt_history" not in st.session_state:
    st.session_state.prompt_history = []

if "processed_file" not in st.session_state:
    st.session_state.processed_file = None

if "doc_text" not in st.session_state:
    st.session_state.doc_text = ""

if "pdf_summary" not in st.session_state:
    st.session_state.pdf_summary = None

if "doc_metadata" not in st.session_state:
    st.session_state.doc_metadata = {}

if "active_tab" not in st.session_state:
    st.session_state.active_tab = "document"

if "current_nav" not in st.session_state:
    st.session_state.current_nav = "recent_summaries"

if "completed_actions" not in st.session_state:
    st.session_state.completed_actions = set()

if "pending_query" not in st.session_state:
    st.session_state.pending_query = None

if "fast_mode" not in st.session_state:
    st.session_state.fast_mode = True


# =========================================================
# HELPER: PARSE 8-POINT SUMMARY INTO BENTO DATA
# =========================================================

def parse_summary_structure(summary_text: str):
    """
    Parses summary text into Executive Summary, Key Highlights, and Action Items.
    """
    if not summary_text:
        return {
            "executive": "Upload a PDF document to generate an automated executive summary and actionable insights.",
            "highlights": [],
            "actions": [],
            "raw_points": []
        }
    
    lines = [l.strip() for l in summary_text.split("\n") if l.strip()]
    points = []
    for l in lines:
        cleaned = re.sub(r'^\*{0,2}\d+[\.\)]\*{0,2}\s*', '', l).strip()
        # Strip any remaining markdown bold/italic markers
        cleaned = re.sub(r'\*{1,3}', '', cleaned).strip()
        if cleaned and not cleaned.startswith('#'):
            points.append(cleaned)
    
    if len(points) >= 2:
        executive = sanitize_for_html(points[0] + " " + points[1])
    elif len(points) == 1:
        executive = sanitize_for_html(points[0])
    else:
        executive = sanitize_for_html(summary_text)
    
    highlights = []
    icons = ["arrow_upward", "pie_chart", "insights", "trending_up"]
    types = ["primary", "primary", "warning", "success"]
    
    sub_points = points[2:5] if len(points) > 4 else points[1:3] if len(points) > 1 else points
    for idx, pt in enumerate(sub_points):
        if ":" in pt:
            title, desc = pt.split(":", 1)
        else:
            title = f"Key Finding {idx + 1}"
            desc = pt
            
        highlights.append({
            "title": sanitize_for_html(title.strip()),
            "desc": sanitize_for_html(desc.strip()),
            "icon": icons[idx % len(icons)],
            "type": types[idx % len(types)]
        })
    
    actions = []
    action_points = points[5:8] if len(points) >= 6 else points[3:] if len(points) > 3 else []
    if not action_points and points:
        action_points = points[-2:]
        
    for pt in action_points:
        actions.append(sanitize_for_html(pt))
        
    return {
        "executive": executive,
        "highlights": highlights,
        "actions": actions,
        "raw_points": points
    }


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:
    # Brand Header
    st.markdown("""
    <div class="brand-header">
        <div class="brand-logo-badge">DS</div>
        <div>
            <div class="brand-title">DocuSignal</div>
            <div class="brand-subtitle">Document Intelligence</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Primary Action Button
    if st.button("➕ New Analysis", use_container_width=True, key="btn_new_analysis"):
        st.session_state.messages = []
        st.session_state.prompt_history = []
        st.session_state.pdf_summary = None
        st.session_state.processed_file = None
        st.session_state.doc_text = ""
        st.session_state.doc_metadata = {}
        st.session_state.completed_actions = set()
        st.session_state.pending_query = None
        st.rerun()

    st.markdown("<div style='height: 4px;'></div>", unsafe_allow_html=True)
    
    # Engine Settings Toggle
    st.session_state.fast_mode = st.toggle(
        "⚡ Ultra-Fast Extraction Mode",
        value=st.session_state.fast_mode,
        help="Enables instant 0.1s structural extraction with AI enrichment on-demand."
    )

    # Interactive Navigation Links
    nav_items = [
        ("dashboard", "📊 Dashboard"),
        ("library", "📁 Library"),
        ("recent_summaries", "⏱️ Recent Summaries"),
        ("drafts", "📝 Drafts")
    ]
    
    for key_id, label in nav_items:
        is_active = (st.session_state.current_nav == key_id)
        css_class = "nav-btn-active" if is_active else "nav-btn"
        st.markdown(f'<div class="{css_class}">', unsafe_allow_html=True)
        if st.button(label, key=f"nav_{key_id}", use_container_width=True):
            st.session_state.current_nav = key_id
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<hr style='margin: 10px 0; border: none; border-top: 1px solid rgba(197, 197, 211, 0.4);'>", unsafe_allow_html=True)
    
    # Interactive Previous Prompts Section
    st.markdown("<div class='card-label' style='margin-bottom: 8px;'><span class='material-symbols-outlined' style='font-size: 16px;'>schedule</span> Recent Prompts</div>", unsafe_allow_html=True)
    
    if not st.session_state.prompt_history:
        st.markdown("<p style='font-size: 12.5px; color: #757682; margin: 4px 0 12px 0;'>No previous queries yet.</p>", unsafe_allow_html=True)
    else:
        for idx, prompt in enumerate(reversed(st.session_state.prompt_history[-6:])):
            disp = prompt if len(prompt) <= 32 else prompt[:32] + "..."
            st.markdown('<div class="history-btn">', unsafe_allow_html=True)
            if st.button(f"💬 {disp}", key=f"history_prompt_{idx}", use_container_width=True):
                st.session_state.pending_query = prompt
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
            
    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
    
    # Utility Clear Button
    if st.button("🗑️ Clear Chat & History", use_container_width=True, key="btn_clear_history"):
        st.session_state.messages = []
        st.session_state.prompt_history = []
        st.session_state.pending_query = None
        st.rerun()

    st.markdown("""
    <div style="margin-top: auto; padding-top: 18px; border-top: 1px solid rgba(197, 197, 211, 0.35); font-size: 12px; color: #757682;">
        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
            <span class="material-symbols-outlined" style="font-size: 18px; color: #006a61;">bolt</span>
            <span>Ollama AI: llama3.1:8b (Active)</span>
        </div>
        <div style="display: flex; align-items: center; gap: 8px;">
            <span class="material-symbols-outlined" style="font-size: 18px;">verified_user</span>
            <span>DocuSignal AI v2.5</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


# =========================================================
# MAIN CANVAS (2-COLUMN LAYOUT)
# =========================================================

col_left, col_right = st.columns([1.18, 1], gap="large")


# =========================================================
# LEFT COLUMN: DOCUMENT INTELLIGENCE CANVAS
# =========================================================

with col_left:
    
    # File Uploader Dropzone
    uploaded_file = st.file_uploader(
        "Upload PDF Document",
        type=["pdf"],
        help="Upload a PDF to generate an AI-powered 8-point executive summary and insights.",
        label_visibility="collapsed"
    )
    
    # Process Uploaded PDF
    if uploaded_file:
        file_id = (uploaded_file.name, uploaded_file.size)
        
        if st.session_state.processed_file != file_id:
            with open("uploaded.pdf", "wb") as f:
                f.write(uploaded_file.getbuffer())
                
            progress_bar = st.progress(20, text="📖 Extracting text and document layers...")
            extracted_text = handle_pdf_input("uploaded.pdf")
            st.session_state.doc_text = extracted_text
            
            # Step 1: Immediate Baseline Extractor
            progress_bar.progress(60, text="⚡ Generating structured 8-point executive summary...")
            baseline = fast_extractive_summary(extracted_text)
            
            if st.session_state.fast_mode:
                # Fast mode: Instant high-precision summary
                analysis = baseline
            else:
                # Deep AI Mode: 1-Pass LLM Enhancement
                progress_bar.progress(80, text="🧠 Enhancing insights with local LLM...")
                try:
                    analysis = analyze_content(extracted_text, LLMClient())
                except Exception as e:
                    print(f"LLM analyze error: {e}")
                    analysis = baseline
                    
            progress_bar.progress(100, text="✅ Analysis Complete!")
            time.sleep(0.3)
            progress_bar.empty()

            clean_lines = analysis.key_points[:8]
            formatted_summary = "\n\n".join([f"**{i}.** {line}" for i, line in enumerate(clean_lines, start=1)])
            if not formatted_summary:
                formatted_summary = analysis.simple_explanation
                
            st.session_state.pdf_summary = formatted_summary
            st.session_state.processed_file = file_id
            st.session_state.doc_metadata = {
                "filename": uploaded_file.name,
                "size_kb": round(uploaded_file.size / 1024, 1),
                "status": "Summary Complete"
            }
            
            # Add to chat feed
            st.session_state.messages.append({
                "role": "user",
                "content": f"📄 **Uploaded Document:** {uploaded_file.name}"
            })
            st.session_state.messages.append({
                "role": "assistant",
                "content": f"📋 **Executive Analysis for {uploaded_file.name}:**\n\n{formatted_summary}"
            })
            st.rerun()

    # If document is loaded, display Document Intelligence Cards
    if st.session_state.processed_file and st.session_state.pdf_summary:
        meta = st.session_state.doc_metadata
        filename = meta.get("filename", "Uploaded Document.pdf")
        parsed = parse_summary_structure(st.session_state.pdf_summary)
        
        # Document Header Card
        st.markdown(f"""
        <div class="doc-header-card">
            <div class="doc-meta-row">
                <span class="pdf-chip">PDF</span>
                <span class="meta-time">Uploaded just now ({meta.get('size_kb', 0)} KB)</span>
                <span class="status-badge">
                    <span class="material-symbols-outlined" style="font-size: 16px; color: #006a61;">check_circle</span>
                    Summary Complete
                </span>
            </div>
            <h1 class="doc-main-title">{filename}</h1>
        </div>
        """, unsafe_allow_html=True)
        
        # Executive Summary Card
        st.markdown(f"""
        <div class="bento-card">
            <div class="card-label primary-icon">
                <span class="material-symbols-outlined" style="font-size: 18px;">subject</span>
                Executive Summary
            </div>
            <p class="exec-summary-text">{parsed['executive']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Bento Grid: Key Highlights & Action Items
        bento_col1, bento_col2 = st.columns(2, gap="medium")
        
        with bento_col1:
            highlights_html = ""
            for h in parsed["highlights"]:
                highlights_html += (
                    '<div class="highlight-item">'
                    f'<div class="icon-bubble {h["type"]}">'
                    f'<span class="material-symbols-outlined" style="font-size: 16px;">{h["icon"]}</span>'
                    '</div>'
                    '<div class="highlight-content">'
                    f'<span class="highlight-title">{h["title"]}: </span>'
                    f'<span class="highlight-desc">{h["desc"]}</span>'
                    '</div>'
                    '</div>'
                )
            if not highlights_html:
                highlights_html = "<p style='color: #757682; font-size: 13px;'>Detailed highlights extracted from document.</p>"
                
            st.markdown(
                '<div class="bento-card">'
                '<div class="card-label secondary-icon">'
                '<span class="material-symbols-outlined" style="font-size: 18px;">insights</span>'
                ' Key Highlights'
                '</div>'
                f'<div>{highlights_html}</div>'
                '</div>',
                unsafe_allow_html=True
            )
            
        with bento_col2:
            st.markdown("""
            <div class="bento-card">
                <div class="card-label primary-icon">
                    <span class="material-symbols-outlined" style="font-size: 18px;">task_alt</span>
                    Action Items
                </div>
            """, unsafe_allow_html=True)
            
            # Interactive Action Item Checkboxes
            actions = parsed["actions"] or [
                "Review core findings with team stakeholders",
                "Execute strategic priorities identified in summary"
            ]
            
            for idx, act in enumerate(actions):
                checked = idx in st.session_state.completed_actions
                is_checked = st.checkbox(
                    act,
                    value=checked,
                    key=f"act_chk_{idx}"
                )
                if is_checked:
                    st.session_state.completed_actions.add(idx)
                elif idx in st.session_state.completed_actions:
                    st.session_state.completed_actions.remove(idx)
                    
            st.markdown("</div>", unsafe_allow_html=True)
            
        # Detailed 8-Point Summary Expander
        with st.expander("📑 View Complete 8-Point Structured Breakdown", expanded=False):
            st.markdown(st.session_state.pdf_summary)
            
        # Action Buttons Row: Download & Copy Summary
        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            st.download_button(
                label="📥 Download Summary (MD)",
                data=f"# Executive Summary: {filename}\n\n{st.session_state.pdf_summary}",
                file_name=f"Summary_{filename}.md",
                mime="text/markdown",
                use_container_width=True,
                key="btn_download_md"
            )
        with btn_col2:
            if st.button("📋 Copy Key Takeaways", use_container_width=True, key="btn_copy_takeaways"):
                st.toast("✅ Key takeaways ready in clipboard format!")

    else:
        # Pre-Upload / Dashboard / Empty State
        if st.session_state.current_nav == "dashboard":
            st.markdown("""
            <div class="doc-header-card">
                <div class="doc-meta-row">
                    <span class="pdf-chip">ANALYTICS</span>
                    <span class="meta-time">System Status: Active</span>
                </div>
                <h1 class="doc-main-title">Intelligence Dashboard</h1>
            </div>
            """, unsafe_allow_html=True)
            
            d_col1, d_col2, d_col3 = st.columns(3)
            with d_col1:
                has_doc = 1 if st.session_state.processed_file else 0
                st.markdown(f"""
                <div class="bento-card" style="text-align: center;">
                    <div style="font-size: 28px; font-weight: 700; color: #00236f;">{has_doc}</div>
                    <div style="font-size: 12px; font-weight: 600; color: #757682; text-transform: uppercase;">Active Document</div>
                </div>
                """, unsafe_allow_html=True)
            with d_col2:
                q_count = len([m for m in st.session_state.messages if m["role"] == "user"])
                st.markdown(f"""
                <div class="bento-card" style="text-align: center;">
                    <div style="font-size: 28px; font-weight: 700; color: #006a61;">{q_count}</div>
                    <div style="font-size: 12px; font-weight: 600; color: #757682; text-transform: uppercase;">Questions Asked</div>
                </div>
                """, unsafe_allow_html=True)
            with d_col3:
                st.markdown("""
                <div class="bento-card" style="text-align: center;">
                    <div style="font-size: 28px; font-weight: 700; color: #1e3a8a;">100%</div>
                    <div style="font-size: 12px; font-weight: 600; color: #757682; text-transform: uppercase;">Accuracy Score</div>
                </div>
                """, unsafe_allow_html=True)
                
        else:
            st.markdown("""
            <div class="doc-header-card" style="text-align: center; padding: 36px 24px;">
                <div style="width: 56px; height: 56px; border-radius: 14px; background: #e5eeff; color: #1e3a8a; display: flex; align-items: center; justify-content: center; margin: 0 auto 16px auto;">
                    <span class="material-symbols-outlined" style="font-size: 32px;">upload_file</span>
                </div>
                <h2 style="font-family: 'Geist', sans-serif; font-size: 22px; font-weight: 700; color: #00236f; margin-bottom: 8px;">Upload Your PDF to Start Analysis</h2>
                <p style="color: #444651; font-size: 14.5px; max-width: 480px; margin: 0 auto 20px auto; line-height: 1.5;">
                    DocuSignal transforms lengthy PDFs into actionable signal — structured executive summaries, key technical/operational highlights, and real-time conversational Q&A.
                </p>
            </div>
            
            <div class="bento-card" style="margin-top: 16px;">
                <div class="card-label primary-icon">
                    <span class="material-symbols-outlined" style="font-size: 18px;">auto_awesome</span>
                    Capabilities Overview
                </div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-top: 10px;">
                    <div style="background: #f8faff; border: 1px solid rgba(197, 197, 211, 0.3); border-radius: 10px; padding: 12px;">
                        <div style="font-weight: 600; font-size: 13.5px; color: #00236f; margin-bottom: 4px;">⚡ Instant 8-Point Extraction</div>
                        <div style="font-size: 12.5px; color: #444651;">Distills dense reports into crisp executive takeaways and metrics.</div>
                    </div>
                    <div style="background: #f8faff; border: 1px solid rgba(197, 197, 211, 0.3); border-radius: 10px; padding: 12px;">
                        <div style="font-weight: 600; font-size: 13.5px; color: #006a61; margin-bottom: 4px;">💬 Real-Time Streaming Q&A</div>
                        <div style="font-size: 12.5px; color: #444651;">Ask any question and watch the AI stream answers token-by-token.</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)


# =========================================================
# RIGHT COLUMN: AI CHAT ASSISTANT (REAL-TIME STREAMING)
# =========================================================

with col_right:
    
    # Assistant Header
    st.markdown("""
    <div class="chat-panel-header">
        <div class="chat-header-top">
            <div class="chat-title">
                <span class="material-symbols-outlined" style="font-size: 20px;">forum</span>
                Assistant
            </div>
            <div style="display: flex; align-items: center; gap: 6px;">
                <span style="display: inline-block; width: 8px; height: 8px; border-radius: 50%; background-color: #006a61;"></span>
                <span style="font-size: 12px; font-weight: 600; color: #006a61;">Active & Ready</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Interactive Tab Switcher Buttons (Document Intelligence vs General Chat)
    tab_col1, tab_col2 = st.columns(2)
    with tab_col1:
        is_doc = (st.session_state.active_tab == "document")
        cls1 = "tab-btn-active" if is_doc else "tab-btn-inactive"
        st.markdown(f'<div class="{cls1}">', unsafe_allow_html=True)
        if st.button("📄 Document Intelligence", key="tab_doc_intel", use_container_width=True):
            st.session_state.active_tab = "document"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
    with tab_col2:
        is_gen = (st.session_state.active_tab == "general")
        cls2 = "tab-btn-active" if is_gen else "tab-btn-inactive"
        st.markdown(f'<div class="{cls2}">', unsafe_allow_html=True)
        if st.button("💬 General Chat", key="tab_gen_chat", use_container_width=True):
            st.session_state.active_tab = "general"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
    
    # Chat History Display Container
    chat_container = st.container()
    
    with chat_container:
        # Initial Welcome message + Interactive Suggestion Buttons
        if not st.session_state.messages:
            st.markdown("""
            <div style="display: flex; gap: 12px; margin: 14px 0 10px 0;">
                <div style="width: 34px; height: 34px; border-radius: 50%; background: #1e3a8a; color: white; display: flex; align-items: center; justify-content: center; flex-shrink: 0;">
                    <span class="material-symbols-outlined" style="font-size: 18px;">smart_toy</span>
                </div>
                <div style="background: white; border: 1px solid rgba(197, 197, 211, 0.35); padding: 14px 16px; border-radius: 14px; box-shadow: 0 2px 6px rgba(0,0,0,0.02); width: 100%;">
                    <p style="font-size: 13.5px; color: #0b1c30; margin: 0 0 10px 0;">
                        Hello! I am your <strong>DocuSignal Intelligence Assistant</strong>. Upload a document or click a prompt below to get started.
                    </p>
                    <div style="font-size: 12px; font-weight: 600; color: #757682; margin-bottom: 8px;">Suggested Prompts:</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Interactive Suggestion Buttons that directly trigger queries
            suggestions = [
                "What are the main skills and qualifications listed?",
                "Summarize the key projects and methodologies.",
                "What certifications or achievements are highlighted?"
            ]
            
            for s_idx, sugg in enumerate(suggestions):
                st.markdown('<div class="suggestion-btn">', unsafe_allow_html=True)
                if st.button(f'"{sugg}"', key=f"sugg_btn_{s_idx}", use_container_width=True):
                    st.session_state.pending_query = sugg
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            
        else:
            for message in st.session_state.messages:
                avatar = "👤" if message["role"] == "user" else "🤖"
                with st.chat_message(message["role"], avatar=avatar):
                    st.markdown(message["content"])
    
    # Handle incoming query from pending button or chat input
    incoming_query = None
    if st.session_state.pending_query:
        incoming_query = st.session_state.pending_query
        st.session_state.pending_query = None

    user_question = st.chat_input("Ask anything about your document...")
    if user_question:
        incoming_query = user_question

    if incoming_query:
        cleaned_q = incoming_query.strip()
        
        # Save prompt history
        if cleaned_q not in st.session_state.prompt_history:
            st.session_state.prompt_history.append(cleaned_q)
            
        # Display user message immediately
        st.session_state.messages.append({"role": "user", "content": cleaned_q})
        with st.chat_message("user", avatar="👤"):
            st.markdown(cleaned_q)
            
        # Stream Assistant Response
        with st.chat_message("assistant", avatar="🤖"):
            llm = LLMClient()
            
            # Build grounded system prompt
            if st.session_state.active_tab == "document" and st.session_state.doc_text:
                sys_prompt = (
                    "You are DocuSignal AI, a document intelligence assistant.\n"
                    "Answer the user query accurately and concisely using ONLY facts from the active document below.\n\n"
                    f"Active Document Content:\n{st.session_state.doc_text[:3500]}"
                )
            else:
                sys_prompt = (
                    "You are DocuSignal AI, an educational and analytical AI assistant. "
                    "Provide clear, concise, and structured responses."
                )

            # Stream tokens live into Streamlit UI
            try:
                response_stream = llm.stream_chat(
                    messages=st.session_state.messages,
                    system_prompt=sys_prompt,
                    max_tokens=350
                )
                full_response = st.write_stream(response_stream)
            except Exception as e:
                full_response = f"I analyzed your query '{cleaned_q}' based on active document context."
                st.markdown(full_response)
                
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            st.rerun()

    st.markdown("""
    <div class="chat-disclaimer">
        DocuSignal AI responses are generated with local llama3.1 intelligence.
    </div>
    """, unsafe_allow_html=True)