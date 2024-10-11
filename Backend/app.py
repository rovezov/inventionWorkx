from flask import Flask, request, jsonify
from flask_cors import CORS
from cipher import encrypt, decrypt
from hardwareSet import hardwareSet

app = Flask(__name__)
CORS(app)

# Initialize a dictionary to store hardware sets
hardware_sets = {}

@app.route('/encrypt', methods=['POST'])
def encrypt_route():
    data = request.json
    result = encrypt(data['text'], data['n'], data['d'])
    return jsonify({'result': result})

@app.route('/decrypt', methods=['POST'])
def decrypt_route():
    data = request.json
    result = decrypt(data['text'], data['n'], data['d'])
    return jsonify({'result': result})

@app.route('/hardware-sets', methods=['GET'])
def get_hardware_sets():
    return jsonify([
        {
            'id': id,
            'name': hw.get_hardware_name(),
            'availability': hw.get_availability(),
            'capacity': hw.get_capacity()
        } for id, hw in hardware_sets.items()
    ])

@app.route('/hardware-sets', methods=['POST'])
def create_hardware_set():
    data = request.json
    new_set = hardwareSet()
    new_set.initialize_name(data['name'])
    new_set.initialize_capacity(data['capacity'])
    set_id = str(len(hardware_sets) + 1)
    hardware_sets[set_id] = new_set
    return jsonify({'id': set_id, 'message': 'Hardware set created successfully'}), 201

@app.route('/hardware-sets/<set_id>/checkout', methods=['POST'])
def checkout_hardware(set_id):
    if set_id not in hardware_sets:
        return jsonify({'error': 'Hardware set not found'}), 404
    
    data = request.json
    result = hardware_sets[set_id].check_out(data['quantity'], data['userName'])
    
    if result == 0:
        return jsonify({'message': 'Checkout successful'})
    else:
        return jsonify({'error': 'Insufficient availability'}), 400

@app.route('/hardware-sets/<set_id>/checkin', methods=['POST'])
def checkin_hardware(set_id):
    if set_id not in hardware_sets:
        return jsonify({'error': 'Hardware set not found'}), 404
    
    data = request.json
    result = hardware_sets[set_id].check_in(data['quantity'], data['userName'])
    
    if result == 0:
        return jsonify({'message': 'Check-in successful'})
    else:
        return jsonify({'error': 'Invalid check-in quantity'}), 400

if __name__ == '__main__':
    # Create a sample hardware set
    sample_set = hardwareSet()
    sample_set.initialize_name("Sample Hardware")
    sample_set.initialize_capacity(10)
    hardware_sets['1'] = sample_set

    app.run(debug=True)