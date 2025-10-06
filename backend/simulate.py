from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import xgboost as xg
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
import pandas as pd
import py7zr
import numpy as np

# For circles
import math

app = Flask(__name__)
cors = CORS(app) # allow CORS for all routes. change this if you're going to deploy this!!
app.config['CORS_HEADERS'] = 'Content-Type'

with py7zr.SevenZipFile('data/full_population_data_chunked.7z', 'r') as archive:
    archive.extractall(path='data')

population_df = pd.read_parquet("data/full_population_data_chunked.parquet")
deathsTotal_model = xg.XGBRegressor()
deathsTotal_model.load_model("xgboostmodel_deathsTotal.bin")

housesDamagedTotal_model = xg.XGBRegressor()
housesDamagedTotal_model.load_model("xgboostmodel_housesDamagedTotal.bin")

injuriesTotal_model = xg.XGBRegressor()
injuriesTotal_model.load_model("xgboostmodel_injuriesTotal.bin")

# Talk to handleSubmit in SimulatorView.vue
@app.route('/simulate', methods=['POST'])
@cross_origin()
def simulate():

    # Import NN model

    # Get request from handleSubmit at localhost.../simulate
    data = request.get_json()
    velocity = data.get('velocity')
    mass = data.get('mass')
    longitude = data.get('longitude')
    latitude = data.get('latitude')

    print(f"Received: velocity={velocity}, mass={mass}, longitude={longitude}, latitude={latitude},")

    # Calculate crater diamater.
    # is_water_impact = is_in_water(latitude, longitude)
    crater_diameter = calc_impact_diameter(velocity, mass, False)

    # Calculate destruction from crater using population density.
    # Query population density data (in repo) using closest lat/long.
    Mw = calc_earthquake_magnitude(velocity, mass)
    crater_radii = crater_diameter / 2
    population = get_population(latitude, longitude, crater_radii)

    results = run_model(Mw, crater_radii, population)

    # Run NN model to get secondary earthquake destruction effects.
    earthquake_deaths = results["deaths"].item()
    total_deaths = population + earthquake_deaths

    # Send json response to handleSubmit
    return jsonify({'housesDamaged': str(results["housesDamaged"].item()),
                    'injuries': str(results["injuries"].item()),
                    'deaths': str(total_deaths),
                    'latitude': str(latitude),
                    'longitude': str(longitude),
                    'total_destruction_radius_m': str(crater_radii),
                    'severe_damage_radius_m': str(crater_radii * 4/3),
                    'moderate_damage_radius_m': str(crater_radii * 5/3)
                    })


def run_model(eqMagMw, eqDepth, population):
    X = pd.DataFrame({"eqMagMw": eqMagMw, "eqDepth": eqDepth, "population": population}, index=[0])
    poly = PolynomialFeatures(degree=2, include_bias=False)
    X_poly = poly.fit_transform(X)
    scaler = StandardScaler()

    X_scaled = scaler.fit_transform(X_poly)
    deathsTotal = deathsTotal_model.predict(X_scaled)
    housesDamagedTotal = housesDamagedTotal_model.predict(X_scaled)
    injuriesTotal = injuriesTotal_model.predict(X_scaled)

    return pd.DataFrame({
        "deaths": deathsTotal,
        "housesDamaged": housesDamagedTotal,
        "injuries": injuriesTotal
    })


def is_in_water(lat, long):
    return


# Returns circles of damage with decreasing serverity form center of impact.
# For the visualization dialog which draws the concentric circles.
def calc_impact_diameter(velocity, mass, is_water_impact):
    k = 1.8
    surface_density = 2750
    water_density = 1000
    target_density = water_density if is_water_impact else surface_density
    crater_diameter = k * ((mass / target_density)**(1/3)) * ((velocity**2) / 9.81)
    
    return crater_diameter


def get_population(lat, long, rad_km):
    # Calculates the TOTAL population of all data points within a given radius.
    # --- STEP 1: Calculate the distance from your point to all other points ---
    # This is an approximation where 1 degree latitude = 111.1 km
    lat_dist = (population_df['latitude'] - lat) * 111.1
    long_dist = (population_df['longitude'] - long) * 111.1 * np.cos(np.deg2rad(lat))

    # Use the Pythagorean theorem to find the true distance in km
    population_df['distance_km'] = np.sqrt(lat_dist**2 + long_dist**2)

    # --- STEP 2: Filter the DataFrame to get only the points inside the circle ---
    points_within_radius = population_df[population_df['distance_km'] <= rad_km]

    # --- STEP 3: Sum the 'population' column of the filtered points ---
    # This is the key change to get a single number
    total_population = points_within_radius['population'].sum()
    
    return total_population

def calc_earthquake_magnitude(velocity, mass):
    # Rough estimate of earthquake magnitude from asteroid impact
    # Using kinetic energy to moment magnitude formula
    # ME = (2/3) * log10(E) - 3.2
    # E = 0.5 * m * v^2
    energy = 0.5 * mass * velocity**2
    M_E = (2/3) * math.log10(energy) - 3.2
    # Assume M_E (energy magnitude) is equivalent to moment magnitude
    return M_E

if __name__ == '__main__':
    app.run(debug=True)
