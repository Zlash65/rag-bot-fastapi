from fastapi import APIRouter, UploadFile, File, Form

from config.settings import MODEL_OPTIONS
from core.vector_database import (
    get_collections_count,
    find_similar_chunks,
    upsert_vectorstore_from_pdfs,
    load_vectorstore
)
from core.llm_chain_factory import build_llm_chain
from api.schemas import SearchQueryRequest, ChatRequest, StandardAPIResponse
from utils.logger import logger

router = APIRouter()


@router.get("/health", response_model=StandardAPIResponse)
def health_check():
  logger.debug("Health check requested")
  return StandardAPIResponse(
    status="success",
    data="ok",
    message="Service is healthy"
  )

@router.get("/llm", response_model=StandardAPIResponse)
async def get_llm_options():
  logger.debug("Fetching LLM providers.")
  return StandardAPIResponse(
    status="success",
    data=[provider.title() for provider in MODEL_OPTIONS.keys()]
  )

@router.get("/llm/{model_provider}", response_model=StandardAPIResponse)
async def get_llm_models(model_provider: str):
  model_provider = model_provider.lower()
  if model_provider not in MODEL_OPTIONS:
    logger.warning(f"Invalid model provider: {model_provider}")
    return StandardAPIResponse(status="error", message="Invalid model provider.")

  logger.debug(f"Fetching models for provider: {model_provider}")
  return StandardAPIResponse(
    status="success",
    data=MODEL_OPTIONS[model_provider]["models"]
  )

@router.post("/upload_and_process_pdfs", response_model=StandardAPIResponse)
async def upload_and_process_pdfs(
  files: list[UploadFile] = File(...),
  model_provider: str = Form(...)
):
  try:
    model_provider = model_provider.lower()
    logger.info(f"Received {len(files)} files for model provider: {model_provider}")
    await upsert_vectorstore_from_pdfs(files, model_provider)
    logger.info("Files processed successfully")
    return StandardAPIResponse(status="success", data="PDFs processed successfully.")
  except Exception as e:
    logger.exception("Error while uploading and processing files")
    return StandardAPIResponse(status="error", message=str(e))

@router.get("/vector_store/count/{model_provider}", response_model=StandardAPIResponse)
async def get_vectorstore_count(model_provider: str):
  try:
    model_provider = model_provider.lower()
    logger.info(f"Getting collection count for provider: {model_provider}")
    count = get_collections_count(model_provider)
    return StandardAPIResponse(status="success", data=count)
  except Exception as e:
    logger.exception("Error getting collection count")
    return StandardAPIResponse(status="error", message=str(e))

@router.post("/vector_store/search", response_model=StandardAPIResponse)
async def get_vectorstore_search(request: SearchQueryRequest):
  try:
    model_provider = request.model_provider.lower()
    logger.info(f"Search requested with query: {request.query} for provider: {request.model_provider}")
    results = find_similar_chunks(model_provider, request.query)
    return StandardAPIResponse(status="success", data=results)
  except Exception as e:
    logger.exception("Error during similarity search")
    return StandardAPIResponse(status="error", message=str(e))

@router.post("/chat", response_model=StandardAPIResponse)
async def chat(request: ChatRequest):
  try:
    message = request.message
    model_name = request.model_name
    model_provider = request.model_provider.lower()
    logger.debug(f"Chat request for model: {request.model_name} (provider: {request.model_provider})")

    if model_provider not in MODEL_OPTIONS:
      logger.warning("Invalid model provider.")
      return StandardAPIResponse(status="error", message="Invalid model provider.")
    if model_name not in MODEL_OPTIONS[model_provider]["models"]:
      logger.warning("Invalid model name.")
      return StandardAPIResponse(status="error", message="Invalid model name.")

    vectorstore = load_vectorstore(model_provider)
    chain = build_llm_chain(model_provider, model_name, vectorstore)

    if not chain:
      logger.error("Failed to build LLM chain.")
      return StandardAPIResponse(status="error", message="Failed to create LLM chain.")

    response = chain.invoke({"input": message})["answer"]
    logger.debug("Chat response generated successfully")
    return StandardAPIResponse(status="success", data=response)
  except Exception as e:
    logger.exception("Chat endpoint encountered an error")
    return StandardAPIResponse(status="error", message=str(e))
