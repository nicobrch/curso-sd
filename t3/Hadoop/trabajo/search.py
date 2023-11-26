import redis
import json


def search_word_in_redis(word):
    redis_host = 'localhost'
    redis_port = 6379
    redis_db = 0

    redis_conn = redis.StrictRedis(host=redis_host, port=redis_port, db=redis_db)

    keys = redis_conn.keys(f"{word}:*")

    results = []

    for key in keys:
        redis_data = redis_conn.hgetall(key.decode('utf-8'))

        results.append({
            'Documento': int(redis_data[b'Documento']),
            'Frecuencia': int(redis_data[b'Frequencia']),
            'url': redis_data[b'URL'].decode('utf-8')
        })

    return results


def main():
    user_input = input("Buscar Palabra: ")

    search_results = search_word_in_redis(user_input)

    formatted_results = json.dumps({user_input: search_results}, indent=2, ensure_ascii=False)
    print(formatted_results)


if __name__ == "__main__":
    main()
