FROM python:3.10.1

WORKDIR /exercise

COPY ./requirement.txt .

RUN pip install --no-cache-dir -r ./requirement.txt

WORKDIR /exercise/application

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]