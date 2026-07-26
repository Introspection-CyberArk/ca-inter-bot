FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for better caching
COPY deploy/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all source code
COPY src/ ./src/
COPY data/ ./data/

# Create data directory
RUN mkdir -p /app/data && chmod 755 /app/data

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV ENVIRONMENT=production

# Expose port (for webhook if needed)
EXPOSE 8443

# Run the bot
CMD ["python", "-u", "src/bot.py"]
