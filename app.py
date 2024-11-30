from flask import Flask, render_template, request, jsonify
import hashlib
import json
from time import time

app = Flask(__name__)

# Blockchain logic
class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, time(), "Genesis Block", "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, data):
        previous_block = self.get_latest_block()
        new_block = Block(len(self.chain), time(), data, previous_block.hash)
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            # Check if current block's hash is valid
            if current_block.hash != current_block.calculate_hash():
                return False

            # Check if current block's previous hash matches the previous block's hash
            if current_block.previous_hash != previous_block.hash:
                return False

        return True

# Instantiate the blockchain
election_blockchain = Blockchain()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_vote', methods=['POST'])
def add_vote():
    voter_id = request.form['voterId']
    candidate = request.form['candidate']
    election_blockchain.add_block({"voter_id": voter_id, "candidate": candidate})
    return jsonify({"message": "Vote added successfully!"})

@app.route('/get_blockchain', methods=['GET'])
def get_blockchain():
    blockchain_data = []
    for block in election_blockchain.chain:
        blockchain_data.append({
            "index": block.index,
            "timestamp": block.timestamp,
            "data": block.data,
            "previous_hash": block.previous_hash,
            "hash": block.hash
        })
    return jsonify(blockchain_data)

if __name__ == "__main__":
    app.run(debug=True)
