from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from classes.models import PriceCollection
from service.route_service import PriceRouteService
from pydantic import BaseModel
from typing import List

app = FastAPI()


class ErrorResponse(BaseModel):
    message: str


@app.get('/')
async def connected():
    return {'status': 200, 'message': 'Connected to Coingecko Price Service'}


@app.get('/prices', response_model=PriceCollection, responses={500: {'model': ErrorResponse}})
async def get_prices(symbols: List[str] = Query(['btc'])):
    service = PriceRouteService(symbols)
    try:
        prices = await service.handle_pipeline()
        return prices
    except Exception as e:
        exception_type = type(e).__name__
        exception_ = f"Exception: {e}"
        exception_msg = f"Exception Type: {exception_type}, {exception_}"
        msg: ErrorResponse = ErrorResponse(message=exception_msg)
        error_res = msg.json()
        return JSONResponse(status_code=500, content=error_res)
