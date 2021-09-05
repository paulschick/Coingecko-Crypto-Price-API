import os
from yaml import safe_load, YAMLError
from pathlib import Path
from typing import Dict, List, Iterable, Any, Tuple


class Config:
    def __init__(self):
        self._config_path: Path = Path(
            os.path.join(Path(__file__).parent.parent),
            'api_config.yml'
        )
        self._config: Dict = self._load_config()
        self._base_uri: str = self._config.get('base_uri', '')
        self._coins_list_endpoint: str = self._config.get('coins_list_endpoint', '')
        self._price_endpoint: str = self._config.get('price_endpoint', '')
        self._db_name: str = self._config.get('db_name', '')
        self._db_table: str = self._config.get('db_table', '')

    def _load_config(self) -> Dict:
        with open(self._config_path, 'r') as f:
            try:
                config: Dict = safe_load(f)
                return config
            except YAMLError as e:
                raise e
            finally:
                f.close()

    @property
    def config(self) -> Dict:
        return self._config

    @property
    def database_path(self) -> Path:
        return Path(
            os.path.join(Path(__file__).parent.parent),
            'data',
            self._db_name
        )

    @property
    def database_table(self) -> str:
        return self._db_table

    @property
    def coins_list_uri(self) -> str:
        return self._base_uri + self._coins_list_endpoint

    @property
    def simple_price_base_uri(self) -> str:
        return self._base_uri + self._price_endpoint

    @staticmethod
    def yield_last(it: Iterable[Any]) -> Iterable[Tuple[bool, Any]]:
        """
        Reference:
        https://betterprogramming.pub/is-this-the-last-element-of-my-python-for-loop-784f5ff90bb5
        """
        iterable = iter(it)
        ret_var = next(iterable)
        for v in iterable:
            yield False, ret_var
            ret_var = v
        yield True, ret_var

    def simple_price_uri(self, symbols: List[str]) -> str:
        base_uri: str = self.simple_price_base_uri
        for is_last, v in self.yield_last(symbols):
            if is_last:
                base_uri = base_uri + v + '&vs_currencies=usd'
            else:
                base_uri = base_uri + v + '%2C'
        return base_uri
