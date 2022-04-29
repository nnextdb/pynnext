# #!/usr/bin/env python

__authors__ = ["Peter W. Njenga"]
__copyright__ = "Copyright 2021, NNext, Co."

import logging
import string
import random

import grpc

from nnext.main_pb2 import VectorAddRequest
from nnext.main_pb2_grpc import NNextStub

class Client(object):
    def __init__(self, config_dict):

        with grpc.insecure_channel(target='localhost:6040',
                                   options=[('grpc.lb_policy_name', 'pick_first'),
                                            ('grpc.enable_retries', 0),
                                            ('grpc.keepalive_timeout_ms', 10000)
                                            ]) as channel:
            stub = NNextStub(channel)
