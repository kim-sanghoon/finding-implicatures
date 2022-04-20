import ray
from ray import serve
from fastapi import FastAPI

from app.routers.query import QueryRouter, router as query_router

app = FastAPI()

ray.init(address='auto', namespace='serve')
serve.start(detached=True)

app.include_router(query_router)
QueryRouter.deploy()
