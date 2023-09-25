import json


def format_json(input_file, output_file):
    try:
        with open(input_file, 'r') as f:
            data = json.load(f)

        # Escribir archivo en una linea
        with open(output_file, 'w') as f:
            json.dump(data, f, separators=(',', ':'))

        print(f'Guardado en {output_file}')
    except Exception as e:
        print(f'Error: {e}')


if __name__ == '__main__':
    in_file = 'cars.json'
    out_file = 'cars2.json'

    format_json(in_file, out_file)
