FROM python:3.10.1 as fastapi

WORKDIR /fastapi

COPY ./requirement.txt .

RUN pip install --no-cache-dir -r ./requirement.txt

RUN mkdir /fastapi/prefect

WORKDIR /fastapi/application

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000","--reload"]
