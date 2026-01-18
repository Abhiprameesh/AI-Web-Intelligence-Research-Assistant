import streamlit as st
import requests

BACKEND_URL = "http://localhost:8000"

st.set_page_config(page_title="AI Web Intelligence Assistant", layout="wide")

st.title("AI Web Intelligence & Research Assistant")

# -------------------------
# Ingestion Section
# -------------------------
st.header("📥 Ingest Knowledge")

urls_text = st.text_area(
    "Enter website URLs (one per line)",
    height=150
)

if st.button("Ingest URLs"):
    urls = [u.strip() for u in urls_text.split("\n") if u.strip()]

    if not urls:
        st.warning("Please enter at least one URL.")
    else:
        response = requests.post(
            f"{BACKEND_URL}/ingest",
            json={"urls": urls}
        )

        if response.status_code == 200:
            job_id = response.json().get("job_id")
            st.success(f"Ingestion started. Job ID: {job_id}")
        else:
            st.error("Failed to start ingestion.")

# -------------------------
# Query Section
# -------------------------
st.header("❓ Ask Questions")

question = st.text_input("Enter your question")

if st.button("Ask"):
    if not question:
        st.warning("Please enter a question.")
    else:
        response = requests.post(
            f"{BACKEND_URL}/rag-query",
            json={"question": question}
        )

        if response.status_code == 200:
            data = response.json()

            st.subheader("Answer")
            st.write(data.get("answer", ""))

            sources = data.get("sources", [])
            if sources:
                st.subheader("Sources")
                for src in sources:
                    st.write(f"- {src}")
        else:
            st.error("Failed to get answer.")
