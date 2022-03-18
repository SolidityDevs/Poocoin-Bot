from pycoingecko import CoinGeckoAPI
cg = CoinGeckoAPI()

import requests,json


def bnbprice():
    try:
        bnb = cryptonator.get_exchange_rate("bnb", "usd")
        return bnb
    except Exception:
        try:
            bnb = cg.get_price(ids='binancecoin', vs_currencies='usd')
            bnb = bnb["binancecoin"]['usd']
            return bnb
        except Exception:
            try:
                url = requests.get('https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?symbol=BNB&convert=USD'
                   ,headers = {'X-CMC_PRO_API_KEY': 'ecf29cc1-a01f-489e-943f-ba37a91a4893'}).json()['data']['BNB']['quote']['USD']['price']
                return url
            except Exception:
                return "0.00000"

              
     


            
            
            
