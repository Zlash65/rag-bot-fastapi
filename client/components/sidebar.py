import streamlit as st

from types import SimpleNamespace

from state.session import is_chat_ready
from utils.helpers import (
  get_model_providers,
  get_models,
  process_uploaded_pdfs
)


def render_model_selector():
  model_provider = st.selectbox(
    "🔌 Model Provider",
    options=get_model_providers(),
    index=None,
    placeholder="Select a model provider",
    key="model_provider"
  )

  model = st.selectbox(
    "🧠 Select a model",
    options=get_models(model_provider),
    index=None,
    placeholder="Select a model",
    disabled=not model_provider,
    key="model"
  )

  return model_provider or "", model or ""

def render_upload_files_button():
  uploaded_files = st.file_uploader(
    "📚 Upload PDFs",
    type=["pdf"],
    accept_multiple_files=True,
    disabled=not st.session_state.get("model"),
    key=f"uploaded_files_{st.session_state.get('uploader_key')}"
  )

  uploaded_filenames = [f.name for f in uploaded_files] if uploaded_files else []
  session_filenames = [f.name for f in st.session_state.get("pdf_files", [])]
  if uploaded_files and uploaded_filenames != session_filenames:
    st.session_state.update(unsubmitted_files=True)

  submitted = st.button("➡️ Submit", disabled=not st.session_state.get("model"))

  return uploaded_files, submitted

def render_view_selector():
  with st.sidebar.expander("👓 View Options", expanded=False):
    view_option = st.selectbox(
      "🧭 Select View",
      options=["💬 Chat", "🔬 Inspector"],
      index=0,
      placeholder="Select the view",
      disabled=not is_chat_ready(),
      key="view"
    )
    return view_option

def sidebar_file_upload(model_provider):
  uploaded_files, submitted = render_upload_files_button()

  if submitted:
    if uploaded_files:
      file_objs = [
        SimpleNamespace(name=f.name, type=f.type, data=f.read())
        for f in uploaded_files
      ]

      with st.spinner("Processing PDFs..."):
        try:
          process_uploaded_pdfs(model_provider, file_objs)
          st.session_state.update(chat_ready=True)
        except Exception as e:
          st.error(f"Error: {str(e)}")
          return

        st.session_state.update(
          pdf_files=file_objs,
          unsubmitted_files=False
        )
        st.toast("PDFs processed successfully!", icon="✅")
    else:
      st.warning("No files uploaded.")

  return uploaded_files, submitted

def sidebar_provider_change_check(model_provider, model):
  if model_provider != st.session_state.get("last_provider"):
    st.session_state.update(chat_ready=False)
    if model:
      st.session_state.update(last_provider=model_provider)
      if st.session_state.get("pdf_files"):
        with st.spinner(f"Reprocessing PDFs with {model_provider}..."):
          try:
            process_uploaded_pdfs(model_provider, st.session_state.get("pdf_files"))
            st.session_state.update(chat_ready=True)
          except Exception as e:
            st.error(f"Error: {str(e)}")
            return

          st.toast("PDFs reprocessed successfully!", icon="🔁")

def sidebar_utilities():
  with st.expander("🛠️ Utilities", expanded=False):
    col1, col2, col3 = st.columns(3)

    if col1.button("🔄 Reset"):
      st.session_state.clear()
      st.session_state["model_provider"] = None
      st.toast("Session reset.", icon="🔄")
      st.rerun()

    if col2.button("🧹 Clear Chat"):
      st.session_state.chat_history = []
      st.session_state.update(pdf_files=[])
      st.session_state.uploader_key += 1
      st.toast("Chat and PDF cleared.", icon="🧼")
      st.rerun()

    if col3.button("↩️ Undo") and st.session_state.get("chat_history"):
      st.session_state.chat_history.pop()
      st.toast("Last message removed.", icon="↩️")
      st.rerun()
