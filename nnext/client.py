# #!/usr/bin/env python

__authors__ = ["Peter W. Njenga"]
__copyright__ = "Copyright 2021, NNext, Co."

import grpc
import logging
import random
import string

from nnext.index import IndexClient
from nnext.main_pb2 import VectorAddRequest
from nnext.main_pb2_grpc import NNextStub


class Client(object):

    def __init__(self, nodes):
        chan_opts = [
            ('grpc.lb_policy_name', 'pick_first'),
            ('grpc.enable_retries', 0),
            ('grpc.keepalive_timeout_ms', 10000)
        ]

        node = nodes[0]
        target = f"{node['host']}:{node['port']}"
        print(target)
        self.channel = grpc.insecure_channel(
            target=target, options=chan_opts)
        stub = NNextStub(self.channel)

        self.index = IndexClient(grpc_stub=stub)
