from kafka import KafkaProducer
import json
import time
from datetime import datetime

# Configuracion Kafka
bootstrap_servers = 'localhost:9092'  # Broker address

# Crear producer
producer = KafkaProducer(bootstrap_servers=bootstrap_servers,
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))


# Enviar JSON
def send_inscripcion(nombre, email, msg, paid):
    topic = 'inscripciones'
    mensaje = {
        "timestamp": datetime.now().isoformat(),
        "nombre": nombre,
        "email": email,
        "mensaje": msg,
        "paid": paid
    }

    partition = 0 if paid else 1

    producer.send(topic=topic, value=mensaje, partition=partition)
    print(f"Enviando mensaje: {mensaje}")
    time.sleep(2)


def send_venta(maestro_id, monto):
    topic = 'ventas'
    mensaje = {
        "maestro_id": maestro_id,
        "monto": monto
    }

    producer.send(topic, value=mensaje)
    print(f"Enviando mensaje: {mensaje}")
    time.sleep(2)


def send_ingrediente(maestro_id):
    topic = 'ingredientes'
    mensaje = {
        "maestro_id": maestro_id
    }

    producer.send(topic, value=mensaje)
    time.sleep(2)


# Cerrar producer
producer.close()
