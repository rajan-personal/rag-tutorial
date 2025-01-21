# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Create cache directory for Hugging Face
RUN mkdir -p /root/.cache/huggingface

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all step files and the test sample directory
COPY step_*.py .
COPY Test_Sample ./Test_Sample/
COPY run_steps.sh .

# Make the shell script executable
RUN chmod +x run_steps.sh

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV HF_HOME=/root/.cache/huggingface

# Run all steps using the shell script
CMD ["./run_steps.sh"]
