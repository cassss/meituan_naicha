FROM python:3.6

MAINTAINER Xiaoshao <ikkcass@hotmail.com>

ADD ./requirements.txt /var/www/app/requirements.txt 
WORKDIR /var/www/app
RUN pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade pip 
RUN pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

CMD ["python", "QueWork.py"]