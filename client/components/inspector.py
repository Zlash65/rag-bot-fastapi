import streamlit as st

from utils.helpers import (
  get_documents_count,
  get_similar_chunks
)

from state.session import is_chat_ready


def render_inspect_query(model_provider):
  st.caption("🕵️ Look under the hood")
  try:
    doc_count = get_documents_count(model_provider)
    st.success(f"🔎 {doc_count} documents stored in VectorStore.")
  except Exception as e:
    st.error("⚠️ Could not fetch document count.")
    st.code(str(e))

  query = st.chat_input(
    "🔍 Test a query against VectorStore",
    disabled=not is_chat_ready()
  )

  if not query:
    return

  with st.chat_message("user"):
    st.markdown(query)
  with st.chat_message("ai"):
    with st.spinner("Searching..."):
      try:
        results = get_similar_chunks(model_provider, query)
        if results:
          st.markdown("### 🔎 Top Matching Chunks:")
          for i, doc in enumerate(results):
            content = doc.get("page_content", str(doc))[:300]
            st.markdown(f"**Result {i + 1}:**\n\n{content}...")
        else:
          st.info("No matching chunks found.")
      except Exception as e:
        st.error("❌ Error querying VectorStore")
        st.code(str(e))
