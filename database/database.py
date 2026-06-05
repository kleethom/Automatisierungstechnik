import csv
import os

FILE = "database/data.csv"

HEADER = [
    "bottle",
    "recipe",
    "red_fill_level",
    "blue_fill_level",
    "green_fill_level",
    "red_vibration",
    "blue_vibration",
    "green_vibration",
    "red_temp",
    "blue_temp",
    "green_temp",
    "final_weight",
    "is_cracked",
    "drop_oscillation"
]


def save_bottle(row):

    file_exists = os.path.exists(FILE)

    with open(FILE, "a", newline="") as f:

        writer = csv.DictWriter(
            f,
            fieldnames=HEADER
        )

        if not file_exists:
            writer.writeheader()

        writer.writerow(row)

    print(
        f"Flasche {row['bottle']} gespeichert."
    )