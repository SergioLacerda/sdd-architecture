# Stage 1: Builder
FROM python:3.12-slim AS builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    make \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app

# Install workspace root dev dependencies + package set in explicit order.
RUN pip install --no-cache-dir --prefix=/install -e "/app[dev]" && \
    pip install --no-cache-dir --prefix=/install -e /app/packages/core/sdd_core && \
    pip install --no-cache-dir --prefix=/install -e /app/packages/core/sdd_compiler && \
    pip install --no-cache-dir --prefix=/install -e /app/packages/features/sdd_integration && \
    pip install --no-cache-dir --prefix=/install -e /app/packages/interfaces/sdd_wizard && \
    pip install --no-cache-dir --prefix=/install -e /app/packages/interfaces/sdd_cli

# Stage 2: Runtime
FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    make \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY --from=builder /install /usr/local
COPY . /app

CMD ["make", "check"]
