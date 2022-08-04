from fastapi import FastAPI

from app.api.v1.api import api_router
import app.db.base

app = FastAPI(title="Task Manager", openapi_url="/openapi.json")

app.include_router(api_router, prefix='/v1')


if __name__ == "__main__":
    # Use this for debugging purposes only
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000,
                log_level="debug", reload=True)
