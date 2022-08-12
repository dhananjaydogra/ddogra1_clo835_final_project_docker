FROM python:alpine

ADD ./requirements.txt /opt/webapp-mysql/

WORKDIR /opt/webapp-mysql

RUN pip install -r requirements.txt

ADD . /opt/webapp-mysql

EXPOSE 81

RUN aws s3 cp s3://ddogra1-test/ /opt/webapp-mysql/static --recursive

CMD python /opt/webapp-mysql/app.py
