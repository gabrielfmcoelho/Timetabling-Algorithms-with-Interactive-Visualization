FROM python:3.12-slim

WORKDIR /app

COPY api/requirements.txt requirements.txt
RUN pip install -r requirements.txt

RUN echo pwd && ls -la
COPY .env /app
COPY api/src /app
RUN echo pwd && ls -la

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "(API_PORT)"]