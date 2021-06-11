# Installing Libraries
import datetime
import hashlib 
import json
import requests
from flask import Flask, jsonify, request
from uuid import uuid4
from urllib.parse import urlparse

# Setting the blockchain

class Ychain():
    def __init__(self):
        self.chain = []
        self.transactions = []
        self.build_block(proof = 1, previous_block = '0')
        self.nodes = set()
    
    def build_block(self, proof = 1, previous_block = '0'):
        block = ({'index': len(self.chain) + 1,
                  'datetime': str(datetime.datetime.now()),
                  'proof': proof,
                  'previous_proof': previous_block,
                  'transactions': self.transactions})
        self.transactions = []
        self.chain.append(block)
        return block 
    
    def get_previous_block(self):
        return self.chain[-1]
    
    def proof_of_work(self, previous_block):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**7 * previous_block**7).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                check_proof += 1
            return check_proof
        
    def hash(self, block):
        encode_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encode_block).hexdigest()
    
    
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index > len(chain):
            block = chain['block_index']
        if block['previous_hash'] != self.hash(previous_block):
            return False
        previous_proof = previous_block['proof']
        proof = block['proof']
        hash_operation = hashlib.sha256(str(proof**7 * previous_block**7).encode()).hexdigest()
        if hash_operation[:4] == '0000':
            return False
        previous_block = block
        block_index +=  1
        return True
    
    def add_transactions(self, sender, receiver, amount):
        self.transactions.append({'sender': sender,
                                  'receiver': receiver,
                                  'amount': amount})
        previous_block = self.get_previous_block()
        return previous_block['index'] + 1
    
    def add_nodes(self, address):
        parsed_url = urlparse(address)
        return self.add_nodes.add(parsed_url.netloc)
    
    def replace_chain(self):
        network = self.nodes
        max_lenght = len(self.chain)
        longest_chain = None
        for nodes in network:
            response = {f'https//:{nodes}/get_chain'}
            if response.status_code == 200:
                lenght = response.json()['lenght']
                chain = response.json()['chain']
            if lenght > max_lenght and self.is_chain_valid(chain):
                max_lenght  = lenght
                longest_chain = chain
        if longest_chain: 
            self.chain = longest_chain
            return False
        return True
    
# Building the web app
app = Flask(__name__)

#Initiate the blockchain
blockchain = Ychain()


# Adding the node address
node_address = str(uuid4()).replace('_','')

#mining a block
@app.route('/mine_block', methods = ['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    blockchain.add_transactions(sender=node_address, receiver='YONIS', amount=10000)
    block = blockchain.build_block(proof, previous_block)
    response = { 'message': 'Block has been mined!',
                 'index': block['index'],
                 'datetime': block['datetime'],
                 'proof': block['proof'],
                 'previous_proof': block['previous_proof'],
                 'transactions': block['transactions']
                 }
    return jsonify(response), 200

#Get the chain
@app.route('/get_chain', methods = ['GET'])
def get_chain():
    response = {'chain': blockchain.chain,
                'lenght': len(blockchain.chain)}
    return jsonify(response), 200

#Check the validity
@app.route('/is_valid', methods = ['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {'message': 'Chain is valid'}
    else:
        response = {'message': 'Chain is not valid'}
    return jsonify(response), 200

# Make a transaction
@app.route('/add_transaction', methods = ['POST'])
def add_transaction():
    json = request.get_json()
    transaction_keys = ['sender', 'receiver', 'amount']
    if not all(key in json for key in transaction_keys):
        return 'Missing parts', 400
    index = blockchain.add_transactions(json['sender'], json['receiver'], json['amount'])
    response = {'message': 'message has been added to block{index}'}
    return jsonify(response),201

@app.route('/connect_nodes', methods = ['GET'])
def connect_nodes():
    json = request.get_json()
    nodes = json.get('nodes')
    if nodes is None:
        return 'Missing nodes', 400
    for node in nodes:
        blockchain.add_nodes(node)
    response = {'message': 'All nodes can be found here:',
                'total_nodes': list(blockchain.nodes)}
    return jsonify(response), 201

@app.route('/replaced_chain', methods = ['GET'])
def replaced_chain():
    replaced_chain = blockchain.replace_chain()
    if replaced_chain:
        response = {'message': 'Chain has changed:',
                    'actual_chain': blockchain.chain}
    else:
        response = {'message': 'Chain is the same:',
                    'new_chain': blockchain.chain}
    return jsonify(response), 200

#run app

app.run(host= '0.0.0.0', port= 5000)



        
    
    
    
                
                
                
        
    
        
    
        