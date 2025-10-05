from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app) # allow CORS for all routes. change this if you're going to deploy this!!
app.config['CORS_HEADERS'] = 'Content-Type'

# Talk to handleSubmit in SimulatorView.vue
@app.route('/simulate', methods=['POST'])
@cross_origin()
def simulate():

    # Get request from handleSubmit at localhost.../simulate
    data = request.get_json()
    diameter = data.get('diameter')
    velocity = data.get('velocity')
    mass = data.get('mass')
    longitude = data.get('longitude')
    latitude = data.get('latitude')

    print(f"Received: diameter={diameter}, velocity={velocity}, mass={mass}, longitude={longitude}, latitude={latitude},")

    # Example "processing" — replace with your real logic

    # Run NN model.

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
                    })


# Function for finding earthquakes similar to submitted asteroid
def run_model(diameter, velocity, mass, longitude, latitude):
    # input data to model
    # get earthquake destruction
    # return results to simulate()
    return

# Returns circles of damage with decreasing serverity form center of impact.
# For the visualization dialog which draws the concentric circles.
def calc_impact_radius(diameter, velocity, mass):
    
    return


if __name__ == '__main__':
    app.run(debug=True)
