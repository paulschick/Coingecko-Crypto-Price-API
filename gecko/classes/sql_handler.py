import pandas as pd
import sqlite3 as sql
from sqlite3 import OperationalError, DataError, DatabaseError
from typing import List, Union
from datetime import datetime, timezone
from pandas import DataFrame
from .configs import Config
from .models import CoinsResponse


class SQLHandler:
    def __init__(self):
        self._config: Config = Config()
        self._cols: List[str] = ['id', 'symbol', 'name', 'updated_timestamp']

    @property
    def nonce(self) -> str:
        dt: datetime = datetime.now(timezone.utc)
        return str(int(dt.timestamp() * 1000))

    def commit_coins_list(self, coins: List[CoinsResponse], kill_on_fail: bool = True) -> DataFrame:
        nonce_: str = self.nonce
        data_list: List[List] = list()
        for data in coins:
            data_list.append([data.id, data.symbol, data.name, nonce_])
        df: DataFrame = pd.DataFrame(
            columns=self._cols,
            data=data_list
        )
        with sql.connect(self._config.database_path) as conn:
            try:
                df.to_sql(name=self._config.database_table, con=conn, if_exists='replace')
                return df
            except (OperationalError, DataError, DatabaseError) as e:
                if kill_on_fail is True:
                    raise e
                else:
                    print(e)
                    pass

    def query_by_symbol(self, symbol: str) -> Union[List, None]:
        query_ = f"""
        SELECT
                symbol
            ,   id
        FROM {self._config.database_table}
        WHERE symbol = '{symbol}'
        COLLATE NOCASE;
        """
        with sql.connect(self._config.database_path) as conn:
            try:
                cur = conn.cursor()
                cur.execute(query_)
                return cur.fetchall()
            except (OperationalError, DataError, DatabaseError) as e:
                print(e)
                return None

