# python-api-example

Simple example repo on how to build a python api using Flask

## API creation steps

- initialize a virtual environment, in this case `pipenv` with `pipenv install`
- add `flask` and `flask-cors` to the environment (`pipenv install flask flask-cors`)
- create the api folder, in my case `python_api`, and make sure to add an `__init__.py` file inside.
- add a `main.py` file, in which I will put all my apis
- initialize `main.py` with by importing all the necessary flask packages, in my case I usually add a `sys.path.append` statement to allow running the api from any folder by running `python [some-folder]/python-api-example/python_api/main.py`. Initialize the flask app and add the cors extension to it to avoid cross-origin issues when working with localhost. Add the startup instructions in the `if __name__ == "__main__":` section

```python
import sys
from pathlib import Path

import flask
from flask import Flask, Response, jsonify
from flask_cors import CORS

sys.path.append(str(Path(__file__).resolve().parents[1])) # allows running the api from anywhere

app = Flask(__name__) # flask app creation
CORS(app) # cors patch to allow working with localhost

def main():
    pass # put all your initialization here

if __name__ == "__main__":
    main() # initialize the app (logging, folders etc.)
    app.run(host="0.0.0.0", port=5999) # run the api on localhost on port 5999
```

- run the project with `pipenv shell` + `python [path-to-main]/main.py` and make sure you get something like

```python
 * Serving Flask app "main" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://0.0.0.0:5999/ (Press CTRL+C to quit)
```

- add some logic to the project, in this case we can have the api work as a phonebook. The phonebook will be a dictionary that contains names as keys with their phone number as values

```python
phonebook = {
    "John": "657-532-1112"
}
```

- in order to have flask access the phonebook from the apis, we are going to initialize an empty phonebook after the app initialization, and in main we will add the example entry.

```python
...
CORS(app) # cors patch to allow working with localhost

phonebook = {}

def main():
    phonebook["John"] = "657-532-1112"

...
```

- we will add a `GET` endpoint to retrieve the phonebook, accessed as `GET /phonebook`.

```python
@app.route("/phonebook", methods=["GET"]) # api endpoint, and allowed methods on it
def api_get_phonebook():
    payload = {
        'phonebook': phonebook
    }

    return jsonify(payload), 200 # returned payload and status code
```

- run the api, send a `GET` request to the new endpoint and you should get

```bash
>curl --get http://localhost:5999/phonebook
{"phonebook":{"John":"657-532-1112"}}
```

- we will add a `POST` endpoint to add elements to the phonebook. The user will provide a `name` and `phone_number` as body values, we will parse and add them to the phonebook

```python
@app.route("/phonebook", methods=["POST"]) # api endpoint, and allowed methods on it
def api_add_to_phonebook():
    name = flask.request.form.get('name')
    phone_number = flask.request.form.get('phone_number')

    if name is None or phone_number is None: # make sure they are defined, otherwise return a 400 error
        return jsonify({'error':'please provide a `name` and a `phone_number` field'}), 400

    print(f"adding {name} and {phone_number} to phonebook")
    phonebook[name] = phone_number

    return jsonify({}), 200 # returned payload and status code
```

- test the new api endpoint by sending a `POST` request

```bash
>curl --location --request POST 'http://localhost:5999/phonebook' --header 'Content-Type: application/x-www-form-urlencoded' --data-urlencode 'name=Tom' --data-urlencode 'phone_number=111-222-2222'
{}
```

- test with a bad payload

```bash
>curl --location --request POST 'http://localhost:5999/phonebook' --header 'Content-Type: application/x-www-form-urlencoded' --data-urlencode 'name=Tom'
{"error":"please provide a `name` and a `phone_number` field"}
```

These are the basics on how to create a simple python api!
