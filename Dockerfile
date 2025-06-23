FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./src ./src
COPY ./main.py .
COPY ./confing.py .
COPY ./.env .


CMD ["python3", "main.py"]