FROM python:3.9-slim

# Nainstalujeme FastAPI a Uvicorn
RUN pip install fastapi uvicorn python-multipart

# Vložíme kód aplikace
WORKDIR /app
COPY main.py main.py

# Exponujeme port pro Uvicorn (interně třeba 8000)
EXPOSE 8000

# Spuštění serveru
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
