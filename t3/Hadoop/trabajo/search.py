import json
import os
import redis
import re


def insert_data(connection):
    print("Insertando archivos...")
    with open('outhadoop/part-00000', 'r') as archivo:
        next(archivo)
        for linea in archivo:
            datos = re.findall(r'\b\w+\b|\([^)]*\)', linea)

            letra = datos[0]
            pares = [tuple(map(int, par.strip('()').split(' '))) for par in datos[1:]]
            for n, m in pares:
                connection.hsetnx(f"registros:{letra}", n, m)


def search_word(connection):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\nGooglent")
    palabra = input("Buscar: ")

    registros_key = f"registros:{palabra}"
    resultados = connection.hgetall(registros_key)

    resultados_json = [{"documento": int(doc), "frecuencia": int(freq)} for doc, freq in resultados.items()]

    print(json.dumps(resultados_json, indent=2))


redis_conn = redis.StrictRedis(
    host="redis",
    port=6379,
    decode_responses=True
)

try:
    insert_data(redis_conn)
    search_word(redis_conn)

except Exception as error:
    print("Error:", error)
finally:
    if redis_conn:
        redis_conn.close()
        print("Redis connection is closed")
