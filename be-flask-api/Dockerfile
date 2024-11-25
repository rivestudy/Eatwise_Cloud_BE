
FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

ENV GOOGLE_APPLICATION_CREDENTIALS="/app/service-account-file.json"

EXPOSE 8080

CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]
