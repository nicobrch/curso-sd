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
            'Frecuencia': int(redis_data[b'Frecuencia']),
            'url': redis_data[b'URL'].decode('utf-8')
        })

    # Sort the results by frequency in descending order
    sorted_results = sorted(results, key=lambda x: x['Frecuencia'], reverse=True)

    # Retrieve the top 5 results
    top_5_results = sorted_results[:5]

    return top_5_results


def main():
    user_input = input("Buscar Palabra: ")

    top_5_results = search_word_in_redis(user_input)

    formatted_results = json.dumps({user_input: top_5_results}, indent=2, ensure_ascii=False)
    print(formatted_results)


if __name__ == "__main__":
    main()
