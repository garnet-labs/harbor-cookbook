FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends auditd python3 curl ca-certificates procps coreutils && rm -rf /var/lib/apt/lists/*
RUN useradd -m runner && mkdir -p /app /tests && chown runner:runner /app /tests
WORKDIR /app
