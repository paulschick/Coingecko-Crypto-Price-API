import aiohttp
from aiohttp import ClientConnectionError, ClientResponseError
from .models import CoinsResponse, SimplePriceResponse
from .configs import Config
from typing import List, Dict, Union


class APIHandler:
    def __init__(self):
        self._config: Config = Config()

    async def get_supported_coins(self) -> List[CoinsResponse]:
        uri: str = self._config.coins_list_uri
        async with aiohttp.ClientSession() as session:
            async with session.get(uri) as resp:
                try:
                    res: List[Dict[str, str]] = await resp.json()
                    res_instances: List[CoinsResponse] = list()
                    for coin in res:
                        instance: CoinsResponse = CoinsResponse(
                            id=coin.get('id', ''),
                            symbol=coin.get('symbol', ''),
                            name=coin.get('name', '')
                        )
                        res_instances.append(instance)
                    return res_instances
                except (
                        ClientConnectionError, ClientResponseError,
                        Exception
                ) as e:
                    print(f'Exception from API: {type(e).__name__}')
                    raise e

    async def get_simple_price(self, currencies: List[str]) -> Union[List[SimplePriceResponse], None]:
        uri: str = self._config.simple_price_uri(currencies)
        async with aiohttp.ClientSession() as session:
            async with session.get(uri) as resp:
                try:
                    res: Union[Dict, None] = await resp.json()
                    if res.get('error', None) is not None:
                        msg = res['error']
                        raise Exception(msg)
                except (
                        ClientConnectionError, ClientResponseError,
                        Exception
                ) as e:
                    print(f'Exception from API: {type(e).__name__}')
                    raise e

                if type(res) is dict:
                    responses: List[SimplePriceResponse] = list()
                    for k, v in res.items():
                        _id = k
                        currency_key_list = list(v.keys())
                        curr = currency_key_list[0]
                        value = v[curr]
                        price_response = SimplePriceResponse(
                            id=_id,
                            quote=curr,
                            price=value
                        )
                        responses.append(price_response)
                    return responses
                else:
                    return None
