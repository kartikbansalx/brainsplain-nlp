FROM python:3.11-slim

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m spacy download en_core_web_sm

COPY backend/ .

# Keep ChromaDB data in a separately mountable directory.
ENV CHROMA_DB_PATH=/data/chroma_db
ENV OMP_NUM_THREADS=1
ENV MKL_NUM_THREADS=1
RUN mkdir -p /data/chroma_db

# Export once at image-build time; app startup loads the saved ONNX model.
RUN python export_onnx.py

EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "--workers", "1", "--timeout", "120", "app:app"]
