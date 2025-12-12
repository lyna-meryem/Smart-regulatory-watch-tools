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
    logo_url = "https://www.bge.asso.fr/wp-content/uploads/2023/04/format-logos-sg.png"  # URL du logo web
    st.markdown(
        f"""
        <div style="text-align:center; margin-bottom: 20px;">
            <img src="{logo_url}" width="180" style="margin-bottom: 10px;">
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

        bank = st.text_input("Bank name:", value="BCL")  # Banque d'origine

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
            # On suppose que l'agent peut gérer plusieurs mots-clés et la banque
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
