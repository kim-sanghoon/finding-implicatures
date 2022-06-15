import ray
from ray import serve
from fastapi import FastAPI

from app.routers.query import QueryRouter, router as query_router

app = FastAPI()

ray.init(address="auto")
serve.start(detached=True, http_options={
    'host': '0.0.0.0',
})

app.include_router(query_router)
QueryRouter.deploy()
