# 1. Partimos de una imagen oficial y ligera
FROM python:3.12-slim

# 2. Directorio de trabajo dentro del contenedor
WORKDIR /app

# 3. Copiamos sólo requirements para aprovechar cache de Docker
COPY requirements.txt .

# 4. Instalamos dependencias sin cache
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiamos el resto del código
COPY . .

# 6. Exponemos el puerto que usa academic_service (FastAPI)
EXPOSE 8001

# 7. Comando por defecto: lanzamos uvicorn apuntando a main:app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]