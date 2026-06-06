from fastapi import FastAPI
from app.api.routes import auth, job_applications
from app.core.logging_config import logger

app = FastAPI()

logger.info("Job Tracker API started")

app.include_router(auth.router)
app.include_router(job_applications.router)


@app.get("/")
def root():
    return {"message": "Job Tracker API is running"}


@app.get("/health")
def health():
    return {"status": "healthy"}