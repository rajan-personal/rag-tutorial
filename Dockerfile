# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Create cache directory for Hugging Face
RUN mkdir -p /root/.cache/huggingface

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY step_0_AI.py .
COPY Test_Sample ./Test_Sample/

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV HF_HOME=/root/.cache/huggingface

# Run the test script
CMD ["python", "step_0_AI.py"]
