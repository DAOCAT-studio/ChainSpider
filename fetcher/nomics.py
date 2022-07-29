import json
from pprint import pprint as pp

import requests

from util import parse_json_resp, insert_dead_coin, insert_candles


class NMSpider(object):
    def __init__(self):
        self.api_list = []

        self.dead_coin_list = []
        self.headers = {}

        self.candles_url = 'https://nomics.com/data/currency-candles'
        self.ticker_url = 'https://nomics.com/data/currencies-ticker'
        self.historical_url = 'https://nomics.com/data/currency-history'

    def get_api(self):
        with open("swagger.json", "r") as json_file:
            json_dict = json.load(json_file)
            # print(json_dict.get("paths"))
            paths = json_dict.get("paths").keys()
        print(f'共获取{len(paths)}个api')
        self.api_list = [f'https://api.nomics.com/v1{key}' for key in paths]
        print(self.api_list)

    '''
    API接口文档中components下parameters会标记参数是否必需("required": true)
    如果paths中转发了参数，如：
    {
            "$ref": "#/components/parameters/page"
    }
    则需查看components下parameters中参数page的required的状态(true or false)
    '''

    # 测试api接口
    def test_res(self):
        url = 'https://api.nomics.com/v1/currencies/ticker'
        file_name = url.split('/')[-2] + '_' + url.split('/')[-1]
        # file_name = url.split('v1/')[1]
        params = {
            'key': '3ed91352276a5939da4a1bd718e08f471ec6961b',
            'interval': '1d'
        }
        res = requests.get(url=url, params=params)
        print(res)
        pp(json.loads(res.text))
        with open(f"{file_name}.json", "w") as json_file:
            json_file.write(res.text)

    def get_dead_coin(self):
        ticker_detail_params = {
            'filter': 'any',
            'interval': '1d',
            'quote-currency': 'USD',
            'symbols': 'VEN'
        }
        ticker_all_params = {
            'include-transparency': 'true',
            'interval': '1d',
            'quote-currency': 'USD',
            'labels': 2,  # 2为dead
            'limit': 100,  # 只能为100
            'start': 0,
        }
        res_temp = parse_json_resp(url=self.ticker_url, params=ticker_all_params)
        items_total = res_temp.get("items_total")
        print(f"there are {items_total} dead coins need to be done!")
        # self.dead_coin_list.extend(res_temp.get("items"))
        # t = 0

        for t in range(0, items_total + 1, 100):
            # for t in range(0, 200, 100):
            print("\rloading...{}%".format(round(t * 100 / items_total, 2)), end="", flush=True)
            # t += 100
            ticker_all_params["start"] = t
            result = parse_json_resp(url=self.ticker_url, params=ticker_all_params)
            self.dead_coin_list.extend(result.get("items"))

        print(f"\nthere are total {len(self.dead_coin_list)} dead coins, inserting into database...")

        data_list = []
        # 处理获取的字典列表
        for item in self.dead_coin_list:
            name_id = item.get("id")
            currency = item.get("currency")
            symbol = item.get("symbol")
            name = item.get("name")
            status = item.get("status")
            platform_currency = item.get("platform_currency")
            price = item.get("price")
            price_date = item.get("price_date")
            price_timestamp = item.get("price_timestamp")
            circulating_supply = item.get("circulating_supply")
            max_supply = item.get("max_supply")
            market_cap = item.get("market_cap")
            num_exchanges = item.get("num_exchanges")
            num_pairs = item.get("num_pairs")
            num_pairs_unmapped = item.get("num_pairs_unmapped")
            first_candle = item.get("first_candle")
            first_trade = item.get("first_trade")
            first_order_book = item.get("first_order_book")
            first_priced_at = item.get("first_priced_at")
            high = item.get("high")
            high_timestamp = item.get("high_timestamp")
            tup = (name_id, currency, symbol, name, status, platform_currency, price, price_date, price_timestamp,
                   circulating_supply, max_supply, market_cap, num_exchanges, num_pairs, num_pairs_unmapped,
                   first_candle, first_trade, first_order_book, first_priced_at, high, high_timestamp)

            data_list.append(tup)

        # 数据入库
        insert_dead_coin(data_list)

    def parse_dead_coin(self):
        # 这里的返回应该只是已获得数据的单个数据
        ticker_detail_params = {
            'filter': 'any',
            'interval': '1d',
            'quote-currency': 'USD',
            'symbols': 'VEN'
        }
        res_temp = parse_json_resp(url=self.ticker_url, params=ticker_detail_params)
        print(res_temp)

    def parse_historical(self):
        name_id = 'HUSD2'
        historical_params = {
            'base': name_id,
            'convert': 'USD',
            'limit': 100,
            'start': 0
        }
        res_1st = parse_json_resp(url=self.historical_url, params=historical_params)
        # print(res_1st)
        # print(f"length of response:{len(res_1st.get('items'))}")
        # 获取历史数据总条数
        items_total = res_1st.get('items_total')
        if items_total <= 100:
            historical_data = res_1st.get("items")
        else:
            historical_params["limit"] = items_total
            # 再次请求得到所有数据
            res_2nd = parse_json_resp(url=self.historical_url, params=historical_params)
            historical_data = res_2nd.get("items")
        print(f"length of request response:{len(historical_data)}")
        insert_historical_data = []
        # 解析为入库数据
        for item in historical_data:
            timestamp = item.get("timestamp")
            open_ = item.get("open")
            high = item.get("high")
            low = item.get("low")
            close = item.get("close")
            volume = item.get("volume")
            transparent_open = item.get("transparent_open")
            transparent_high = item.get("transparent_high")
            transparent_low = item.get("transparent_low")
            transparent_close = item.get("transparent_close")
            transparent_volume = item.get("transparent_volume")
            volume_transparency = json.dumps(item.get("volume_transparency"))
            data = (
                name_id, timestamp, open_, high, low, close, volume, transparent_open, transparent_high,
                transparent_low,
                transparent_close, transparent_volume, volume_transparency)
            insert_historical_data.append(data)

        # 数据入库
        insert_candles(insert_historical_data)


if __name__ == '__main__':
    # NMSpider().get_dead_coin()
    # NMSpider().parse_deadcoin()
    # NMSpider().parse_candles()
    NMSpider().parse_historical()
