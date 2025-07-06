import uvicorn

from fastapi import FastAPI

from api.routes import router
from core.vector_database import initialize_empty_vectorstores
from utils.logger import logger


app = FastAPI(title="RAG PDFBot", description="Chat with multiple PDFs :books:")
app.include_router(router)

@app.on_event("startup")
async def startup_event():
  logger.info("Starting up app...")
  initialize_empty_vectorstores()
  logger.info("Startup complete.")

if __name__ == "__main__":
  logger.info("Running app...")
  uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
