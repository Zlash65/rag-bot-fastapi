import os
import aiofiles

from typing import List
from fastapi import UploadFile

from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import TokenTextSplitter

from config.settings import TEMPFILE_UPLOAD_DIRECTORY
from utils.logger import logger


def validate_pdf(file: UploadFile, max_size_mb: int = 200):
  if not file.filename.endswith(".pdf"):
    logger.warning(f"Invalid file type: {file.filename}")
    raise ValueError(f"{file.filename} is not a valid PDF file.")

  file_size_mb = len(file.file.read()) / (1024 * 1024)
  file.file.seek(0)

  if file_size_mb > max_size_mb:
    logger.warning(f"File too large: {file.filename} ({file_size_mb:.2f} MB)")
    raise ValueError(f"PDF file size exceeds the maximum allowed size of {max_size_mb} MB.")

  logger.debug(f"Validated PDF: {file.filename} ({file_size_mb:.2f} MB)")

async def save_uploaded_file(files: List[UploadFile]) -> List[str]:
  os.makedirs(TEMPFILE_UPLOAD_DIRECTORY, exist_ok=True)
  file_paths = []

  for file in files:
    validate_pdf(file)
    file_path = os.path.join(TEMPFILE_UPLOAD_DIRECTORY, file.filename)
    async with aiofiles.open(file_path, "wb") as f:
      content = await file.read()
      await f.write(content)
    file_paths.append(file_path)
    logger.debug(f"Saved uploaded file: {file.filename} to {file_path}")

  return file_paths

def load_documents_from_paths(file_paths: List[str]):
  docs = []
  for file_path in file_paths:
    loader = PyPDFLoader(file_path)
    loaded = loader.load()
    logger.debug(f"Loaded {len(loaded)} documents from {file_path}")
    docs.extend(loaded)

  return docs

def split_documents_to_chunks(docs) -> List[str]:
  text_splitter = TokenTextSplitter(chunk_size=500, chunk_overlap=50)
  chunks = text_splitter.split_documents(docs)
  logger.debug(f"Split {len(docs)} docs into {len(chunks)} chunks")
  return chunks
