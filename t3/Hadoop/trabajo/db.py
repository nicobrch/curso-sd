import re
import redis

redis_host = 'localhost'
redis_port = 6379
redis_db = 0

redis_conn = redis.StrictRedis(host=redis_host, port=redis_port, db=redis_db)


def process_hadoop_output(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split('\t')
            if len(parts) == 2:
                word = parts[0]
                data_str = parts[1]

                if data_str == "[ (Document1, Count1), ... ]":
                    continue

                matches = re.findall(r'\((.*?)\)', data_str)

                for match in matches:
                    item = str(match)
                    item.replace(",", "")
                    doc_number, page_url, frecuency = item.split(" ")
                    # Insertar
                    redis_key = f"{word}"
                    redis_data = {
                        'Palabra': word,
                        'Documento': doc_number,
                        'Frecuencia': frecuency,
                        'URL': page_url,
                    }
                    redis_conn.hmset(redis_key, redis_data)


part_0000_path = 'outhadoop/part-00000'

process_hadoop_output(part_0000_path)

print("Data inserted into Redis successfully.")
