FROM python:3.8.13

RUN sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list

RUN apt-get update && apt-get -y install openssh-server vim apt-utils && rm -rf /var/lib/apt/lists/*


WORKDIR /usr/src/app
ENV PYTHONPATH /usr/src/app


COPY requirements.txt /usr/src/app/requirements.txt

RUN pip3 install --upgrade pip -i https://pypi.douban.com/simple
RUN pip3 install -i https://pypi.douban.com/simple -r requirements.txt

COPY . /usr/src/app

EXPOSE 8001
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo '$TZ' > /etc/timezone && rm -rf /root/.cache/pip

CMD ["python3", "/usr/src/main.py"]
