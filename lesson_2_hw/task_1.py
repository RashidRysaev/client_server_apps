# Task 1:

# a:

import csv
import os
import re

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


def parse_files():
    data_dir = "/Users/Rashid/Documents/AaP/GeekBrains Cources/12. Клиент-серверные приложения на Python/client_server_apps/lesson_2_hw"
    result = []
    source_files = [i for i in os.listdir(data_dir) if i.split(".")[1] == "txt"]

    for filename in source_files:
        filepath = os.path.join(data_dir, filename)

        with open(filepath, encoding="cp1251") as fl:
            for line in fl.readlines():
                result += re.findall(r"^(\w[^:]+).*:\s+([^:\n]+)\s*$", line)

    return result


def get_data():
    data = parse_files()
    # print(data)
    os_prod_list, os_name_list, os_code_list, os_type_list = [], [], [], []
    main_data = [["Изготовитель системы", "Название ОС", "Код продукта", "Тип системы"]]

    for item in data:
        os_prod_list.append(item[1]) if item[0] == main_data[0][0] else None
        os_name_list.append(item[1]) if item[0] == main_data[0][1] else None
        os_code_list.append(item[1]) if item[0] == main_data[0][2] else None
        os_type_list.append(item[1]) if item[0] == main_data[0][3] else None

    for i in range(len(os_prod_list)):
        main_data.append([os_prod_list[i], os_name_list[i], os_code_list[i], os_type_list[i]])

    return main_data


# b:


def write_to_csv(filepath):
    data = get_data()

    dir_, filename = os.path.split(filepath)

    filepath = os.path.join(CURRENT_DIR, dir_, filename)

    with open(filepath, "w", encoding="utf-8", newline="") as csv_file:
        writer = csv.writer(csv_file, delimiter=",", quoting=csv.QUOTE_NONNUMERIC)

        for line in data:
            writer.writerow(line)

    return


# c:

write_to_csv("main_data.csv")
