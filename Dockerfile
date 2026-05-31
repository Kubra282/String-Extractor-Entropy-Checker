
FROM python:3.10-slim


WORKDIR /app


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY src/ ./src/
COPY tests/ ./tests/
COPY .env.example .env


RUN mkdir -p /app/data


ENTRYPOINT ["python", "src/hydra_parser.py"]
