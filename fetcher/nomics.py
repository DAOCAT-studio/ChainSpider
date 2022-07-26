import json
from pprint import pprint as pp

import requests

from util import parse_json_resp


class Spider(object):
    def __init__(self):
        self.api_list = []

        self.dead_coin_list = []
        self.headers = {}

        self.candles_url = 'https://nomics.com/data/currency-candles'
        self.ticker_url = 'https://nomics.com/data/currencies-ticker'

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
        print(f"应有{items_total}个dead coin需收集")
        self.dead_coin_list.extend(res_temp.get("items"))
        t = 0

        while t <= items_total:
            t += 100
            print("\r完成进度{0}%".format(t * 100 / items_total), end="", flush=True)
            # print(f"本次循环t的值为：{t}")
            ticker_all_params["start"] = t
            result = parse_json_resp(url=self.ticker_url, params=ticker_all_params)
            self.dead_coin_list.extend(result.get("items"))
            # 如使用代理则不需延时
            # time.sleep(random.uniform(1, 3))
        print("-------------------all done!-------------------")
        print(self.dead_coin_list)
        # with open('deadcoin.json', 'w', encoding='utf-8') as f:
        #     f.write(str(self.dead_coin_list))
        print(f"共计获取{len(self.dead_coin_list)}个dead coin")

    def parse_dead_coin(self):
        ticker_detail_params = {
            'filter': 'any',
            'interval': '1d',
            'quote-currency': 'USD',
            'symbols': 'VEN'
        }
        res_temp = parse_json_resp(url=self.ticker_url, params=ticker_detail_params)
        print(res_temp)

    def parse_dead_coin_v2(self):
        candles_params = {
            'bars': 320,
            'convert': 'USD',
            'from': '2017-10-12T00:00:00.000Z',
            'id': 'VEN',
            'resolution': '1D',
            'to': '2018-08-28T00:00:01.000Z'
        }
        res_temp = parse_json_resp(url=self.candles_url, params=candles_params)
        print(res_temp)


if __name__ == '__main__':
    Spider().get_dead_coin()
    # Spider().parse_deadcoin()
    # Spider().parse_dead_coin_v2()
