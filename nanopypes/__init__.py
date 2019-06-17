# -*- coding: utf-8 -*-

"""Top-level package for NanoPypes."""

__author__ = """Kevin Fortier"""
__email__ = 'kevin.r.fortier@gmail.com'
__version__ = '0.1.0'

import logging

from .compute import ClusterManager
from .pipelines.pipeline import Pipeline
from .utilities import CommandBuilder


logging.getLogger(__name__).addHandler(logging.NullHandler())
