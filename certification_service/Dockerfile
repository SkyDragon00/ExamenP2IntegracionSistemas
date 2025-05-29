FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# El servicio SOAP normalmente arranca con WSGI dentro de main.py
EXPOSE 8002
# Si en main.py usas wsgiref.simple_server o similar:
CMD ["python", "main.py"]
# — o si prefieres usar gunicorn:
# CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:8002", "main:app"]