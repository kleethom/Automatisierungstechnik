import json

from database.database import save_bottle

bottles = {}
latest_temperature = {}


def get_bottle(bottle_id):

    if bottle_id not in bottles:

        bottles[bottle_id] = {
            "bottle": bottle_id
        }

    return bottles[bottle_id]


def process_message(topic, data):

    topic_end = topic.replace(
        "aut/SoSe26/learning_factory_simulation/", ""
    )

    # Temperatur

    if topic_end == "temperature":

        dispenser = data["dispenser"]

        latest_temperature[dispenser] = data["temperature_C"]

        return

    # Dispenserdaten

    if topic_end.startswith("dispenser_"):

        bottle = str(data["bottle"])

        row = get_bottle(bottle)

        color = topic_end.split("_")[1]

        row[f"{color}_fill_level"] = data["fill_level_grams"]
        row[f"{color}_vibration"] = data["vibration-index"]
        row[f"{color}_temp"] = latest_temperature.get(
            data["dispenser"], None
        )

        row["recipe"] = data["recipe"]

        return

    # Endgewicht

    if topic_end == "scale/final_weight":

        bottle = str(data["bottle"])

        row = get_bottle(bottle)

        row["final_weight"] = data["final_weight"]

        return

    # Schwingung

    if topic_end == "drop_oscillation":

        bottle = str(data["bottle"])

        row = get_bottle(bottle)

        row["drop_oscillation"] = json.dumps(
            data["drop_oscillation"]
        )

        return

    # Label

    if topic_end == "ground_truth":

        bottle = str(data["bottle"])

        row = get_bottle(bottle)

        row["is_cracked"] = int(data["is_cracked"])

        save_bottle(row)