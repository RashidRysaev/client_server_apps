# Task 3:

import yaml

# a:

data = {
    "info": ["some", "information", "we", "have_to", "proceed"],
    "number": 13,
    "dict": {"num_1": "10€", "num_2": "15€", "num_3": "20€"},
}

# b:

with open("lesson_2_hw/write_to_yaml.yaml", "w") as file:
    yaml.dump(data, file, default_flow_style=False, allow_unicode=True)

# c:

with open("lesson_2_hw/write_to_yaml.yaml", encoding="utf-8") as file:
    print(file.read())
