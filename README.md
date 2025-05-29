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

# (Opcional) Solicitud Service
docker build -t solicitud-service:latest ./solicitud_service
```

---

## 3. Despliegue de los Microservicios en Minikube
```sh
kubectl apply -f [academic-service.yml](http://_vscodecontentref_/0)
kubectl apply -f [certification-service.yml](http://_vscodecontentref_/1)
kubectl apply -f [security-service.yml](http://_vscodecontentref_/2)
kubectl apply -f proxi/solicitud-service.yml

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

## 5.1 Acceso a los Servicios vía Istio Ingress
Por defecto Istio expone en el IngressGateway los puertos 80 y 443. Con Minikube mapeaste 8080→80:
```sh
# Obtén la IP del IngressGateway:
INGRESS_IP=$(kubectl -n istio-system get svc istio-ingressgateway -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
echo "http://$INGRESS_IP:80/academico/1"
echo "http://$INGRESS_IP:80/auth/token"
echo "http://$INGRESS_IP:80/certification"
echo "http://$INGRESS_IP:80/solicitudes"

```


---

## 6. Integración con WSO2 API Manager
1. Instala WSO2 API Manager siguiendo la documentación oficial.
2. Ingresa al Publisher (https://localhost:9443/publisher).
3. Crea una nueva API REST apuntando a los endpoints expuestos por Minikube (las URLs que te da minikube service ...).
4. Publica la API y suscríbete desde el Developer Portal.
5. Prueba la API usando el token OAuth2 generado por el servicio de seguridad.

---

## 7. Pruebas Manuales
7.1 Academic Service
curl http://localhost:8080/academico/1

7.2 Security Service (Token)
curl -X POST http://localhost:8080/auth/token \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'username=alice&password=secret123'

7.3 Certification Service (SOAP)
curl -X POST http://localhost:8080/certification \
  -H 'Content-Type: text/xml; charset=utf-8' \
  -H 'SOAPAction: "registerCertification"' \
  -d '<?xml version="1.0" encoding="UTF-8"?>
      <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="tns">
        <soapenv:Header/>
        <soapenv:Body>
          <tns:registerCertification>
            <tns:student_id>123</tns:student_id>
            <tns:doc_type>ID_CARD</tns:doc_type>
          </tns:registerCertification>
        </soapenv:Body>
      </soapenv:Envelope>'

7.4 Solicitud Service
curl -X POST http://localhost:8080/solicitudes \
  -H 'Authorization: Bearer <token>' \
  -H 'Content-Type: application/json' \
  -d '{"studentId":123,"courseId":"FENIX-001","docType":"ID_CARD"}'


---

## 8. Monitoreo y Trazabilidad
- Prometheus + Grafana: métricas de Istio (RPS, errores, latencia)
- Jaeger: trazabilidad distribuida (headers B3 inyectados)
- Kiali: topología y estado del mesh

