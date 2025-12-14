import streamlit as st
import pandas as pd
import os
from PyPDF2 import PdfReader
from transformers import pipeline

# ---------- CONFIG ----------
st.set_page_config(page_title="Operational Excellence Dashboard", layout="wide")
st.title("📊 Operational Excellence File Intelligence Dashboard")

# ---------- FILE PATH ----------
folder_path = st.text_input(
    "Enter folder path (example: C:/Consulting_Data)",
    value="C:/Consulting_Data"
)

# ---------- SUMMARIZER ----------
@st.cache_resource
def load_summarizer():
    return pipeline("summarization", model="facebook/bart-large-cnn")

summarizer = load_summarizer()

def summarize_text(text):
    if len(text.split()) < 80:
        return text
    return summarizer(text, max_length=150, min_length=60, do_sample=False)[0]['summary_text']

# ---------- FILE READERS ----------
def read_file(file_path):
    if file_path.endswith(".csv"):
        return pd.read_csv(file_path).to_string()
    elif file_path.endswith(".xlsx"):
        return pd.read_excel(file_path).to_string()
    elif file_path.endswith(".pdf"):
        reader = PdfReader(file_path)
        return " ".join([page.extract_text() for page in reader.pages if page.extract_text()])
    elif file_path.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    else:
        return ""

# ---------- DASHBOARD ----------
if os.path.exists(folder_path):

    files = os.listdir(folder_path)
    selected_file = st.selectbox("Select a file", files)

    if selected_file:
        file_path = os.path.join(folder_path, selected_file)
        raw_text = read_file(file_path)

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📄 File Content (Extracted)")
            st.text_area("Content", raw_text[:5000], height=300)

        with col2:
            st.subheader("🧠 AI Summary")
            summary = summarize_text(raw_text)
            st.success(summary)

        # ---------- CONSULTING INSIGHTS ----------
        st.divider()
        st.subheader("🏭 Operational Excellence Consulting Snapshot")

        col3, col4, col5 = st.columns(3)

        with col3:
            st.markdown("### 🛠 Tools Used")
            st.markdown("""
            • Lean Six Sigma (DMAIC)  
            • Process Mapping (VSM, SIPOC)  
            • Power BI / Tableau  
            • Excel Solver & VBA  
            • RPA (UiPath, Power Automate)  
            • ERP / SAP Analytics  
            """)

        with col4:
            st.markdown("### 📈 Impact Created")
            st.markdown("""
            • 15–30% cost reduction  
            • 20–40% cycle time improvement  
            • Productivity uplift  
            • Reduction in defects & rework  
            • Data-driven decision making  
            """)

        with col5:
            st.markdown("### 🏢 Industries Catered")
            st.markdown("""
            • Manufacturing  
            • FMCG  
            • BFSI  
            • Logistics & Supply Chain  
            • Energy & Utilities  
            • Retail & E-commerce  
            """)

else:
    st.error("❌ Folder path does not exist")
