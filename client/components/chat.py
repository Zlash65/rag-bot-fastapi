import pandas as pd
import streamlit as st

from datetime import datetime

from utils.helpers import process_user_input


def render_user_input(model_provider, model):
  disable_input = (
    st.session_state.get("unsubmitted_files", False)
    or not st.session_state.get(f"uploaded_files_{st.session_state.uploader_key}", [])
    or not st.session_state.get("chat_ready")
  )

  question = st.chat_input(
    "💬 Ask a Question from the PDF Files",
    disabled=disable_input
  )

  if not question:
    return

  with st.chat_message("user"):
    st.markdown(question)
  with st.chat_message("ai"):
    with st.spinner("Thinking..."):
      try:
        output = process_user_input(model_provider, model, question)
        st.markdown(output)
        pdf_names = [f.name for f in st.session_state.get("pdf_files")]
        st.session_state.chat_history.append(
          (question, output, model_provider, model, pdf_names, datetime.now())
        )
      except Exception as e:
        st.error(f"Error: {str(e)}")

def render_uploaded_files_expander():
  uploaded_files = st.session_state.get(f"uploaded_files_{st.session_state.uploader_key}", [])
  if uploaded_files and not st.session_state.get("unsubmitted_files"):
    with st.expander("📎 Uploaded Files:"):
      for f in uploaded_files:
        st.markdown(f"- {f.name}")

def render_chat_history():
  for q, a, *_ in st.session_state.get("chat_history", []):
    with st.chat_message("user"):
      st.markdown(q)
    with st.chat_message("ai"):
      st.markdown(a)

def render_download_chat_history():
  df = pd.DataFrame(
    st.session_state.get("chat_history", []),
    columns=["Question", "Answer", "Model", "Model Name", "PDF File", "Timestamp"]
  )

  with st.expander("📎 Download Chat History:"):
    st.sidebar.download_button(
      "📥 Download Chat History",
      data=df.to_csv(index=False),
      file_name="chat_history.csv",
      mime="text/csv"
    )
