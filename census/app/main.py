from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config.db import init_db

from web.routes import camera, group, status

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(camera.router)
app.include_router(group.router)
app.include_router(status.router)


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/health")
async def root():
    return {"message": "Sucksex"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True, host="0.0.0.0", port=8000)
