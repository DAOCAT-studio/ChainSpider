import json
import random
import threading
import time

import requests

import settings
from util import get_logger, db_handle, db_ori_set, db_trace, db_get_429, record_api, refresh_date

API_KEY_LIST = settings.API_KEY_LIST


class Spider(object):
    def __init__(self):
        self.params = {
            'i': '24h',
            'api_key': random.choice(API_KEY_LIST)
        }
        self.api_list = []

    def get_api_url(self):
        try:
            url = "https://api.glassnode.com/v2/metrics/endpoints"
            params = {
                'api_key': random.choice(API_KEY_LIST)
            }
            res = requests.get(url, params=params)
            result_list = json.loads(res.text)

            # 将获取到的api信息入库记录
            record_api(result_list)

            for item in result_list:
                tier = item.get("tier")
                if tier != 3:
                    api = 'https://api.glassnode.com{}'.format(item.get("path"))
                    assets = item.get("assets")
                    for asset in assets:
                        symbol = asset.get("symbol")
                        api_dict = {"api": api, "symbol": symbol}
                        self.api_list.append(api_dict)

        except Exception as e:
            logger.error(e)

    # 一个api_key开一个线程
    def get_data(self, api_list, api_key):
        for info in api_list:
            try:
                api = info.get("api")
                symbol = info.get("symbol")
                self.params['api_key'] = api_key
                self.params['a'] = symbol
                print("getting {} with symbol {}...".format(api, symbol))
                r = requests.get(url=api, params=self.params)
                # 将其他url存入追踪表
                db_trace(api, symbol, api_key, r.status_code)

                if r.status_code == 200:
                    result_list = json.loads(r.text)
                    # print(result_list)

                    if result_list:
                        db_handle(api, symbol, result_list)

                time.sleep(random.uniform(0.1, 1))
            except Exception as e:
                logger.error("api info:{};e:{}".format(json.dumps(info), e))

    # 重新获取返回429的api
    def check_429(self):
        res = db_get_429()
        while res:
            # logger.info("there are {} api response 429 with symbol {} left, requesting...".format(len(res), symbol))
            print("there are {} api response 429 left, requesting...".format(len(res)))
            api_list = [{"api": i[0], "symbol": i[1]} for i in res]
            # print(api_url_list)
            self.handle_api(api_list)
            res = db_get_429()

    def handle_api(self, api_list):
        threads = []
        # 线程数
        n = len(API_KEY_LIST)
        # 需处理的url数量
        total = len(api_list)
        if total >= n:
            if total % n == 0:
                cnt = total // n
            else:
                cnt = total // n + 1
        else:
            cnt = 1
        # 遍历key列表，将均分的任务列表交给每个线程
        for i, key in enumerate(API_KEY_LIST):
            threads.append(
                threading.Thread(target=self.get_data, args=(api_list[i * cnt:(i + 1) * cnt], key)))

        for i in threads:
            i.start()
        for j in threads:
            j.join()

    def run_main(self):
        print('初始化追踪表状态...')
        db_ori_set()

        print('获取所有api中...')
        self.get_api_url()
        logger.info(
            "共需请求{}次api".format(len(self.api_list)))
        time.sleep(1)
        # 数据获取主函数
        print('获取数据中...')
        self.handle_api(self.api_list)
        self.check_429()
        refresh_date()


if __name__ == '__main__':
    logger = get_logger("glassnode.log")
    Spider().run_main()
