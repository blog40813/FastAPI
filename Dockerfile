FROM python:3.10.1 as fastapi

RUN mkdir /fastapi

WORKDIR /fastapi

COPY ./requirement.txt .

RUN pip install --no-cache-dir -r ./requirement.txt

