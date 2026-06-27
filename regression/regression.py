import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error


# =============================
# Einstellungen
# =============================

TRAIN_DATA_PATH = "database/data1.csv"
PREDICT_DATA_PATH = "database/X.csv"

OUTPUT_PATH = "regression/reg_Außerlechner-Kleemayr.csv"
RESULTS_PATH = "regression/regression_results.csv"


# =============================
# 1. Trainingsdaten laden
# =============================

df = pd.read_csv(TRAIN_DATA_PATH)

# Spaltennamen aus data.csv an die Namen aus X.csv / Angabe anpassen
df = df.rename(columns={
    "red_fill_level": "fill_level_grams_red",
    "blue_fill_level": "fill_level_grams_blue",
    "green_fill_level": "fill_level_grams_green",

    "red_vibration": "vibration_index_red",
    "blue_vibration": "vibration_index_blue",
    "green_vibration": "vibration_index_green",

    "red_temp": "temperature_red",
    "blue_temp": "temperature_blue",
    "green_temp": "temperature_green"
})


# =============================
# 2. Feature-Sets laut Angabe
# =============================

target = "final_weight"

feature_sets = [
    [
        "fill_level_grams_red",
        "fill_level_grams_blue",
        "fill_level_grams_green"
    ],
    [
        "fill_level_grams_red",
        "fill_level_grams_blue",
        "fill_level_grams_green",
        "vibration_index_red",
        "vibration_index_blue",
        "vibration_index_green"
    ],
    [
        "fill_level_grams_red",
        "fill_level_grams_blue",
        "fill_level_grams_green",
        "vibration_index_red",
        "vibration_index_blue",
        "vibration_index_green",
        "temperature_red",
        "temperature_blue",
        "temperature_green"
    ]
]


# =============================
# 3. Modelle trainieren
# =============================

results = []
models = []

for features in feature_sets:
    X = df[features]
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    model = LinearRegression()
    model.fit(X_train, y_train)

    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)

    mse_train = mean_squared_error(y_train, y_train_pred)
    mse_test = mean_squared_error(y_test, y_test_pred)

    results.append({
        "Genutzte Spalten (X)": ", ".join(features),
        "Modell-Typ": "Linear",
        "MSE Training": mse_train,
        "MSE Test": mse_test
    })

    models.append({
        "features": features,
        "model": model,
        "mse_train": mse_train,
        "mse_test": mse_test
    })


# =============================
# 4. Ergebnis-Tabelle
# =============================

results_df = pd.DataFrame(results)

print("\nVergleich der linearen Modelle:")
print(results_df.to_string(index=False))

results_df.to_csv(RESULTS_PATH, index=False)


# =============================
# 5. Bestes Modell auswählen
# =============================

best = min(models, key=lambda x: x["mse_test"])

best_model = best["model"]
best_features = best["features"]

print("\nBestes Modell:")
print(best_features)
print(f"MSE Training: {best['mse_train']:.6f}")
print(f"MSE Test:     {best['mse_test']:.6f}")


# =============================
# 6. Formel ausgeben
# =============================

formula_parts = []

for coef, feature in zip(best_model.coef_, best_features):
    formula_parts.append(f"({coef:.6f} * {feature})")

formula = "y = " + " + ".join(formula_parts) + f" + {best_model.intercept_:.6f}"

print("\nFormel des besten Modells:")
print(formula)


# =============================
# 7. X.csv laden und Prognose erstellen
# =============================

X_pred = pd.read_csv(PREDICT_DATA_PATH)

missing_columns = [col for col in best_features if col not in X_pred.columns]

if missing_columns:
    raise ValueError(f"Diese Spalten fehlen in X.csv: {missing_columns}")

y_hat = best_model.predict(X_pred[best_features])


# =============================
# 8. reg_<Gruppe>.csv speichern
# =============================

reg_df = pd.DataFrame({
    "Flaschen ID": X_pred["bottle"],
    "y_hat": y_hat
})

reg_df.to_csv(OUTPUT_PATH, index=False)

print(f"\nPrognose wurde gespeichert unter: {OUTPUT_PATH}")
print(reg_df.head())