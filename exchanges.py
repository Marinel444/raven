from decimal import Decimal
import json
import requests


def binance_json_data(asset='USDT', fiat='UAH', bank=None, trade_type='BUY', limit=0):
    data = {
        "asset": asset.upper(),
        "countries": [],
        "fiat": fiat.upper(),
        "page": 1,
        "payTypes": bank,
        "proMerchantAds": False,
        "publisherType": None,
        "rows": 10,
        "shieldMerchantAds": False,
        "tradeType": trade_type.upper(),
        "transAmount": limit,
    }
    response = requests.post('https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search', json=data)
    response = json.loads(response.text)
    return response


def binance_get_spot_price(arg1='usdt', arg2='btc'):
    response = requests.get(f'https://www.binance.com/api/v3/depth?symbol={arg2.upper()}{arg1.upper()}&limit=1000')
    response = json.loads(response.text)
    return response


def binance_get_p2p_scheme(asset='USDT', asset2='BTC', fiat='UAH', bank=None, limit=0):
    if not bank:
        bank = ['Monobank']
    # выдать цену по монете
    data = binance_json_data(asset=asset2, fiat=fiat, bank=bank, trade_type='SELL', limit=limit)
    # цена продажи usdt
    end_point = binance_json_data(asset=asset, fiat=fiat, bank=bank, trade_type="BUY", limit=limit)
    # спотовая цена монеты
    get_spot = binance_get_spot_price(arg1=asset, arg2=asset2)
    data = Decimal(data['data'][0]['adv']['price'])
    data = data - (data * Decimal(0.001))
    get_spot = Decimal(get_spot['bids'][0][0])
    btc = ((100 / data) * get_spot)
    btc = btc - (btc * Decimal(0.001))
    end_point = Decimal(end_point['data'][0]['adv']['price'])
    end_point = end_point - (end_point * Decimal(0.001))
    btc = (((end_point * btc) / 100) - 1) * 100
    text = f"{fiat.upper()}-{asset2.upper()}-{asset.upper()}-{fiat.upper()}" \
           f"\nMаржа: {btc:.3f} %\nбанк: {bank[0]}\nМин.сумма: {limit}"
    return text


coins = {
    'btc': 1,
    'usdt': 2,
    'ht': 4,
    'trx': 22,
    'eth': 3,
    'xrp': 7,
    'ltc': 8,
}
pay_method = {
    'monobank': 49,
    'privatbank': 33,
    'abank': 149,
    'sportbank': 156,
    'neo': 306,
}

fiat_money = {
    'uah': 45,
}


def huobi_get_p2p(bank='monobank', coin='usdt', method='sell', fiat='uah', limit=0):
    response = requests.get(f'https://www.huobi.com/-/x/otc/v1/data/trade-market?coinId={coins[coin.lower()]}'
                            f'&currency={fiat_money[fiat.lower()]}&tradeType={method.lower()}&currPage=1&'
                            f'payMethod={pay_method[bank.lower()]}&acceptOrder=-1&country='
                            f'&blockType=general&online=1&range=0&amount={limit}&onlyTradable=false&isFollowed=false')
    response = json.loads(response.text)
    return response


def huobi_get_price(coin='btc'):
    response = requests.get(
        f'https://www.huobi.com/-/x/hbg/v1/important/currency/introduction/detail?currency={coin.lower()}')
    response = json.loads(response.text)
    return response


def huobi_get_p2p_scheme(bank='monobank', coin='usdt', coin2='btc', fiat='uah', limit=0):
    # покупка монеты
    buy_coin = huobi_get_p2p(bank=bank, coin=coin2, method='buy', fiat=fiat, limit=limit)
    # продажа монеты
    sell_coin = huobi_get_p2p(bank=bank, coin=coin, method='sell', fiat=fiat, limit=limit)
    # выдать спот ценну
    get_spot = huobi_get_price(coin=coin2)
    buy_coin = Decimal(buy_coin['data'][0]['price'])
    sell_coin = Decimal(sell_coin['data'][0]['price'])
    get_spot = Decimal(get_spot['data']['currentPrice'])
    btc = ((100 / buy_coin) * get_spot)
    btc = btc - (btc * Decimal(0.002))
    btc = (((sell_coin * btc) / 100) - 1) * 100
    text = f"{fiat.upper()}-{coin2.upper()}-{coin.upper()}-{fiat.upper()}" \
           f"\nMаржа: {btc:.3f} %\nбанк: {bank}\nМин.сумма: {limit}"
    return text


