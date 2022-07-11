import asyncio
import json
import random
import threading
import time
import traceback

import aiohttp
import requests
from lxml import etree

import settings
from util import get_logger, db_handle, db_ori_set, db_trace, db_get_429

API_KEY_LIST = settings.API_KEY_LIST


# symbol = settings.SYMBOL
# params = settings.PARAMS


class Spider(object):
    def __init__(self):
        self.group_url = []
        self.api_url = []

        self.params = {
            # 'a': self.symbol,
            'i': '24h',
            'api_key': random.choice(API_KEY_LIST)
        }

    def get_group_url(self):
        try:
            # url = 'https://docs.glassnode.com/api/addresses'
            url = 'https://docs.glassnode.com/basic-api/endpoints'
            r = requests.get(url=url)
            tree = etree.HTML(r.text)
            # result = tree.xpath('/html/body/div[1]/div/div/div[2]/div[1]/div/div[1]/div/div/div[5]/div[2]/div/a/@href')
            # result = tree.xpath('/html/body/div[1]/div/div/div[2]/div[1]/div/div[1]/div/div/div[4]/div[2]/div[5]/div/div/a/@href')
            result = tree.xpath(
                '/html/body/div[1]/div/div/div[2]/div[2]/div/div/div/div/div/div[2]/div[1]/div/div/div/div[2]/a/@href')
            # print(result)
            for i in result:
                # print(i)
                self.group_url.append('https://docs.glassnode.com{}'.format(i))
            print("共获取{}个页面".format(len(self.group_url)))
        except:
            print(traceback.format_exc())

    async def run_get_api(self, pool):
        sem = asyncio.Semaphore(pool)
        tasks = [self.control_sem_group(sem, i) for i in self.group_url]
        await asyncio.wait(tasks)

    async def control_sem_group(self, sem, group_url):  # 限制信号量
        async with sem:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=600),
                                             connector=aiohttp.TCPConnector(ssl=False, force_close=True),
                                             # trust_env=True
                                             ) as session:
                await self.get_api_url(group_url, session)

    async def get_api_url(self, group_url, session):
        try:
            async with session.get(url=group_url) as res:
                r = await res.text()
                tree = etree.HTML(r)
                result = tree.xpath(
                    '/html/body/div[1]/div/div/div[2]/div[2]/div/div/div/div/div/div[2]/div[1]/div[2]/div/div/div/div/div/div/div/div/div/div/div/div/div[1]/div[2]/div[2]/div')
                # print(result)
                for i in result:
                    # print(i.text)
                    self.api_url.append('https://api.glassnode.com{}'.format(i.text))
                await asyncio.sleep(1)
        except:
            print(traceback.format_exc())

    # 不同的key开不同的线程
    def get_data(self, api_url_li, api_key, symbol):
        try:
            for api_url in api_url_li:
                self.params['api_key'] = api_key
                print("getting api: ", api_url)
                r = requests.get(url=api_url, params=self.params)
                # 将其他url存入追踪表
                db_trace(api_url, symbol, api_key, r.status_code)

                if r.status_code == 200:
                    result_list = json.loads(r.text)
                    # print(result_list)

                    if result_list:
                        db_handle(api_url, symbol, result_list)

                time.sleep(1)
        except Exception as e:
            print(traceback.format_exc())
            logger.error(e)

    # 重新获取返回429的api
    def check_429(self, symbol):
        res = db_get_429(symbol)
        while res:
            logger.info("there are {} api response 429 with symbol {} left, requesting...".format(len(res), symbol))
            api_url_list = [i[0] for i in res]
            # print(api_url_list)
            self.handle_api(api_url_list, symbol)
            res = db_get_429(symbol)
        logger.info("done!bye!")

    def handle_api(self, api_url_list, symbol):
        threads = []
        # 线程数
        n = len(API_KEY_LIST)
        # 需处理的url数量
        total = len(api_url_list)
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
                threading.Thread(target=self.get_data, args=(api_url_list[i * cnt:(i + 1) * cnt], key, symbol)))

        for i in threads:
            i.start()
            i.join()

    def run_main(self):
        print('初始化追踪表状态...')
        db_ori_set()
        print('获取页面url中...')
        self.get_group_url()
        print('获取所有api中...')
        # asyncio.run(self.run_get_api(pool=30))
        loop1 = asyncio.get_event_loop()
        loop1.run_until_complete(self.run_get_api(pool=20))
        logger.info(
            "共获取{}个api".format(len(self.api_url)))
        time.sleep(1)
        # 数据获取主函数
        print('获取数据中...')
        for symbol in settings.SYMBOL_LIST:
            # Spider(symbol).run_main()
            self.handle_api(self.api_url, symbol)
            # 补充请求返回429状态的api
            self.check_429(symbol)


if __name__ == '__main__':
    logger = get_logger("glassnode.log")
    Spider().run_main()
