from ray import serve
from fastapi import APIRouter

from app.models.query import Query
from app.services.generator import TextGenerator

router = APIRouter()


@serve.deployment(route_prefix='/')
@serve.ingress(router)
class QueryRouter(TextGenerator):
    def __init__(self):
        super().__init__()
    
    @router.post('/')
    async def predict(self, request: Query):
        prediction = super().predict(request.query)
        return {'predict': prediction}
