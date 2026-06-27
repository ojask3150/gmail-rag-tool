import streamlit as st
import os
from dotenv import load_dotenv
from gmail_loader import GmailLoader
from rag_engine import GmailRAG

st.set_page_config(page_title="Gmail RAG Assistant", layout="wide")

st.title("Gmail RAG Assistant")
st.write("Ask questions about your emails in plain English.")

load_dotenv()

with st.sidebar:
    st.header("Credentials")
    
    gmail_email = st.text_input("Gmail Email", value=os.getenv("GMAIL_EMAIL", ""))
    gmail_password = st.text_input("Gmail App Password", type="password", value=os.getenv("GMAIL_APP_PASSWORD", ""))
    groq_api_key = st.text_input("Groq API Key", type="password", value=os.getenv("GROQ_API_KEY", ""))
    
    days = st.slider("Days to fetch", min_value=1, max_value=30, value=7)
    max_emails = st.slider("Max emails", min_value=5, max_value=50, value=20)
    
    load_btn = st.button("Load Emails", type="primary")

if "rag" not in st.session_state:
    st.session_state.rag = None
    st.session_state.documents = []
    st.session_state.loaded = False

if load_btn:
    if not gmail_email or not gmail_password or not groq_api_key:
        st.error("Please fill in all credentials")
    else:
        with st.spinner("Fetching emails..."):
            try:
                loader = GmailLoader(gmail_email, gmail_password)
                emails = loader.fetch_emails(days=days, max_emails=max_emails)
                st.session_state.documents = emails
                st.success(f"Loaded {len(emails)} emails")
            except Exception as e:
                st.error(f"Gmail error: {e}")
        
        with st.spinner("Building RAG index..."):
            try:
                rag = GmailRAG(groq_api_key)
                count = rag.index_emails(st.session_state.documents)
                st.session_state.rag = rag
                st.session_state.loaded = True
                st.success(f"Indexed {count} emails")
            except Exception as e:
                st.error(f"Indexing error: {e}")

if st.session_state.loaded and st.session_state.rag:
    st.divider()
    
    col1, col2 = st.columns([3, 1])
    with col1:
        question = st.text_input("Ask about your emails:", placeholder="e.g., What are my deadlines?")
    with col2:
        st.write("")
        st.write("")
        ask_btn = st.button("Ask", type="primary", use_container_width=True)
    
    if ask_btn and question:
        with st.spinner("Thinking..."):
            result = st.session_state.rag.query(question)
            st.markdown("Answer")
            st.write(result["answer"])
            
            if result.get("sources"):
                st.markdown("Sources")
                for s in result["sources"][:3]:
                    st.caption(f"{s.get('sender', 'Unknown')} | {s.get('subject', 'No subject')}")
    
    st.divider()
    st.markdown("Try these questions")
    cols = st.columns(3)
    suggestions = [
        "What are my deadlines?",
        "Who sent the most emails?",
        "Any important tasks?",
        "Summarize my emails",
        "Any offers or coupons?",
        "What's the sentiment of my emails?"
    ]
    for i, suggestion in enumerate(suggestions):
        with cols[i % 3]:
            if st.button(suggestion, use_container_width=True):
                st.session_state.question = suggestion
                st.rerun()

st.divider()
st.caption("Your credentials are not stored. They are only used for the current session.")
