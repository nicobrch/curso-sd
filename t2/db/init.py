import peewee as pw
import base64
from datetime import datetime

# Define the SQLite database connection
db = pw.SqliteDatabase('mamochi.db')


# Define the "maestro" table
class Maestro(pw.Model):
    id = pw.PrimaryKeyField()
    nombre = pw.CharField(max_length=50)
    email = pw.CharField(unique=True)
    stock = pw.IntegerField(default=0)
    secret_key = pw.CharField(max_length=255)

    class Meta:
        database = db


# Define the "venta" table
class Venta(pw.Model):
    id = pw.PrimaryKeyField()
    maestro_id = pw.ForeignKeyField(Maestro, backref='ventas')
    monto = pw.IntegerField()
    fecha = pw.DateTimeField(default=datetime.now)

    class Meta:
        database = db


# Define the "reposicion" table
class Reposicion(pw.Model):
    id = pw.PrimaryKeyField()
    maestro_id = pw.ForeignKeyField(Maestro, backref='reposiciones')
    stock = pw.IntegerField()
    fecha = pw.DateTimeField(default=datetime.now)

    class Meta:
        database = db


# Create tables in the database if they don't exist
db.connect()


def create_tables():
    db.create_tables([Maestro, Venta, Reposicion])


def insert_maestro(nombre, email):
    try:
        secret_key = base64.b64encode(f"{nombre}".encode()).decode()
        Maestro.create(nombre=nombre, email=email, stock=0, secret_key=secret_key)
        return True
    except pw.IntegrityError:
        return False


def get_maestro_by_id(maestro_id):
    try:
        maestro = Maestro.get(Maestro.id == maestro_id)
        return maestro
    except Maestro.DoesNotExist:
        return None


def get_all_maestros():
    return Maestro.select()


# Close the database connection when done
db.close()
