FROM python:3.6.9

# Unbuffer Python logs
ENV PYTHONUNBUFFERED=1

COPY requirements_test.txt requirements.txt /tmp/
RUN pip install --upgrade pip && pip install -r /tmp/requirements_test.txt

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
