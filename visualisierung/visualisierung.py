
import pandas as pd
import matplotlib.pyplot as plt
import time

def start_visualisierung():

    plt.ion()

    fig, ax = plt.subplots()

    while True:

        try:

            df = pd.read_csv(
                "database/data.csv"
            )

            ax.clear()

            ax.plot(
                df["final_weight"]
            )

            ax.set_title(
                "Final Weight"
            )

            plt.draw()

            plt.pause(5)

        except Exception as e:

            print(
                "Visualisierungsfehler:",
                e
            )

            time.sleep(5)
