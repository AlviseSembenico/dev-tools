import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from mangum import Mangum

from .routers import executor
from .routers import snippets

stage = os.environ.get('STAGE', None)
openapi_prefix = f"/{stage}" if stage else "/"

app = FastAPI(
    title='Devtools - app',
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


@app.get("/ping")
def read_root():
    return {"Status": "Operational"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


handler = Mangum(app)



if __name__ == "__main__":
    '''
    DEBUG Mode on
    '''
    uvicorn.run(app, host="0.0.0.0", port=8000)
else:
    '''
    Production mode
    '''
    import sentry_sdk
    from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

    sentry_sdk.init(
        dsn="https://271dc35e73924161ad8faca434deaa65@o359982.ingest.sentry.io/5872881",
        traces_sample_rate=1.0
    )

    app.add_middleware(SentryAsgiMiddleware)