# ChainSpider

```

  ______ _           _             _          _     _             
 / _____) |         (_)           | |        (_)   | |            
| /     | | _   ____ _ ____        \ \  ____  _  _ | | ____  ____ 
| |     | || \ / _  | |  _ \        \ \|  _ \| |/ || |/ _  )/ ___)
| \_____| | | ( ( | | | | | |   _____) ) | | | ( (_| ( (/ /| |    
 \______)_| |_|\_||_|_|_| |_|  (______/| ||_/|_|\____|\____)_|    
                                       |_|                        

```
## 项目概述
本项目用以获取指定数据源提供的api返回数据。  
目前的数据源有：  
- [glassnode](https://docs.glassnode.com/)
- [nomics](https://nomics.com/)

## 运行环境
- python 3.8  
- docker
- ubuntu
- mysql 3.5.18
- anaconda

## 数据结构说明
### GLASSNODE
`1.` 数据库api_data,内含数据表glassnode、追踪表state_trace、api记录表endpoints；  
`2.`以24h为时间单位获取数据并入mysql数据库，每个api的返回数据在glassnode中以**api+返回数据字段名**的形式表示，
例如，**https://api.glassnode.com/v1/metrics/addresses/sending_to_exchanges_count** 的返回数据在表glassnode内的字段是**addresses_sending_to_exchanges_count_v**；  
`3.`glassnode表中的数据以**t+symbol**（如：1615075200_BTC）为唯一索引来插入或更新数据；

### NOMICS
`1.` 数据库api_data,内含数据总览表表tickers、详细数据candles；  
`2.` 数据字段以api返回的数据字段为准；  

## 准备工作
- 创建mysql数据库及对应表
- 添加fetcher文件夹下配置文件config.ini，格式如：
```
[server]
HOST = xxx.xxx.xxx.xxx
PORT = xxxx
USER = xxx
PASSWD = xxx

[local]
...
```

## 使用步骤
（省略建表及拉取docker镜像步骤）  
```shell
git clone https://github.com/DAOCAT-studio/ChainSpider.git  
cd ./ChainSpider
```
`1.`使用docker
```shell
docker build -t chain .  
docker run chain
```
`2.`使用conda
```shell
conda create -n chain python=3.8
conda activate chain
pip install -r requirements.txt

# glassnode爬虫启动
python fetcher/glassnode.py 
#或者 python fetcher/start.py glassnode

# nomics爬虫启动
python fetcher/nomics.py 
#或者 python fetcher/start.py nomics
```
ps.其中nomics的数据获取可以不用更新总览表tickers，直接运行***nomics.py***即可

## 后续完善
- 优化脚本逻辑，提高效率；
- 添加更多数据；