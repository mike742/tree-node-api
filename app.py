from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from flask_cors import CORS
import csv
import json

app = Flask(__name__)
CORS(app, resources={r"/nodes/*": {"origins": "*"}})
app.config['MONGO_DBNAME'] = 'test'
app.config['MONGO_URI'] = 'mongodb+srv://adcore:adcore@cluster0.agwmf.mongodb.net/test?retryWrites=true&w=majority'


mongo = PyMongo(app)


@app.route('/nodes', methods=['GET'])
def get_tree():
    nodes = mongo.db.tree_node

    return jsonify([
        {"id": node["_id"], "name": node["name"], "description": node["description"],
         "read_only": node["read_only"], "parent": node["parent"]}
        for node in nodes.find({})
    ])


@app.route('/nodes/<id>', methods=['GET'])
def get_node(id):
    nodes = mongo.db.tree_node
    node = nodes.find_one({'_id': int(id)})

    if node:
        output = {"id": node["_id"], "name": node["name"], "description": node["description"],
                  "read_only": node["read_only"], "parent": node["parent"]}
    else:
        output = "No node with id " + id + " is found"

    return output


@app.route('/nodes', methods=['POST'])
def create_node():

    nodes = mongo.db.tree_node
    content = request.get_json(force=True)
    parent = content["parent"]
    node = content["node"]

    new_id = nodes.insert(
        {"_id": int(node["id"]), "name": node["name"], "description": node["description"],
         "read_only": int(node["read_only"]), "parent": int(parent)})

    return str(new_id)


@app.route('/nodes/<id>', methods=['PUT'])
def update_node(id):
    node = mongo.db.tree_node.find_one({'_id': int(id)})

    if node['read_only'] == 0:
        content = request.get_json(force=True)
        name = content["name"]

        mongo.db.tree_node.update_one(
            {"_id": int(id)}, {"$set": {"name": name}})
    else:
        return "read only"

    return "success"


@app.route('/nodes/<id>', methods=['DELETE'])
def delete_node(id):
    try:
        mongo.db.tree_node.delete_one({"_id": int(id)})
        return "has been deleted"
    except:
        return "Something wrong"


"""
{
    "parent": 2,
    "node": {
        "id": 1,
        "name": "test",	
        "description": "test desc",	
        "read_only": 0
    }
}
"""


def make_json(csvFilePath, jsonFilePath):

    data = []

    with open(csvFilePath, encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf, delimiter="\t")

        for rows in csvReader:
            data.append(rows)

    with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
        jsonf.write(json.dumps(data))


csvFilePath = r'assets/tree_data.csv'
jsonFilePath = r'tree_data.json'

make_json(csvFilePath, jsonFilePath)

if mongo.db.tree_node.count_documents({}) == 0:
    file = open(jsonFilePath)
    list = []
    data = json.load(file)

    for row in data:
        post = {"_id": int(row["id"]), "name": row["name"], "description": row["description"],
                "read_only": int(row["read_only"]), "parent": int(row["parent"])}

        list.append(post)

    file.close()

    mongo.db.tree_node.insert_many(list)


if __name__ == "__main__":
    app.run(debug=True)
