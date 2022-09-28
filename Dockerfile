# 基于镜像基础
FROM python:3.8
# 维护者信息
MAINTAINER name hwt
# 复制当前代码文件到容器中 /app
ADD . /app
# 设置app文件夹是工作目录 /app
WORKDIR /app
#修改为清华源
RUN pip install -r requirements.txt
# Run scheduler.py when the container launches
CMD ["python", "/app/fetcher/scheduler.py"]