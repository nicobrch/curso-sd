from kafka import KafkaConsumer
import json
from db import insert_maestro, insert_reposicion, insert_venta

# Configuracion Broker Kafka
bootstrap_servers = 'localhost:9092'  # Broker address
topics = ['inscripciones', 'ingredientes']

# Crear consumer
consumer = KafkaConsumer(
    *topics,
    bootstrap_servers=bootstrap_servers,
    value_deserializer=json.loads
)


# Procesar mensajes
def process_inscripcion(message):
    nombre = message.value.get('nombre')
    email = message.value.get('email')

    if nombre is not None and email is not None:
        # Insertar a la BDD
        maestro = insert_maestro(nombre, email)
        if maestro:
            print(f"Solicitud aprobada y agregada a la BDD. Maestro ID: {maestro.id}, Nombre: {maestro.nombre}")
        else:
            print("Error al insertar a la BDD.")
    else:
        print("Solicitud de inscripción no tiene nombre o email.")


def process_ingrediente(message):
    maestro_id = message.value.get('maestro_id')

    if maestro_id is not None:
        # Insertar a la BDD
        reposicion = insert_reposicion(maestro_id=maestro_id, stock=10)
        if reposicion:
            print(f"Solicitud aprobada y agregada a la BDD. Stock Repuesto: {reposicion.stock}")
        else:
            print("Error al insertar a la BDD.")
    else:
        print("Solicitud de reposición no tiene ID Maestro.")


def process_venta(message):
    maestro_id = message.value.get('maestro_id')
    monto = message.value.get('monto')

    if maestro_id is not None and monto is not None:
        # Insertar a la BDD
        venta = insert_venta(maestro_id=maestro_id, monto=monto)
        if venta:
            print(f"Venta aprobada y agregada a la BDD. Monto agregado: {venta.monto}")
        else:
            print("Error al insertar a la BDD.")
    else:
        print("Solicitud de venta no tiene ID Maestro o Monto.")


# Consumir mensajes
for msg in consumer:
    print(f"Solicitud recibida de topico {msg.topic}: {msg.value}")

    if msg.topic == topics[0]:
        process_inscripcion(msg)
    elif msg.topic == topics[1]:
        process_ingrediente(msg)
