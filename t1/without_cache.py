import json
import time
import numpy as np
import matplotlib.pyplot as plt


def find_car_by_id(target_id, file_path="./cars2.json"):
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
                return obj
            elif obj["id"] < target_id:
                low = mid + 1
            else:
                high = mid - 1

    return None


def simulate_searches(n_search):
    keys_to_search = [f"{i}" for i in np.random.randint(1, 101, n_search)]

    # Métricas
    time_without_cache = 0
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
        time_without_cache += elapsed_time

    print(f"Total time without cache: {round(time_without_cache, 2)}s for {n_search} searches.")
    print(f"Average time without cache: {round(np.average(individual_times), 4)}s for {n_search} searches.")
    plt.plot(individual_times)
    plt.xlabel("Searches (n)")
    plt.ylabel("Time (s)")
    plt.title("Tiempo de búsqueda sin usar caché")
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
