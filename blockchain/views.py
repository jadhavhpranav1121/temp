from django.shortcuts import render
import datetime
import hashlib
import copy, os
import json
from uuid import uuid4
import socket
from urllib.parse import urlparse
from django.http import JsonResponse, HttpResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from django.core.files import File
import requests
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile

from crimechain.settings import MEDIA_URL


class Blockchain:
    def __init__(self, chain1=0):
        if chain1:
            self.chain = chain1["chain"]
        else:
            self.chain = []
            self.data = []
            self.create_block(nonce=1, previous_hash="0")
            self.nodes = set()

    def create_block(self, nonce, previous_hash):
        block = {
            "index": len(self.chain) + 1,
            "timestamp": str(datetime.datetime.now()),
            "nonce": nonce,
            "previous_hash": previous_hash,
            "data": self.data,
        }
        self.data = []
        self.chain.append(block)
        return block

    def create_block1(self, nonce, previous_hash, data, scale):
        dat = copy.deepcopy(data)
        dat[0]["crime_list"].append(scale)
        block = {
            "index": len(self.chain) + 1,
            "timestamp": str(datetime.datetime.now()),
            "nonce": nonce,
            "previous_hash": previous_hash,
            "data": dat,
        }
        # block['data'][0]['crime_list'].append(scale)
        self.chain.append(block)
        return block

    def get_last_block(self):
        return self.chain[-1]

    def proof_of_work(self, previous_nonce):
        new_nonce = 1
        check_nonce = False
        while check_nonce is False:
            hash_operation = hashlib.sha256(str(new_nonce**2 - previous_nonce**2).encode()).hexdigest()
            if hash_operation[:4] == "0000":
                check_nonce = True
            else:
                new_nonce += 1
        return new_nonce

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block["previous_hash"] != self.hash(previous_block):
                return False
            previous_nonce = previous_block["nonce"]
            nonce = block["nonce"]
            hash_operation = hashlib.sha256(str(nonce**2 - previous_nonce**2).encode()).hexdigest()
            if hash_operation[:4] != "0000":
                return False
            previous_block = block
            block_index += 1
        return True

    def add_transaction(self, id, name, dob, nationality, location, financial_status, crime_scale):
        flag = False

        for i in range(int(1), int(len(blockchain.chain))):
            d = blockchain.chain[i]["data"]
            e = blockchain.chain[i]
            if int(len(d)) > 0 and d[0]["name"] == name:
                flag = True
                return (-1, e)

        if flag == False:
            self.data.append(
                {
                    "id": id,
                    "name": name,
                    "dob": dob,
                    "nationality": nationality,
                    "location": location,
                    "financial_status": financial_status,
                    "crime_list": [crime_scale],
                    "time": str(datetime.datetime.now()),
                }
            )

        previous_block = self.get_last_block()
        if flag == False:
            return (previous_block["index"] + 1, {})

    def add_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def replace_chain(self):
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)
        for node in network:
            response = requests.get(f"http://{node}/get_chain")
            if response.status_code == 200:
                length = response.json()["length"]
                chain = response.json()["chain"]
                if length > max_length and self.is_chain_valid(chain):
                    max_length = length
                    longest_chain = chain
        if longest_chain:
            self.chain = longest_chain
            return True
        return False


# Creating our Blockchain
blockchain = Blockchain()
# Creating an address for the node running our server
node_address = str(uuid4()).replace("-", "")
root_node = "e36f0158f0aed45b3bc755dc52ed4560d"


# Mining a new block
def mine_block(request):
    if request.method == "GET":
        received_json = json.loads(request.body)
        a = blockchain.add_transaction(
            id=received_json["id"],
            name=received_json["name"],
            dob=received_json["dob"],
            nationality=received_json["nationality"],
            location=received_json["location"],
            financial_status=received_json["financial_status"],
            crime_scale=received_json["crime_scale"],
        )
        previous_block = blockchain.get_last_block()
        previous_nonce = previous_block["nonce"]
        nonce = blockchain.proof_of_work(previous_nonce)
        previous_hash = blockchain.hash(previous_block)
        if a[0] == -1:
            block = blockchain.create_block1(nonce, previous_hash, a[1]["data"], received_json["crime_scale"])
        else:
            block = blockchain.create_block(nonce, previous_hash)
        response = {
            "message": "Congratulations, you just mined a block!",
            "index": block["index"],
            "timestamp": block["timestamp"],
            "nonce": block["nonce"],
            "previous_hash": block["previous_hash"],
            "data": block["data"],
        }
        try:
            # os.remove(os.path.join(MEDIA_URL, "main.json"))
            os.remove("media/main.json")
            print(os.path.join(MEDIA_URL, "main.json"))

        except:
            print("pass")
            print(os.path.join(MEDIA_URL, "main.json"))
            pass
        # path = default_storage.save("./fs.txt", ContentFile(b"Hello"))
        # default_storage.open(path).read()
        fs = FileSystemStorage()
        file = fs.save(
            "main.json", ContentFile(json.dumps({"chain": blockchain.chain, "length": len(blockchain.chain)}))
        )
        data = json.loads(json.dumps({"chain": blockchain.chain, "length": len(blockchain.chain)}))

        return JsonResponse(response)
        # else:
        #     response={}
        #     return JsonResponse(response)


# Getting the full Blockchain


def get_chain(request):
    file = open("media/main.json", "r")
    chain1 = json.loads(file.read())
    blockchain.chain = chain1["chain"]
    if request.method == "GET":
        response = {"chain": blockchain.chain, "length": len(blockchain.chain)}
    convertToCSV()
    return JsonResponse(response)


# Checking if the Blockchain is valid
def is_valid(request):
    if request.method == "GET":
        is_valid = blockchain.is_chain_valid(blockchain.chain)
        if is_valid:
            response = {"message": "All good. The Blockchain is valid."}
        else:
            response = {"message": "Houston, we have a problem. The Blockchain is not valid."}
    return JsonResponse(response)


# Adding a new transaction to the Blockchain
@csrf_exempt
def add_transaction(request):
    if request.method == "POST":
        received_json = json.loads(request.body)
        transaction_keys = ["sender", "receiver", "amount", "time"]
        if not all(key in received_json for key in transaction_keys):
            return "Some elements of the transaction are missing", HttpResponse(status=400)

        index = blockchain.add_transaction(
            received_json["id"],
            received_json["name"],
            received_json["dob"],
            received_json["nationality"],
            received_json["location"],
            received_json["financial_status"],
            received_json["crime_list"],
            received_json["time"],
        )
        response = {"message": f"This transaction will be added to Block {index}"}
    return JsonResponse(response)


# Connecting new nodes
@csrf_exempt
def connect_node(request):
    if request.method == "POST":
        received_json = json.loads(request.body)
        nodes = received_json.get("nodes")
        if nodes is None:
            return "No node", HttpResponse(status=400)
        for node in nodes:
            blockchain.add_node(node)
        response = {
            "message": "All the nodes are now connected. The Sudocoin Blockchain now contains the following nodes:",
            "total_nodes": list(blockchain.nodes),
        }
    return JsonResponse(response)


# Replacing the chain by the longest chain if needed
def replace_chain(request):
    if request.method == "GET":
        is_chain_replaced = blockchain.replace_chain()
        if is_chain_replaced:
            response = {
                "message": "The nodes had different chains so the chain was replaced by the longest one.",
                "new_chain": blockchain.chain,
            }
        else:
            response = {"message": "All good. The chain is the largest one.", "actual_chain": blockchain.chain}
    return JsonResponse(response)


def convertToCSV():
    chain2 = blockchain.chain
    l = len(chain2)
    d = {}
    list1 = []
    for i in range(l - 1, 0, -1):
        temp = chain2[i]["data"][0]["name"]
        val = d.get(temp, 0)
        # print(val)
        # if val <= 1:
        #     list1.append(chain2[i]["data"][0])
        #     d[temp] += 1
    print(list1)
