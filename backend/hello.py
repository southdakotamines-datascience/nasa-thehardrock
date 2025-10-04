from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/simulate', methods=['POST'])
def simulate():
    data = request.get_json()
    diameter = data.get('diameter')
    velocity = data.get('velocity')
    mass = data.get('mass')

    print(f"Received: diameter={diameter}, velocity={velocity}, mass={mass}")

    # Example "processing" — replace with your real logic
    energy = 0.5 * mass * velocity**2

    return jsonify({'result': energy})


if __name__ == '__main__':
    app.run(debug=True)
