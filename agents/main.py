import os
import streamlit as st
from datetime import datetime
from analysis_agent import AnalysisComparisonAgent

# -------------------------------------------------------
# 1. BACKEND FIXED PATHS
# -------------------------------------------------------
DEFAULT_OLD_FILE = r"C:\Users\lyna_\Documents\Projet Datathon\agents\AnaCredit - Technical specifications - v1.0.7_track_changes.pdf"
DEFAULT_NEW_FILE = r"C:\Users\lyna_\Documents\Projet Datathon\agents\AnaCredit - Technical specifications - v1.0.7.pdf"

DOC_TYPES = ["PDF", "TXT", "Excel", "Word", "Other"]


# -------------------------------------------------------
# STREAMLIT UI
# -------------------------------------------------------
def main():
    st.set_page_config(
        page_title="Document Change Analyzer",
        layout="centered"
    )

    # ---------- HEADER ----------
    st.markdown(
        """
        <div style="text-align:center; margin-bottom: 20px;">
            <img src="data:image/png;base64,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"
            width="180" style="margin-bottom: 10px;">
            <h1 style="color:#E60028;">Document Change Analyzer</h1>
            <h4 style="color:#333;">Automated comparison and summarization tool</h4>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ---------- INPUT CARD ----------
    with st.container():
        st.markdown("### 🔍 Search Settings")

        keywords_input = st.text_input(
            "Enter keywords (comma-separated):",
            placeholder="e.g., credit risk, default, capital"
        )

        col1, col2 = st.columns(2)
        with col1:
            doc_type = st.selectbox("Document type:", DOC_TYPES)
        with col2:
            selected_date = st.date_input("Select date:", datetime.now())

        bank = st.text_input("Bank name:", value="BCL")

    st.write("---")

    # ---------- RUN ANALYSIS ----------
    run_button = st.button("Run Analysis", type="primary")

    if run_button:
        if not keywords_input.strip():
            st.error("❌ Please enter at least one keyword.")
            return

        keywords = [kw.strip() for kw in keywords_input.split(",") if kw.strip()]

        agent = AnalysisComparisonAgent()

        with st.spinner("Running analysis... Please wait"):
            result = agent.analyze_change(
                DEFAULT_OLD_FILE, DEFAULT_NEW_FILE, keywords, bank=bank
            )

        # ---------- RESULTS ----------
        st.success("Analysis completed successfully!")

        st.markdown("## 📄 Analysis Results")

        st.markdown(
            f"""
            **File analyzed:** {result['filename']}  
            **Bank:** {result['bank']}  
            **Document type:** {doc_type}  
            **Keywords:** {', '.join(result['keywords'])}  
            **Selected date:** {selected_date.strftime('%Y-%m-%d')}  
            **Timestamp:** {result['timestamp']}
            """
        )

        st.markdown("### 📝 Summary Report")
        st.info(result["summary"])


if __name__ == "__main__":
    main()
