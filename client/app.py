import streamlit as st

from state.session import setup_session_state, is_chat_ready
from components.chat import (
  render_chat_history,
  render_download_chat_history,
  render_uploaded_files_expander,
  render_user_input
)
from components.sidebar import (
  render_model_selector,
  render_view_selector,
  sidebar_file_upload,
  sidebar_provider_change_check,
  sidebar_utilities
)
from components.inspector import render_inspect_query


def main():
  st.set_page_config(page_title="RAG PDFBot", layout="centered")
  st.title("👽 RAG PDFBot")
  st.caption("Chat with multiple PDFs :books:")

  setup_session_state()

  if st.session_state.get("chat_history"):
    render_download_chat_history()

  with st.sidebar:
    with st.expander("⚙️ Configuration", expanded=True):
      model_provider, model = render_model_selector()
      sidebar_file_upload(model_provider)
      sidebar_provider_change_check(model_provider, model)

    view_option = render_view_selector()
    sidebar_utilities()

  if not st.session_state.get(f"uploaded_files_{st.session_state.uploader_key}", []):
    st.info("📄 Please upload and submit PDFs to start chatting.")

  if st.session_state.get("unsubmitted_files", False):
    st.warning("📄 New PDFs uploaded. Please submit before chatting.")

  if st.session_state.get("chat_ready") and st.session_state.get("pdf_files", []):
    render_uploaded_files_expander()

  if view_option == "💬 Chat":
    if st.session_state.get("chat_history", []):
      render_chat_history()

    if is_chat_ready():
      render_user_input(model_provider, model)
  elif view_option == "🔬 Inspector":
    if is_chat_ready():
      render_inspect_query(model_provider)

if __name__ == "__main__":
    main()
