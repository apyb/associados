FROM python:2.7
ENV PYTHONUNBUFFERED 1
ADD . /code
WORKDIR /code
RUN ls -l .
RUN make deps
