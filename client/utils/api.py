import requests
from io import BytesIO

from utils.config import API_URL


def handle_response(response):
  try:
    json_data = response.json()
    if json_data["status"] == "success":
      return json_data.get("data")
    else:
      raise Exception(json_data.get("message", "Unknown error occurred."))
  except Exception as e:
    raise Exception(f"API Error: {str(e)}")

def get_supported_llm() -> list[str]:
  response = requests.get(f"{API_URL}/llm")
  return handle_response(response)

def get_supported_models(model_provider) -> list[str]:
  response = requests.get(f"{API_URL}/llm/{model_provider}")
  return handle_response(response)

def get_vectorstore_colllection_count(model_provider) -> int:
  response = requests.get(f"{API_URL}/vector_store/count/{model_provider}")
  return handle_response(response)

def get_vectorstore_similarity_search(model_provider, query) -> list[dict]:
  payload = {
    "model_provider": model_provider,
    "query": query
  }
  response = requests.post(f"{API_URL}/vector_store/search", json=payload)
  return handle_response(response)

def upload_and_process_pdfs(model_provider, uploaded_files) -> str:
  files = []
  for file in uploaded_files:
    if hasattr(file, "data"):
      files.append(("files", (file.name, BytesIO(file.data), file.type)))
    else:
      files.append(("files", (file.name, file.read(), file.type)))

  data = {
    "model_provider": model_provider
  }

  # Send the POST request with multiple files
  response = requests.post(f"{API_URL}/upload_and_process_pdfs", files=files, data=data)
  return handle_response(response)

def chat(model_provider, model_name, user_input) -> str:
  payload = {
    "model_provider": model_provider,
    "model_name": model_name,
    "message": user_input
  }

  response = requests.post(f"{API_URL}/chat", json=payload)
  return handle_response(response)
