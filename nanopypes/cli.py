# -*- coding: utf-8 -*-
"""Console script for pai-nanopypes."""
import shutil
import os

import click

from nanopypes.utilities import PipelineConfiguration
from nanopypes.api import build_pipeline

@click.command(context_settings=dict(
    ignore_unknown_options=True,
))
@click.option('-i', '--input_path', help='Path to the input data')
@click.option('-pn', '--pipeline_name', help='Name of the pipeline- Will be used to find the correct config file if no config path is given')
@click.option('-pc', '--pipeline_config', help="Path to a pipeline config file", required=False)
@click.option('-cc', '--compute_config', help="Path to a compute config file", required=False)
@click.option('-cn', '--compute_name', help="Path to a compute config file", required=False)
@click.argument('pipeline_args', help="Arguments that are required by the pipeline that is being run.", nargs=-1, type=click.UNPROCESSED)
def run_pipeline(input_path, pipeline_name, pipeline_config, compute_config, pipeline_args):
    """An interface for running Nanopypes pipelines."""
    key, value = None, None
    keys = {}

    # odd pipeline_args are keys, evens are values
    for i in pipeline_args:
        if key is None:
            key = i.replace('-', '')
            continue
        elif key and value is None:
            value = i
        keys[key] = value
        key, value = None, None
    if pipeline_config is None:
        path = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(path, "configs", "pipelines", (pipeline_name + ".yml"))
    else:
        path = pipeline_config
    print("path: ", path)
    print("keys: ", keys)
    # config = PipelineConfiguration(path, keys)
    # pipeline_builder = build_pipeline(inputs, config)
    # pipeline_builder.run()


@click.command()
@click.option('-C', '--cluster-type', 'cluster_type', help='The type of cluster you plan to use for your analysis. ["lsf", "local]', required=True, type=str)
@click.option('-s', '--save-path', 'save_path', help='The number of batches to process at one time.', type=str)
def get_config_template(save_path, cluster_type):
    cluster_type = cluster_type.lower()
    template_name = "{}_albacore_template.yml".format(cluster_type)
    current_dir = os.path.dirname(os.path.abspath(__file__))

    template_path = current_dir.replace("/nanopypes", ("/configs/" + template_name))

    shutil.copy(template_path, save_path)
    print("saved template to " + save_path)
    return 0


#############################################
## Run Pipes
#############################################


@click.command()
@click.option('-p', '--ports', 'ports', help='')
def start_app(ports):
    import subprocess
    import os
    from nanopypes.server.nanopypes_server import start_backend_server
    cwd = os.getcwd()
    os.chdir('/Users/kevinfortier/Desktop/Nanopypes_client/nanopypes-app')
    subprocess.Popen(['npm', 'start'])
    os.chdir(cwd)
    start_backend_server()


