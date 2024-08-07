from fastapi import FastAPI
from API.routers import load_routers
from API import views

app = FastAPI()


@app.get("/fast-api")
def read_root():
    return {"Hello": "World"}


for router, prefix, tag in load_routers():
    app.include_router(
        router = router,
        prefix = prefix,
        tags = tag
    )