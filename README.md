# Plataforma de Servicios Estudiantiles

Este proyecto contiene tres microservicios: **academic_service**, **certification_service** y **security_service**. Cada uno se ejecuta en un contenedor Docker y puede desplegarse en un clúster Kubernetes (Minikube). Además, se puede integrar con WSO2 API Manager para la gestión de APIs.

---

## Requisitos Previos

- Docker
- Kind o Minikube
- kubectl
- Python 3.12
- WSO2 API Manager

---

## 1. Configuración del entorno Docker en Minikube

Antes de construir las imágenes, configura tu terminal para usar el Docker interno de Minikube:

```sh
eval $(minikube docker-env)
```

---

## 2. Construcción de Imágenes Docker
Desde la raíz del proyecto, ejecuta:

```sh
# Academic Service
docker build -t academic-service:latest ./academic_service

# Certification Service
docker build -t certification-service:latest ./certification_service

# Security Service
docker build -t security-service:latest ./security_service
```

---

## 3. Despliegue de los Microservicios en Minikube
```sh
kubectl apply -f [academic-service.yml](http://_vscodecontentref_/0)
kubectl apply -f [certification-service.yml](http://_vscodecontentref_/1)
kubectl apply -f [security-service.yml](http://_vscodecontentref_/2)
```
Verifica que los pods y servicios estén corriendo:
```sh
kubectl get pods
kubectl get svc
```

---

## 4. Exposición de Servicios
Para acceder a los servicios desde tu navegador o herramientas externas, usa:
```sh
minikube service academic-service
minikube service certification-service
minikube service security-service
```

Esto abrirá una URL local para cada servicio.

---

## 5. Pruebas Locales
```sh
# Academic Service
cd academic_service
uvicorn main:app --host 0.0.0.0 --port 8001

# Certification Service
cd certification_service
python main.py

# Security Service
cd security_service
uvicorn main:app --host 0.0.0.0 --port 8003
```

---

## 6. Integración con WSO2 API Manager
1. Instala WSO2 API Manager siguiendo la documentación oficial.
2. Ingresa al Publisher (https://localhost:9443/publisher).
3. Crea una nueva API REST apuntando a los endpoints expuestos por Minikube (las URLs que te da minikube service ...).
4. Publica la API y suscríbete desde el Developer Portal.
5. Prueba la API usando el token OAuth2 generado por el servicio de seguridad.

