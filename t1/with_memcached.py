import json
import time
import numpy as np
import matplotlib.pyplot as plt
from pymemcache.client.base import Client

mc = Client(('localhost', 11211))
avoided_json_lookups: int = 0


def find_car_by_id(target_id, file_path="./cars2.json"):
    global avoided_json_lookups
    # Revisar si ya esta en cache
    cached_result = mc.get(target_id)
    if cached_result:
        avoided_json_lookups += 1
        return json.loads(cached_result)

    # No está en cache
    target_id = int(target_id)
    with open(file_path, 'r') as f:
        f.seek(0, 2)
        total_size = f.tell()

        low = 0
        high = total_size

        while low <= high:
            mid = (low + high) // 2
            f.seek(mid)

            while f.read(1) != "{":
                f.seek(f.tell() - 2)

            obj_str = "{"

            while True:
                char = f.read(1)
                obj_str += char
                if char == "}":
                    break

            obj = json.loads(obj_str)

            if obj["id"] == target_id:
                # Agregar al caché
                mc.set(str(target_id), json.dumps(obj), expire=3600)  # Cache for 1 hour
                return obj
            elif obj["id"] < target_id:
                low = mid + 1
            else:
                high = mid - 1

    return None


def simulate_searches(n_search):
    keys_to_search = [f"{i}" for i in np.random.randint(1, 101, n_search)]
    global avoided_json_lookups

    # Métricas
    time_memcached = 0
    individual_times = []

    count = 0
    for key in keys_to_search:
        # clear console
        count += 1
        print("\033[H\033[J")
        print(f"Searching : {count}/{n_search}")
        start_time = time.time()
        find_car_by_id(key)
        elapsed_time = time.time() - start_time
        individual_times.append(elapsed_time)
        time_memcached += elapsed_time

    print(f"Total time with memcached: {round(time_memcached, 2)}s for {n_search} searches.")
    print(f"Average time with memcached: {round(np.average(individual_times), 4)}s.")
    print(f"Number of times JSON lookup was avoided: {avoided_json_lookups}")
    plt.plot(individual_times)
    plt.xlabel("Searches (n)")
    plt.ylabel("Time (s)")
    plt.title("Tiempo de búsqueda usando Memcached")
    plt.show()


if __name__ == "__main__":
    while True:
        print("\nChoose an operation:")
        print("1. Get")
        print("2. Simulate Searches")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            key = input("Enter key: ")
            value = find_car_by_id(key)
            if value is not None:
                print(f"Value: {value}")
        elif choice == "2":
            n_searches = int(input("Enter the number of searches you want to simulate: "))
            simulate_searches(n_searches)
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")
