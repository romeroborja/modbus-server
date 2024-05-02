# DEVELOPMENT
FROM python:3.12-slim as development-stage

COPY requirements.txt .
RUN pip3 install -r requirements.txt

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV ENV development

WORKDIR /app
COPY ./src /app

CMD ["python", "-m", "debugpy", "--listen", "0.0.0.0:5678", "main.py"]
