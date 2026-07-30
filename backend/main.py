import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from controller.assessment_controller import router
from database import init_db

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

app = FastAPI(title="Assessment Automation API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)


@app.exception_handler(Exception)
async def unexpected_error_handler(request: Request, error: Exception):
    logging.getLogger(__name__).exception("Unexpected request failure: %s %s", request.method, request.url.path)
    return JSONResponse(status_code=500, content={"success": False, "message": "Unexpected server error.", "data": None})


@app.on_event("startup")
def startup():
    init_db()
