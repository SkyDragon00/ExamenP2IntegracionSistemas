from spyne import Application, rpc, ServiceBase, Integer, Unicode
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication

class CertService(ServiceBase):
    @rpc(Integer, Unicode, _returns=Unicode)
    def registerCertification(ctx, student_id, doc_type):
        # Simulación de registro
        return f"Certificación registrada: estudiante={student_id}, tipo={doc_type}"

soap_app = Application(
    [CertService],
    tns="tns",
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

if __name__ == "__main__":
    from wsgiref.simple_server import make_server
    server = make_server("0.0.0.0", 8002, WsgiApplication(soap_app))
    print("SOAP Service en http://0.0.0.0:8002")
    server.serve_forever()
