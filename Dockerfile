# Estágio 1: Builder - Instala dependências de build
FROM python:3.10-slim AS builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    make \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY _core/pyproject.toml /app/_core/
RUN mkdir -p /app/_core/sdd_cli && \
    touch /app/_core/sdd_cli/__init__.py && \
    touch /app/_core/README.md

# Instala dependências em um prefixo separado
RUN pip install --no-cache-dir --prefix=/install "/app/_core[dev]"

# Estágio de Segurança: Análise de vulnerabilidades (Trivy)
FROM builder AS security-scan
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates && \
    curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh -s -- -b /usr/local/bin && \
    rm -rf /var/lib/apt/lists/*
RUN trivy filesystem --exit-code 1 --severity HIGH,CRITICAL --no-progress /app

# Estágio 2: Runtime - Imagem final leve
FROM python:3.10-slim

# Mantemos apenas o 'make' para orquestração; 'git' é removido por ser apenas build-time
RUN apt-get update && apt-get install -y --no-install-recommends \
    make \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copia apenas as bibliotecas instaladas e o código fonte
COPY --from=builder /install /usr/local
COPY . /app

RUN pip install --no-cache-dir --no-deps -e "./_core[dev]"

CMD ["make", "check"]