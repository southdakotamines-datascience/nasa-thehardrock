from flask import Flask, request, jsonify

app = Flask(__name__)


# Talk to handleSubmit in SimulatorView.vue
@app.route('/simulate', methods=['POST'])
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
def search_earthquakes():
    # load csv
    # filtering logic
    # return summary/results to simulate()
    return


if __name__ == '__main__':
    app.run(debug=True)
