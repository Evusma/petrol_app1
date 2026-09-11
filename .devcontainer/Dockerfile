# Base image
FROM mcr.microsoft.com/devcontainers/python:1-3.11-bookworm

# Working directory
WORKDIR /workspace

# Dependency
COPY pyproject.toml .
COPY src/ ./src/

# Install dev dependencies
# RUN pip install --upgrade pip && pip install -e ".[dev]"
RUN pip install --upgrade pip && \
    pip install -e ".[dev]"

# Expose Streamlit default port
EXPOSE 8501
