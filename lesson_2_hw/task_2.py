# Task 2:

import json

# a:


def write_order_to_json(item, quantity, price, buyer, date):
    file = "lesson_2_hw/orders.json"

    data = {}

    with open(file, encoding="utf-8") as f:
        data = json.loads(f.read())

    data["orders"].append(
        {
            "item": item,
            "quantity": quantity,
            "price": price,
            "buyer": buyer,
            "date": date,
        }
    )

    with open(file, "w+", encoding="utf-8") as f:
        json.dump(data, f, indent=4, separators=(",", ": "))

    return


# b:

write_order_to_json("something", 2, 20, "somebody", "12.12.12.")
