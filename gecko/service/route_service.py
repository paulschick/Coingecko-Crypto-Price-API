from typing import List
from classes.sql_handler import SQLHandler
from classes.api_handler import APIHandler
from classes.configs import Config
from classes.models import CurrencyDetails, PriceCollection
from datetime import datetime, timezone


class PriceRouteService:
    def __init__(self, symbols: List[str]):
        self._symbols = symbols
        self._sql = SQLHandler()
        self._gecko = APIHandler()
        self._config = Config()

    async def handle_pipeline(self) -> PriceCollection:
        if self._check_db() is False:
            await self._get_coininfo()
        return await self._get_prices()

    def _check_db(self) -> bool:
        if self._config.database_path.exists() is False:
            return False
        else:
            return True

    async def _get_coininfo(self) -> None:
        supported_coins = await self._gecko.get_supported_coins()
        self._sql.commit_coins_list(supported_coins)

    def _get_symbol_ids(self) -> PriceCollection:
        supported = list()
        collection: PriceCollection = PriceCollection()
        for symbol in self._symbols:
            query_res = self._sql.query_by_symbol(symbol)
            if len(query_res):
                supported.append(query_res)
            else:
                collection.unsupported.append(symbol)
        for data in supported:
            res = data[0]
            sym = res[0]
            _id = res[1]
            _detail = CurrencyDetails(
                id=_id,
                symbol=sym
            )
            collection.prices.append(_detail)
        return collection

    async def _get_prices(self) -> PriceCollection:
        all_ids = list()
        _details = self._get_symbol_ids()
        for currency_detail in _details.prices:
            _id = currency_detail.id
            all_ids.append(_id)
        all_prices = await self._gecko.get_simple_price(all_ids)
        if type(all_prices) is list:
            for price in all_prices:
                for details in _details.prices:
                    if price.id == details.id:
                        details.price = str(price.price)
            dt: datetime = datetime.now(timezone.utc)
            nonce: str = str(int(dt.timestamp() * 1000))
            _details.timestamp = nonce
            return _details
