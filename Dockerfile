FROM python:3.9.18-slim

RUN --mount=type=cache,target=/var/cache/apt \
    apt-get update && apt-get install -y git git-lfs

WORKDIR /usr/src/app

COPY release-requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r release-requirements.txt

COPY . .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install .

ENTRYPOINT [ "github-backup" ]
