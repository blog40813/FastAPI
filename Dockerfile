FROM python:3.10.1 as fastapi

WORKDIR /fastapi

COPY ./requirement.txt .

RUN pip install --no-cache-dir -r ./requirement.txt

RUN mkdir /fastapi/application

RUN mkdir /fastapi/prefect

WORKDIR /fastapi

