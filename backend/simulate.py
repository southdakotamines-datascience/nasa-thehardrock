from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

# For circles
import math

app = Flask(__name__)
cors = CORS(app) # allow CORS for all routes. change this if you're going to deploy this!!
app.config['CORS_HEADERS'] = 'Content-Type'

# Talk to handleSubmit in SimulatorView.vue
@app.route('/simulate', methods=['POST'])
@cross_origin()
def simulate():

    # Import NN model

    # Get request from handleSubmit at localhost.../simulate
    data = request.get_json()
    diameter = data.get('diameter')
    velocity = data.get('velocity')
    mass = data.get('mass')
    longitude = data.get('longitude')
    latitude = data.get('latitude')

    print(f"Received: diameter={diameter}, velocity={velocity}, mass={mass}, longitude={longitude}, latitude={latitude},")

    # Calculate crater diamater.
    is_water_impact = is_in_water(latitude, longitude)
    crater_diameter = calc_impact_diameter(velocity, mass, is_water_impact)

    # Calculate destruction from crater using population density.
    # Query population density data (in repo) using closest lat/long.
    pop_density = get_population_density(latitude, longitude)
    pop_enclosed = calc_total_population(pop_density, crater_diameter)

    # Run NN model to get secondary earthquake destruction effects.

    energy = 0.5 * mass * velocity**2

    # Send json response to handleSubmit
    return jsonify({'housesDamaged': energy,
                    'damageAmountOrder': energy,
                    'injuries': energy,
                    'housesDestroyed': energy,
                    'housesDamagedAmountOrder': energy,
                    'deaths': energy,
                    'damageMillionsDollars': energy,
                    'missing': energy,
                    'missingAmountOrder': energy,
                    'total_destruction_radius_m': energy,
                    'severe_damage_radius_m': energy,
                    'moderate_damage_radius_m': energy
                    })


# Function for finding earthquakes similar to submitted asteroid
def run_model():# model_params):
    # input data to model
    # get earthquake destruction
    # return results to simulate()
    return


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


def get_population_density(lat, long):
    # Load population density parquet into pandas
    
    # Filter population density parquet by closest lat and long

    # Return population density
    return


# Rough estimate of population enclosed by the crater: assuming constant density for entire area
# Uses density value at the impact center (input lat and long)
def calc_total_population(pop_density, crater_diameter):
    circular_area = math.pi * crater_diameter
    population = round(pop_density * circular_area)

    return population


if __name__ == '__main__':
    app.run(debug=True)
