# CoinGecko Crypto Price API

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Simple Python3 and FastAPI wrapper for fetching prices using *symbols* from the [CoinGecko API](https://www.coingecko.com/en).

## Setup

### Requirements

[Docker Compose](https://docs.docker.com/compose/install/) or just
[Docker](https://docs.docker.com/get-docker/) to use it with just the `Dockerfile`.

### Get From Source

Clone the repository, and run `docker-compose up -d`, or run the `Dockerfile` directly.

```shell
git clone https://github.com/paulschick/Coingecko-Crypto-Price-API.git
cd Coingecko-Crypto-Price-API
docker-compose up -d
```

## Usage

Starting the container will run the [FastAPI](https://fastapi.tiangolo.com/) server on
port 4004. You can open the browser to `http://0.0.0.0:4004` to start making requests.

I made this application as a simple addition to a collection of apps that I'm working on for
dealing with cryptocurrency exchanges. I chose CoinGecko because of its wide variety of
cryptocurrencies with USD values available.

The first time you hit the `/prices` endpoint, the application will request all available
cryptocurrencies from the CoinGecko API and store them in a sqlite database in the `data/` directory.
As long as this persists, it will always refer to this database.

Right now, there's no endpoint to force-refresh the database, so if you want the API to
update the database, you'll have to clear out the volume for the Docker container.

```shell
curl http://0.0.0.0:4004/prices?symbols=btc
```

To get multiple currencies, you can add `&symbols=` as many times as you like.

```shell
curl http://0.0.0.0:4004/prices?symbols=btc&symbols=eth&symbols=bnb
```

If you pass in a symbol that's not supported by CoinGecko, the API will return these symbols
back in the response object, rather than error out.

**Note** timestamps are returned in *milliseconds*.

The response object (Pydantic):

```python
class CurrencyDetails(BaseModel):
    id: str
    symbol: str
    price: str = ''

    
class PriceCollection(BaseModel):
    timestamp: str
    prices: List[CurrencyDetails] = []
    unsupported: List[str] = []
```

```json
{
  "timestamp": "1631185695443",
  "prices": [
    {
      "id": "bitcoin",
      "symbol": "btc",
      "price": "50000"
    } 
  ],
  "unsupported": []
}
```
