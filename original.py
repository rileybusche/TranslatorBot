# Handles the persistence of the original translation by saving to a JSON file
import json
import os.path

file_name = "original.json"

# Save Json to file
def save(message_id:int, translation:str):
    data = {}
    if os.path.isfile(file_name):
        with open(file_name) as json_file:
            data = json.load(json_file)
        json_file.close()

    data[message_id] = translation
    with open(file_name, 'a') as outfile:
        json.dump(data, outfile)

    outfile.close()

# Get Translation from file
def get(message_id:int) -> str:
    with open(file_name) as json_file:
        data = json.load(json_file)
    json_file.close()

    return