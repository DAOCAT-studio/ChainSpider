# ChainSpider
（项目地址是@bacar写错的）
## 项目概述
本项目用以获取指定数据源提供的api返回数据。  
目前的数据源有：  
- [glassnode](https://docs.glassnode.com/api/addresses)

## 运行环境
- python 3.8  
- docker
- ubuntu
- mysql 3.5.18

## 数据结构说明
`1.` 数据库api_data,内含数据表glassnode、追踪表state_trace；  
`2.`
以24h为单位获取数据并入mysql数据库，每个api的返回数据在glassnode中以**api+返回数据字段名**的形式表示，  
例如，**https://api.glassnode.com/v1/metrics/addresses/sending_to_exchanges_count** 的返回数据在mysql内的字段是**addresses_sending_to_exchanges_count_v**；  
  
## 使用步骤
（省略建表及拉取docker镜像步骤）
```
git clone https://github.com/DAOCAT-studio/ChianSpider.git  
cd ./ChianSpider
docker build -t chain .  
docker run chain
```

## 后续完善
- 切换symbol，获取所有数据并入库；
- 将每日最新数据入库，无需旧数据；