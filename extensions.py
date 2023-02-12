import requests
import json
from config import keys

class APIException(Exception):
    pass

class ManyConverter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        if quote == base:
            raise APIException(f'Две одинаковые валюты! Нет смысла конвертировать{base}!')

        try:
            quote_ticket = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обратотать валюту {quote}')

        try:
            base_ticket = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обратотать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать кол-во {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticket}&tsyms={base_ticket}')
        total_base = json.loads(r.content)[keys[base]]
        save = total_base * amount

        return save
