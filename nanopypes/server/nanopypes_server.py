from flask import Flask, request, jsonify
from flask_cors import CORS
from nanopypes.api import *

app = Flask(__name__)
CORS(app)


@app.route('/')
def server_build_pipeline():
    config = request.json['config']
    # compute_config = request.json['compute_config']
    # input_path = request.json['input_path']
    # save_path = request.json['save_path']
    # pipe_configs = request.json['pipe_configs']
    pipeline, commands = build_pipeline(config)

    response = {
        'commands': commands,
        'pipeline': pipeline.serialize()
    }

    return jsonify(response)

@app.route('/compute-config')
def get_compute():
    data = get_config_data('compute')
    return data

@app.route('/pipes-config')
def get_pipes():
    data = get_config_data('pipe')
    return data

@app.route('/pipeline-config')
def get_pipeline():
    data = get_config_data('pipeline')
    return data



def get_config_data(id):
    import os

    path = os.path.dirname(os.path.abspath(__package__))
    config_type_handler = {'compute': os.path.join(path, "nanopypes", "configs", "compute.yml"),
                           'pipeline': os.path.join(path, "nanopypes", "configs", "pipelines", "local_pipeline.yml"),
                           'pipe': os.path.join(path, "nanopypes", "configs", "pipes.yml")}
    config_path = config_type_handler[id]
    import yaml
    with open(config_path, 'r') as file:
        data = yaml.safe_load(file)

    response = {
        'data': data
    }
    print(jsonify(response))
    return jsonify(response)

def start_backend_server():
    app.run(debug=True)

if __name__ == '__main__':
    start_backend_server()
