FROM python:3.15.0rc1-slim

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Add Tini
# This avoids the healthcheck becoming zombie processes
# Ignoring DL3008 as we don't need to pin tini
# hadolint ignore=DL3008
RUN apt-get -y update &&  \
    apt-get install --no-install-recommends  \
    -y tini && \
    rm -rf /var/lib/apt/lists/*

RUN useradd -m python
USER python

# Install httpie for the healthcheck
RUN uv tool install httpie
HEALTHCHECK CMD uv tool run --from httpie http localhost:8080

# Copy the application into the container.
COPY --chown=python . /app

# Install the application dependencies.
WORKDIR /app
RUN uv sync --frozen --no-cache

EXPOSE 8080/tcp

# Run the application.
ENTRYPOINT ["tini", "--"]
CMD ["/app/.venv/bin/fastapi", "run", "--port", "8080", "--host", "0.0.0.0", "--forwarded-allow-ips=*"] 
