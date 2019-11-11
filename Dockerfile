FROM python:3.6.9

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements_test.txt /usr/src/app/
COPY requirements_test_osx.txt /usr/src/app/
COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements_test.txt
