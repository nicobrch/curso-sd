import json
from kafka import KafkaConsumer
from db import (insert_maestro, insert_venta, insert_reposicion, set_maestro_stock, get_maestro_by_id,
                query_maestro_ventas_last_3_days)

# Configuracion de Correo
# email_sender = os.getenv('EMAIL_SENDER')
# email_password = os.getenv('EMAIL_PASSWORD')

# Configuracion Broker Kafka
bootstrap_servers = 'kafka:9092'  # Broker address
topics = ['inscripciones', 'ingredientes', 'ventas', 'contabilidad']

# Crear consumer
consumer = KafkaConsumer(
    *topics,
    bootstrap_servers=[bootstrap_servers],
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)


# Generar correo
def send_mail(email_receiver, subject, body):
    mail = EmailMessage()
    mail['From'] = email_sender
    mail['To'] = email_receiver
    mail['subject'] = subject
    mail.set_content(body)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 587, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, mail.as_string())
        print("Email enviado con éxito")


# Procesar mensajes
def process_aprobacion(message):
    nombre = message.value.get('nombre')
    email = message.value.get('email')

    if nombre is not None and email is not None:
        # Insertar a la BDD
        maestro = insert_maestro(nombre, email)
        if maestro:
            print(f"Solicitud aprobada y agregada a la BDD. Maestro ID: {maestro.id}, Nombre: {maestro.nombre}.")
            print(f"Su credencial de ingreso es: {maestro.secret_key} y fue enviada a {maestro.email}")
        else:
            print("Error al insertar a la BDD.")
    else:
        print("Solicitud de inscripción no tiene nombre o email.")


def process_distribucion(message):
    maestro_id = message.value.get('maestro_id')
    new_stock = 10

    if maestro_id is not None:
        # Insertar a la BDD
        reposicion = insert_reposicion(maestro_id=maestro_id, stock=new_stock)
        if reposicion:
            print(f"Solicitud aprobada y agregada a la BDD. Stock Repuesto: {reposicion.stock}.")
            # Agregar stock a maestro
            maestro = set_maestro_stock(maestro_id=maestro_id, new_stock=new_stock)
            if maestro:
                print(f"Se ha respuesto {maestro.stock} de stock al maestro {maestro.id}.")
            else:
                print("Error al actualizar el stock del maestro.")
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


def process_contabilidad(message):
    maestro_id = message.value.get('maestro_id')

    if maestro_id is not None:
        # Insertar a la BDD
        result = query_maestro_ventas_last_3_days(maestro_id=maestro_id)
        if result:
            maestro = get_maestro_by_id(maestro_id)
            subject = "RECUENTO CONTABILIDAD"
            body = "Ha hecho {result.get('ventas_count')} ventas y ha ganado ${result.get('total_montos')"
            send_mail(maestro.email, subject, body)
            print(f"Recuento de ventas enviadas al mail del maestro. El maestro ha hecho {result.get('ventas_count')} "
                  f"ventas y ha ganado ${result.get('total_montos')}")
        else:
            print("Error al insertar a la BDD.")
    else:
        print("Solicitud de resultado no tiene ID Maestro")


# Consumir mensajes
for msg in consumer:
    print(f"Solicitud recibida de topico {msg.topic}: {msg.value}")

    if msg.topic == topics[0]:
        process_aprobacion(msg)
    elif msg.topic == topics[1]:
        process_distribucion(msg)
    elif msg.topic == topics[2]:
        process_venta(msg)
    elif msg.topic == topics[3]:
        process_contabilidad(msg)
