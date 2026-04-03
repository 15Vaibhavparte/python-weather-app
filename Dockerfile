# ---- Stage 1: Build ----
FROM python:3.10-slim AS builder
WORKDIR /build

# Copy requirements and install to a local user directory
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# ---- Stage 2: Final Image ----
FROM python:3.10-slim
WORKDIR /app

# Create a non-root user for security
RUN useradd -m appuser
USER appuser

# Copy installed dependencies from the builder stage
COPY --from=builder /root/.local /home/appuser/.local

# Copy application code
COPY ./app ./app

# Add local bin to PATH
ENV PATH=/home/appuser/.local/bin:$PATH

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]