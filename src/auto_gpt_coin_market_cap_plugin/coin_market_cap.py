from requests import get


class CoinMarketCap:
    def __init__(self, api_key: str, base_url: str = "https://pro-api.coinmarketcap.com"):
        self.api_key = api_key
        self.base_url = base_url
        self.request_headers = {
            "X-CMC_PRO_API_KEY": api_key,
            "Accept": "application/json"
        }

    def get_current_listings(self, count):
        r = get(
            f"{self.base_url}/v1/cryptocurrency/listings/latest",
            headers=self.request_headers,
            params={"limit": count}
        )

        if r.ok:
            return [
                {
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
                for item in r.json()["data"]
            ]
        else:
            return None
