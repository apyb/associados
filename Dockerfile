FROM python:2.7

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements_test.txt /usr/src/app/
COPY requirements_test_osx.txt /usr/src/app/
COPY requirements.txt /usr/src/app/
RUN pip install -r requirements_test.txt
