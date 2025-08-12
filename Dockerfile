FROM python:3.12-alpine3.22 AS builder

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir uv

WORKDIR /app

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    --mount=type=bind,source=release-requirements.txt,target=release-requirements.txt \
    uv venv \
    && uv pip install -r release-requirements.txt

COPY . .

RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install .


FROM python:3.12-alpine3.22
ENV PYTHONUNBUFFERED=1

RUN apk add --no-cache \
    ca-certificates \
    git \
    git-lfs \
    && addgroup -g 1000 appuser \
    && adduser -D -u 1000 -G appuser appuser

COPY --from=builder --chown=appuser:appuser /app /app

WORKDIR /app

USER appuser

ENV PATH="/app/.venv/bin:$PATH"

ENTRYPOINT ["github-backup"]
