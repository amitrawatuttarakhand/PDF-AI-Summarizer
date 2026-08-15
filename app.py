import os
import streamlit as st
from PyPDF2 import PdfReader
from dotenv import load_dotenv

# Import backend classes
from pdf_processor import PDFSummarizer, SummaryFormatter
from utility import TextProcessor, ErrorHandler

# Load environment variables (.env)
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="SummarizeAI — Intelligent PDF Studio",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Styling
st.markdown(
    """
    <style>
        /* Global layout tweaks */
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1000px;
        }

        /* Hero Header */
        .hero-container {
            text-align: center;
            padding: 2.2rem 1.5rem;
            background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #312e81 100%);
            border-radius: 16px;
            color: white;
            margin-bottom: 2rem;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1);
        }
        .hero-title {
            font-size: 2.3rem;
            font-weight: 800;
            letter-spacing: -0.025em;
            margin: 0;
            background: linear-gradient(to right, #ffffff, #c7d2fe);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .hero-subtitle {
            font-size: 1rem;
            color: #94a3b8;
            margin-top: 0.5rem;
            font-weight: 400;
        }

        /* Stat Card Badges */
        .metric-container {
            background-color: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 1.2rem;
            text-align: center;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05);
        }
        .metric-value {
            font-size: 1.6rem;
            font-weight: 700;
            color: #1e293b;
        }
        .metric-label {
            font-size: 0.8rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: #64748b;
            margin-top: 0.2rem;
        }

        /* Summary Card Box */
        .summary-card {
            background: #ffffff;
            border-radius: 14px;
            padding: 1.8rem;
            border: 1px solid #e2e8f0;
            border-left: 5px solid #4f46e5;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            margin-top: 1.5rem;
            line-height: 1.7;
            font-size: 1rem;
            color: #334155;
        }

        /* Buttons */
        div.stButton > button:first-child {
            width: 100%;
            height: 3rem;
            font-size: 1.05rem;
            font-weight: 600;
            border-radius: 10px;
            background: linear-gradient(135deg, #4f46e5 0%, #4338ca 100%);
            color: white;
            border: none;
            transition: all 0.2s ease-in-out;
            box-shadow: 0 4px 14px 0 rgba(79, 70, 229, 0.35);
        }
        div.stButton > button:first-child:hover {
            transform: translateY(-1px);
            box-shadow: 0 6px 20px 0 rgba(79, 70, 229, 0.45);
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Hero Header
st.markdown(
    """
    <div class="hero-container">
        <h1 class="hero-title">✨ Intelligent PDF Summarizer</h1>
        <p class="hero-subtitle">Turn lengthy documents, reports, and papers into actionable insights in seconds.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Sidebar Configuration
with st.sidebar:
    st.markdown("### ⚙️ Summary Settings")
    st.caption("Customize how your document should be analyzed.")

    summary_type_options = {
        "concise": "⚡ Concise (5-10 Sentences)",
        "detailed": "📑 Detailed (Headings & Depth)",
        "bullet_points": "📌 Key Bullet Points",
    }

    selected_type_key = st.selectbox(
        "Format Style",
        options=list(summary_type_options.keys()),
        format_func=lambda x: summary_type_options[x],
        index=0,
    )

    st.markdown("---")
    st.markdown("### 🎯 Fine-Tune Instructions")
    custom_prompt = st.text_area(
        "Custom Prompt",
        placeholder="e.g., Focus on numerical KPIs, financial results, or technical architecture...",
        height=120,
    )

    st.markdown("---")
    st.caption("⚡ Powered by Advanced AI Processing")

# Main Content: File Upload
uploaded_file = st.file_uploader(
    "Upload Document (PDF)",
    type=["pdf"],
    help="Select any text-based PDF file up to 50MB.",
)

if uploaded_file:
    try:
        reader = PdfReader(uploaded_file)
        pages_text = [page.extract_text() or "" for page in reader.pages]
        extracted_text = "\n".join(pages_text).strip()

        if not extracted_text:
            st.warning(
                "⚠️ No readable text detected in this document. It may consist entirely of scanned images."
            )
        else:
            stats = TextProcessor.get_text_statistics(extracted_text)

            # Metadata Display
            st.markdown("#### 📊 Document Overview")
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.markdown(
                    f"""
                    <div class="metric-container">
                        <div class="metric-value">{len(reader.pages)}</div>
                        <div class="metric-label">Pages</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with col2:
                st.markdown(
                    f"""
                    <div class="metric-container">
                        <div class="metric-value">{stats["words"]:,}</div>
                        <div class="metric-label">Words</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with col3:
                st.markdown(
                    f"""
                    <div class="metric-container">
                        <div class="metric-value">{stats["characters"]:,}</div>
                        <div class="metric-label">Characters</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with col4:
                st.markdown(
                    f"""
                    <div class="metric-container">
                        <div class="metric-value">{stats["reading_time"]}</div>
                        <div class="metric-label">Est. Read Time</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            st.write("")

            # Action Button
            if st.button("🚀 Generate Summary", type="primary", use_container_width=True):
                with st.spinner("Analyzing document and extracting insights..."):
                    summarizer = PDFSummarizer()
                    raw_summary = summarizer.summarize(
                        chunks=[extracted_text],
                        summary_type=selected_type_key,
                        custom_prompt=custom_prompt,
                    )
                    formatted_summary = SummaryFormatter.format_summary(raw_summary)

                    st.markdown("### 📝 Generated Summary")
                    st.markdown(
                        f"""
                        <div class="summary-card">
                            {formatted_summary}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    st.download_button(
                        label="📥 Download Summary as Text",
                        data=formatted_summary,
                        file_name=f"summary_{uploaded_file.name.replace('.pdf', '')}.txt",
                        mime="text/plain",
                    )

    except Exception as e:
        error_msg = ErrorHandler.handle_error(e, context="PDF Processing")
        st.error(error_msg)