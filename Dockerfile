FROM python:3.10.1

WORKDIR /fastapi

COPY ./requirement.txt .

RUN pip install --no-cache-dir -r ./requirement.txt

WORKDIR /fastapi/application

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
