# -*- coding: utf-8 -*-
"""Console script for pai-nanopypes."""
import shutil
import os
import yaml
from pathlib import Path

import click

from distributed import LocalCluster, Client

from .compute import ClusterManager
from .pipes.basecaller import AlbacoreBasecaller
from nanopypes.utilities import Configuration
from nanopypes.api import build_pipeline

@click.command(context_settings=dict(
    ignore_unknown_options=True,
))
@click.option('-v', '--verbose', is_flag=True, help='Enables verbose mode')
@click.option('-n', '--name')
@click.argument('pipeline_args', nargs=-1, type=click.UNPROCESSED)
def run_pipeline(verbose, name, pipeline_args):
    """A fake wrapper around Python's timeit."""
    key, value = None, None
    keys = {}
    for i in pipeline_args:
        if key is None:
            key = i.replace('-', '')
            continue
        elif key and value is None:
            value = i
        keys[key] = value
        key, value = None, None

    path = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(path, "configs", "pipelines", (name+".yml"))
    config = Configuration(path, keys)
    pipeline_builder = build_pipeline(config)
    pipeline_builder.run()


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


