FROM python:3.10-alpine

ENV PATH="/app/venv/bin:$PATH"
WORKDIR /app
COPY pyproject.toml poetry.lock ./

RUN apk update
RUN apk update && \
    apk add --no-cache \
        curl \
        unixodbc-dev \
        gcc \
        g++ \
        vim \
        sudo \
        bash \
        libffi-dev \
        libpq \
        libpq-dev \
        gnupg \
        openssl

RUN pip install "poetry==1.2.2" "psycopg[binary]" && poetry install --no-cache

COPY . .
CMD ["poetry", "run", "python3", "-m", "telegram_bot_zoo", "start-encollector"]
