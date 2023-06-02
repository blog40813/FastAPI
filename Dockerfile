FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

WORKDIR /code

COPY ./application /code/app
COPY ./sta /code/sta
COPY ./requirement.txt /code/requirement.txt

RUN pip install --no-cache-dir -r ./requirement.txt

CMD ["uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000"]