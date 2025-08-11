FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY run.py .

EXPOSE 5000

# Gunicorn是一个unix上被广泛使用的高性能的Python WSGI UNIX HTTP Server。和大多数的web框架兼容，并具有实现简单，轻量级，高性能等特点
# "run:app"： run代表的是我的python脚本名字是run.py
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "run:app"]
