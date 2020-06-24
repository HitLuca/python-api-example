import sys
from pathlib import Path

import flask
from flask import Flask, Response, jsonify
from flask_cors import CORS

sys.path.append(str(Path(__file__).resolve().parents[1])) # allows running the api from anywhere

app = Flask(__name__) # flask app creation
CORS(app) # cors patch to allow working with localhost

phonebook = {}

@app.route("/phonebook", methods=["GET"]) # api endpoint, and allowed methods on it
def api_get_phonebook():
    payload = {
        'phonebook': phonebook
    }

    return jsonify(payload), 200 # returned payload and status code

@app.route("/phonebook", methods=["POST"]) # api endpoint, and allowed methods on it
def api_add_to_phonebook():
    name = flask.request.form.get('name')
    phone_number = flask.request.form.get('phone_number')

    if name is None or phone_number is None: # make sure they are defined, otherwise return a 400 error
        return jsonify({'error':'please provide a `name` and a `phone_number` field'}), 400

    print(f"adding {name} and {phone_number} to phonebook")
    phonebook[name] = phone_number

    return jsonify({}), 200 # returned payload and status code


def main():
    phonebook["John"] = "657-532-1112"

if __name__ == "__main__":
    main() # initialize the app (logging, folders etc.)
    app.run(host="0.0.0.0", port=5999) # run the api on localhost on port 5999