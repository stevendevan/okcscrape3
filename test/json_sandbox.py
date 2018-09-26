import json
import os

#

#


json_test_file = 'json_test_file.json'


def print_test_json():
    with open(json_test_file, 'r') as file:
        result = file.read()

    print(result)


def write_stuff_to_json(stuff, json_file):
    if stuff is None:
        return

    with open(json_file, 'a') as file:
        empty_file = False

        file_length = file.tell()
        if file_length == 0:
            file.write('[')
            empty_file = True
        else:
            # Remove closing bracket (])
            file.truncate(file_length - 1)

        if not empty_file:
            file.write(',')

        json.dump(stuff, file)
        file.write(']')


def main():
    dict1 = {'key1': 'val1', 'key2': 'val2'}
    dict2 = {'key1': 'val3', 'key2': 'val4'}
    data = [dict1, dict2]

    try:
        os.remove(json_test_file)
    except FileNotFoundError:
        pass

    for item in data:
        write_stuff_to_json(item, json_test_file)

    with open(json_test_file, 'r') as file:
        result = json.load(file)

    print(result)


if __name__ == '__main__':
    main()
