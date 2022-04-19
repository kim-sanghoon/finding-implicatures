import ray
from ray import serve
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.responses import JSONResponse

from .model import UnifiedQA

app = FastAPI()
ray.init(address='auto', namespace='unifiedqa')
serve.start(detached=True)

class Query(BaseModel):
    query: str

@serve.deployment(route_prefix='/')
@serve.ingress(app)
class UnifiedQAWrapper(UnifiedQA):
    def __init__(self):
        super().__init__()
    
    @app.post('/')
    async def predict(self, request: Query):
        prediction = super().predict(request.query)
        return JSONResponse({'predict': prediction})

UnifiedQAWrapper.deploy()
