import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from mangum import Mangum

from .routers import executor
from .routers import snippets

stage = os.environ.get('STAGE', None)
openapi_prefix = f"/{stage}" if stage else "/"

app = FastAPI(
    title='Intrical AI - app',
    version='0.1',
    openapi_prefix=openapi_prefix
)


app.include_router(executor.router)
app.include_router(snippets.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


handler = Mangum(app)
