FROM python:3.10.12-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD python rps.py

EXPOSE 5000

