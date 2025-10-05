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

    print(f"Received: diameter={diameter}, velocity={velocity}, mass={mass}")

    # Example "processing" — replace with your real logic
    energy = 0.5 * mass * velocity**2

    # Send json response to handleSubmit
    return jsonify({'result': energy})


# Function for finding earthquakes similar to submitted asteroid
def run_model():
    # input data to model
    # get earthquake destruction
    # return results to simulate()
    return


if __name__ == '__main__':
    app.run(debug=True)
