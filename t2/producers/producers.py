from kafka import KafkaProducer
from json import dumps
import time
import random
from datetime import datetime
from db import get_maestro_stock, get_maestro_by_email

# Configuracion Kafka
bootstrap_servers = 'kafka:9092'  # Broker address

# Crear producer
producer = KafkaProducer(
    bootstrap_servers=[bootstrap_servers],
    value_serializer=lambda x: dumps(x).encode('utf-8')
)


# Enviar JSON
def send_inscripcion(nombre, email, paid):
    topic = 'inscripciones'
    mensaje = {
        "timestamp": datetime.now().isoformat(),
        "nombre": nombre,
        "email": email,
        "paid": paid
    }

    producer.send(topic=topic, value=mensaje)
    print(f"Enviando mensaje: {mensaje} al topic {topic}")
    time.sleep(2)


def send_venta(maestro_id):
    topic = 'ventas'
    while True:
        monto = random.randint(100, 500)
        stock = get_maestro_stock(maestro_id)

        if stock:
            mensaje = {
                "timestamp": datetime.now().isoformat(),
                "maestro_id": maestro_id,
                "monto": monto
            }

            producer.send(topic, value=mensaje)
            print(f"Enviando mensaje: {mensaje} al topic {topic}")
            delay = random.randint(4, 6)
            time.sleep(delay)
        else:
            send_ingrediente(maestro_id)
            time.sleep(2)


def send_ingrediente(maestro_id):
    topic = 'ingredientes'
    mensaje = {
        "timestamp": datetime.now().isoformat(),
        "maestro_id": maestro_id
    }

    producer.send(topic, value=mensaje)
    print(f"Enviando mensaje: {mensaje} al topic {topic}")
    time.sleep(2)


def send_contabilidad(maestro_id):
    topic = 'contabilidad'
    mensaje = {
        "timestamp": datetime.now().isoformat(),
        "maestro_id": maestro_id
    }

    producer.send(topic, value=mensaje)
    print(f"Enviando mensaje: {mensaje} al topic {topic}")
    time.sleep(2)


if __name__ == "__main__":

    print("-- Bienvenido al sistema MAMOCHI! --\n> Primero, deberas inscribirte.")
    nombre = input("> Por favor, ingrese su nombre:")
    email = input("> Ahora, ingrese su email:")
    paid = input("> ¿Desea pagar para ser inscrito más rapido?")

    send_inscripcion(nombre, email, paid)

    while True:
        maestro = get_maestro_by_email(email)
        print("-- Menú MAMOCHI --")
        print("1. Realizar ventas hasta acabar stock.")
        print("2. Reponer stock.")
        print("3. Solicitar contabilidad.")
        opcion = input("0. Salir")

        if opcion == 0:
            print("Adios!")
            break
        elif opcion == 1:
            for _ in range(10):
                send_venta(maestro.id)

        elif opcion == 2:
            send_ingrediente(maestro.id)

        elif opcion == 3:
            send_contabilidad(maestro.id)

    # Cerrar producer
    producer.close()
