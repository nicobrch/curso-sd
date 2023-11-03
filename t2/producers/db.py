import peewee as pw
import base64
from datetime import datetime, timedelta
from peewee import fn

# Definir base de datos
db = pw.PostgresqlDatabase(
    database='proyecto',
    user='postgres',
    password='postgres',
    host='db'
)


# Tabla maestro
class Maestro(pw.Model):
    id = pw.PrimaryKeyField()
    nombre = pw.CharField(max_length=50)
    email = pw.CharField(unique=True)
    stock = pw.IntegerField(default=0)
    secret_key = pw.CharField(max_length=255)

    class Meta:
        database = db


# Tabla venta
class Venta(pw.Model):
    id = pw.PrimaryKeyField()
    maestro_id = pw.ForeignKeyField(Maestro, backref='ventas')
    monto = pw.IntegerField()
    fecha = pw.DateTimeField(default=datetime.now)

    class Meta:
        database = db


# Tabla maestro
class Reposicion(pw.Model):
    id = pw.PrimaryKeyField()
    maestro_id = pw.ForeignKeyField(Maestro, backref='reposiciones')
    stock = pw.IntegerField()
    fecha = pw.DateTimeField(default=datetime.now)

    class Meta:
        database = db


# Establecer conexión
db.connect()


def insert_maestro(nombre, email):
    try:
        nombre = nombre.lower()
        email = email.lower()
        secret_key = base64.b64encode(f"{nombre}_{email}".encode()).decode()
        maestro = Maestro.create(nombre=nombre, email=email, stock=10, secret_key=secret_key)
        return maestro
    except pw.IntegrityError:
        return None


def get_maestro_by_id(maestro_id):
    try:
        maestro = Maestro.get(Maestro.id == maestro_id)
        return maestro
    except Maestro.DoesNotExist:
        return None


def get_maestro_by_email(maestro_email):
    try:
        maestro = Maestro.get(Maestro.email == maestro_email)
        return maestro
    except Maestro.DoesNotExist:
        return None


def set_maestro_stock(maestro_id, new_stock):
    try:
        maestro = Maestro.get(Maestro.id == maestro_id)
        maestro.stock = new_stock
        maestro.save()
        return maestro
    except Maestro.DoesNotExist:
        return None


def get_maestro_stock(maestro_id):
    try:
        stock = Maestro.select(Maestro.stock).where(Maestro.id == maestro_id)
        return stock
    except Maestro.DoesNotExist:
        return None


def get_all_maestros():
    return Maestro.select()


def query_maestro_ventas_last_3_days(maestro_id):
    # Calcular los ultimos 3 dias
    seven_days_ago = datetime.now() - timedelta(days=3)

    # Query que obtiene el conteo de ventas y la suma de montos
    query = (Venta
             .select(fn.COUNT(Venta.id).alias('ventas_count'), fn.SUM(Venta.monto).alias('total_montos'))
             .where((Venta.maestro_id == maestro_id) & (Venta.fecha >= seven_days_ago)))

    result = query.dicts().get()

    return result if result else {'ventas_count': 0, 'total_montos': 0}


def insert_venta(maestro_id, monto):
    try:
        venta = Venta.create(maestro_id=maestro_id, monto=monto)
        return venta
    except Maestro.DoesNotExist:
        return None


def get_ventas_by_maestro_id(maestro_id):
    return Venta.select().where(Venta.maestro_id == maestro_id)


def insert_reposicion(maestro_id, stock):
    try:
        reposicion = Reposicion.create(maestro_id=maestro_id, stock=stock)
        return reposicion
    except Maestro.DoesNotExist:
        return None


def get_reposiciones_by_maestro_id(maestro_id):
    return Reposicion.select().where(Reposicion.maestro_id == maestro_id)


# Cerrar conexión
db.close()
