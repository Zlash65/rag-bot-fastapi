import streamlit as st


def setup_session_state():
  default_state = {
    "chat_history": [],             # Stores tuples of (question, answer, provider, model, pdfs, timestamp)
    "chat_ready": False,            # Tracks whether chat is ready to receive user input
    "pdf_files": [],                # Currently submitted PDF files
    "last_provider": None,          # Tracks last selected provider for dynamic reloading
    "unsubmitted_files": False,     # Tracks whether new files were uploaded but not submitted
    "uploader_key": 0               # Used to reset file_uploader widget
  }

  for key, default in default_state.items():
    if key not in st.session_state:
      st.session_state[key] = default

def is_chat_ready():
  return (
    st.session_state.get("chat_ready")
    and st.session_state.get(f"uploaded_files_{st.session_state.uploader_key}", [])
    and not st.session_state.get("unsubmitted_files")
  )
