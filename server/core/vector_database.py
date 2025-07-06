import os

from typing import List
from fastapi import UploadFile

from config.settings import GOOGLE_API_KEY, VECTORSTORE_DIRECTORY, MODEL_OPTIONS
from core.document_processor import save_uploaded_file, load_documents_from_paths, split_documents_to_chunks

from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from utils.logger import logger


def vectorstore_exists(persist_path: str) -> bool:
  exists = os.path.exists(persist_path) and bool(os.listdir(persist_path))
  logger.debug(f"Vectorstore exists at {persist_path}: {exists}")
  return exists

def get_embeddings(model_provider: str):
  logger.debug(f"Getting embeddings for provider: {model_provider}")
  if model_provider == "groq":
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L12-v2")
  elif model_provider == "gemini":
    return GoogleGenerativeAIEmbeddings(
      model="models/embedding-001",
      google_api_key=GOOGLE_API_KEY
    )
  else:
    logger.error(f"Unsupported LLM Provider: {model_provider}")
    raise ValueError(f"Unsupported LLM Provider: {model_provider}")

def initialize_empty_vectorstores():
  logger.info("Initializing empty vectorstores...")
  for provider in MODEL_OPTIONS.keys():
    persist_path = VECTORSTORE_DIRECTORY[provider]
    os.makedirs(persist_path, exist_ok=True)

    if not os.listdir(persist_path):
      embedding = get_embeddings(provider)
      Chroma(
        embedding_function=embedding,
        persist_directory=persist_path
      )
      logger.debug(f"Initialized vectorstore for {provider} at {persist_path}")

  logger.info("Vectorstore initialization complete.")

async def upsert_vectorstore_from_pdfs(uploaded_files: List[UploadFile], model_provider: str):
  logger.debug(f"Upserting vectorstore for {model_provider}")
  file_paths = await save_uploaded_file(uploaded_files)
  docs = load_documents_from_paths(file_paths)
  chunks = split_documents_to_chunks(docs)
  embedding = get_embeddings(model_provider)

  persist_path = VECTORSTORE_DIRECTORY[model_provider]

  if vectorstore_exists(persist_path):
    logger.debug("Appending to existing vectorstore...")
    vectorstore = Chroma(persist_directory=persist_path, embedding_function=embedding)
    vectorstore.add_documents(chunks)
    logger.debug(f"Added {len(chunks)} chunks to existing vectorstore.")
  else:
    vectorstore = Chroma.from_documents(documents=chunks, embedding=embedding, persist_directory=persist_path)
    logger.debug(f"Created new vectorstore with {len(chunks)} chunks.")

  return vectorstore

def load_vectorstore(model_provider: str):
  persist_path = VECTORSTORE_DIRECTORY[model_provider]
  logger.debug(f"Loading vectorstore from {persist_path}")

  if vectorstore_exists(persist_path):
    logger.debug(f"Loading existing vectorstore for provider: {model_provider}")
    return Chroma(persist_directory=persist_path, embedding_function=get_embeddings(model_provider))

  logger.debug(f"VectorStore not found for provider: {model_provider}")
  raise ValueError(f"VectorStore not found for provider: {model_provider}")

def get_collections_count(model_provider: str):
  logger.debug(f"Getting collection count for provider: {model_provider}")
  vectorstore = load_vectorstore(model_provider)
  return vectorstore._collection.count()

def find_similar_chunks(model_provider: str, query: str):
  logger.debug(f"Searching for similar chunks for provider: {model_provider}")
  vectorstore = load_vectorstore(model_provider)
  return vectorstore.similarity_search(query)
