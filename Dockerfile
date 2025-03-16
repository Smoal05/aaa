FROM python:3.10

WORKDIR /app
COPY server.py server.py

RUN pip install websockets

CMD ["python", "server.py"]