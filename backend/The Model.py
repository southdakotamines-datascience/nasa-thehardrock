import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.model_selection import train_test_split
from sklearn.metrics import root_mean_squared_error, mean_absolute_error
from scipy.spatial import KDTree

# --- 1. Data Loading ---
print("Loading earthquake data...")
earthquakes_df = pd.read_csv('data/noaa_earthquakes_2000_2025_cleaned.csv')

print("Loading population data from Parquet file (this may take a while)...")
population_df = pd.read_parquet('data/full_population_data_chunked.parquet')

# --- 2. Spatial Join with KD-Tree ---
print("Preparing coordinates for spatial join...")
pop_coords = np.c_[population_df['longitude'], population_df['latitude']]
eq_coords = np.c_[earthquakes_df['longitude'], earthquakes_df['latitude']]

print("Building KD-Tree for fast spatial lookups...")
kdtree = KDTree(pop_coords)

print("Querying tree to find nearest population data for each earthquake...")
distances, indices = kdtree.query(eq_coords, k=1)

print("Assigning population data to earthquakes...")
earthquakes_df['population'] = population_df.iloc[indices]['population'].values


# --- 3. Advanced Feature Engineering ---
print("Performing feature engineering on enriched data...")
# --- FIX #1: Restored the full, more informative feature set ---
features = ['eqMagMw', 'eqDepth', 'population']
targets = ['housesDamagedTotal', 'deathsTotal', 'injuriesTotal']

X = earthquakes_df[features]
print(X.columns)

poly = PolynomialFeatures(degree=2, include_bias=False)
X_poly = poly.fit_transform(X)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_poly)


# --- 4. Train a Specialized Model for Each Target ---
final_results = {}

for target_variable in targets:
    print(f"\n--- Training Specialized Model with Population Data for: {target_variable} ---")
    
    y = earthquakes_df[[target_variable]].fillna(earthquakes_df[target_variable].median())
    y_log = np.log1p(y)

    X_train, X_test, y_train_log, y_test_log = train_test_split(X_scaled, y_log, test_size=0.2, random_state=42)

    specialized_model = xgb.XGBRegressor(
        objective='reg:squarederror', n_estimators=1000, learning_rate=0.05,
        max_depth=7, subsample=0.8, colsample_bytree=0.8,
        random_state=42, n_jobs=-1, early_stopping_rounds=50
    )

    specialized_model.fit(X_train, y_train_log, eval_set=[(X_test, y_test_log)], verbose=False)

    y_pred_log = specialized_model.predict(X_test)
    y_pred = np.expm1(y_pred_log)
    y_test_original = np.expm1(y_test_log)

    # save the model
    specialized_model.save_model(f"xgboostmodel_{target_variable}.bin")

    rmse = root_mean_squared_error(y_test_original, y_pred)
    mae = mean_absolute_error(y_test_original, y_pred)
    print(f"Final RMSE for {target_variable}: {rmse:.4f}")
    print(f"Final MAE for {target_variable}: {mae:.4f}")

    final_results[f'Actual_{target_variable}'] = y_test_original.values.flatten()
    final_results[f'Predicted_{target_variable}'] = y_pred.flatten()


# --- 5. Final Output ---
results_df = pd.DataFrame(final_results)
results_df.to_csv('final_predictions_with_population.csv', index=False)
print("\n--- All predictions saved to final_predictions_with_population.csv ---")
print(results_df.head())
