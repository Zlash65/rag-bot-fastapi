from utils.api import (
  chat,
  get_supported_llm,
  get_supported_models,
  upload_and_process_pdfs,
  get_vectorstore_colllection_count,
  get_vectorstore_similarity_search
)


def get_model_providers() -> list[str]:
  return get_supported_llm()

def get_models(model_provider) -> list[str]:
  if not model_provider:
    return []
  return get_supported_models(model_provider)

def process_uploaded_pdfs(model_provider, uploaded_files) -> str:
  return upload_and_process_pdfs(model_provider, uploaded_files)

def process_user_input(model_provider, model_name, user_input) -> str:
  return chat(model_provider, model_name, user_input)

def get_documents_count(model_provider) -> int:
  return get_vectorstore_colllection_count(model_provider)

def get_similar_chunks(model_provider, query) -> list[dict]:
  return get_vectorstore_similarity_search(model_provider, query)
