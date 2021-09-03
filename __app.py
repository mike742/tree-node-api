import csv
import json
import pymongo


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
