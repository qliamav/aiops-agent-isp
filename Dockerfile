FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

FROM base AS builder

RUN apt-get update && apt-get install -y --no-install-recommends build-essential && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml requirements.txt ./

RUN pip install --upgrade pip && \
    pip install --prefix=/install -r requirements.txt

FROM base AS runtime

COPY --from=builder /install /usr/local

COPY app ./app
COPY .env.example ./.env.example

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
