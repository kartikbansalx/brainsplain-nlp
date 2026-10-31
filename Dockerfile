# Use the official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy dependencies
COPY backend/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m spacy download en_core_web_sm

# Copy the backend code and static files
COPY backend/ .

# Keep the vector database outside the application code directory so it can be mounted.
ENV CHROMA_DB_PATH=/data/chroma_db
RUN mkdir -p /data/chroma_db

# Expose port
EXPOSE 5000

# Run the application with gunicorn for production
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
