import ray
from ray import serve
from fastapi import FastAPI

from app.routers.query import QueryRouter, router as query_router

app = FastAPI()

ray.init()
serve.start()

app.include_router(query_router)
QueryRouter.deploy()
