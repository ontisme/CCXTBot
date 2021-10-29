import json
from time import sleep
import ccxt


class TradeClient:
    def __init__(self, platform, _api_key, _api_secret):
        self.api_secret = _api_secret
        self.api_key = _api_key
        if platform == "ftx":
            self.api = ccxt.ftx({
                'apiKey': self.api_key,
                'secret': self.api_secret,
                'enableRateLimit': True
            })
        elif platform == "binance":
            self.api = ccxt.binance({
                'apiKey': self.api_key,
                'secret': self.api_secret,
                'enableRateLimit': True
            })
        else:
            raise ValueError("未填入或不支援的交易所名稱")

    # 取得錢包資料
    def get_wallet(self):
        ret = self.api.fetch_balance()
        if ret:
            info = {
                "totalValue": 0,
                "wallet": []
            }

            result = ret["info"]["result"]
            for i in result:
                if float(i["total"]) > 0:
                    info["totalValue"] += float(i["usdValue"])
                    data = {
                        "coin": i['coin'],
                        "total": i['total'],
                        "free": i['free'],
                        "usdValue": i['usdValue']
                    }
                    info["wallet"].append(data)
            return info
        else:
            return False

    # 取得當前幣種
    def get_markets(self):
        if self.api.load_markets():
            return self.api.symbols
        else:
            print("讀取幣種失敗")
            return False

    # 取得所有訂單
    def get_all_orders(self):
        return self.api.fetch_open_orders()

    # 撤銷所有訂單
    def cancel_all_orders(self):
        ret = self.api.cancel_all_orders()
        if ret:
            return True
        else:
            return False


    def create_order_limit_buy(self, symbol: str, amount: float, limit_price: float):
        symbol = f"{symbol}/USDT"
        type = 'limit'  # or 'market', other types aren't unified yet
        side = 'buy'
        amount = amount  # your amount
        price = limit_price  # your price

        order = self.api.create_order(symbol, type, side, amount, price)
        return order

    def create_order_limit_sell(self, symbol: str, amount: float, limit_price: float):
        symbol = f"{symbol}/USDT"
        type = 'limit'  # or 'market', other types aren't unified yet
        side = 'sell'
        amount = amount  # your amount
        price = limit_price  # your price

        order = self.api.create_order(symbol, type, side, amount, price)
        return order

    # 分倉建單
    def create_order_in_range(self, symbol: str, type: str, min_price: float, max_price: float,
                              batch_count: int, total_price: float):
        for i in range(batch_count):
            batch_order_price = round(max_price - (max_price - min_price) / (batch_count - 1) * i, 2)  # 區間掛單價格
            batch_order_amount = round((total_price / batch_count) / batch_order_price, 9)  # 區間掛單數量

            if type == "buy":
                self.create_order_limit_buy(symbol, batch_order_amount, batch_order_price)
                return True
            elif type == "sell":
                self.create_order_limit_sell(symbol, batch_order_amount, batch_order_price)
                return True
            else:
                raise ValueError("不支援的交易類型名稱")

    def sub(self):
        while True:
            result = self.api.fetch_ticker('BTC-PERP')
            print(result['close'])
            sleep(0.01)



# api_key = 'KXthkPeCegKWGPyQqQ0lf0eXrV7PwGBa70KjBZws'  # TODO: Place your API key here
# api_secret = 'cyEQCcmjN_y7ASCwDmBW39amQujii4Lp3oVqZGDM'  # TODO: Place your API secret here
#
# app = TradeClient("ftx", api_key, api_secret)
# app.create_order_in_range("ETH", "buy", 3820, 3940, 10, 3000)

# ret = app.limit_buy("DOGE",1,1)
# ret = app.limit_buy("ETH", 0.001, 2000)
# a = app.cancel_all_orders()
