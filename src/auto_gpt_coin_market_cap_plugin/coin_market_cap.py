from requests import get


class CoinMarketCap:
    def __init__(self, api_key: str, base_url: str = "https://pro-api.coinmarketcap.com"):
        self.api_key = api_key
        self.base_url = base_url
        self.request_headers = {
            "X-CMC_PRO_API_KEY": api_key,
            "Accept": "application/json"
        }

    def _get_latest_listings(self, count: int, sort: str = "market_cap") -> list:
        r = get(
            f"{self.base_url}/v1/cryptocurrency/listings/latest",
            headers=self.request_headers,
            params={"limit": count, "sort": sort}
        )
        if r.ok:
            return r.json()["data"]

    def _get_current_quote(self, symbol: str = None, slug: str = None) -> dict:
        params = {}
        if symbol:
            params["symbol"] = symbol.upper()
        if slug:
            params["slug"] = slug

        r = get(
            f"{self.base_url}/v2/cryptocurrency/quotes/latest",
            headers=self.request_headers,
            params=params
        )
        if r.ok:
            # There should always be a single item in the dict so just retrieve the first key and return it
            data = r.json()["data"]
            data_key = list(data.keys())[0]
            return data[data_key][0] if isinstance(data[data_key], list) else data[data_key]

    @staticmethod
    def _strip_response_dict(item: dict) -> dict:
        return {
            "name": item["name"],
            "symbol": item["symbol"],
            "max_supply": item["max_supply"],
            "circulating_supply": item["circulating_supply"],
            "total_supply": item["total_supply"],
            "infinite_supply": item["infinite_supply"],
            "quote": {
                "USD": item["quote"]["USD"]
            }
        }

    def get_current_listings(self, count: int) -> list:
        listings = self._get_latest_listings(count)
        return [
            self._strip_response_dict(item)
            for item in listings
        ]

    def get_current_top_coin_prices(self, count: int) -> list:
        listings = self._get_latest_listings(count)
        return [
            {
                "name": item["name"],
                "symbol": item["symbol"],
                "price": item["quote"]["USD"]["price"]
            }
            for item in listings
        ]

    def get_current_top_coin_by_volume(self, count: int) -> list:
        listings = self._get_latest_listings(count, sort="volume_24h")
        return [
            self._strip_response_dict(item)
            for item in listings
        ]

    def get_current_price_by_symbol(self, symbol: str) -> str:
        quote = self._get_current_quote(symbol=symbol)
        return f"${quote['quote']['USD']['price']}"

    def get_current_price_by_slug(self, slug: str) -> str:
        quote = self._get_current_quote(slug=slug)
        return f"${quote['quote']['USD']['price']}"

    def get_current_quote_by_symbol(self, symbol: str) -> dict:
        return self._get_current_quote(symbol=symbol)

    def get_current_quote_by_slug(self, slug: str) -> dict:
        return self._get_current_quote(slug=slug)
