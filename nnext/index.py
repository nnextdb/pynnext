# #!/usr/bin/env python

__authors__ = ["Peter W. Njenga"]
__copyright__ = "Copyright 2021, NNext, Co."

import logging
from grpc._channel import _InactiveRpcError

from nnext.main_pb2 import VectorAddRequest, CreateIndexRequest, VectorSearchRequest, Datum, Vector, Index as IndexPB
from google.protobuf.json_format import MessageToJson, MessageToDict

class Index(object):
    def __init__(self, grpc_stub, name, d):
        self.grpc_stub = grpc_stub
        self.name = name
        self.d = d

    def search(self, query, k=5, return_metadata=True, return_vector=True, filters=None):
        print(query, query.shape)

        n, d = query.shape

        query_vector = []
        for datum in query:
            vector = Vector(rptd__element=datum)
            query_vector.append(vector)

        vsreq = VectorSearchRequest(
            index_name=self.name,
            k=k,
            rptd_query_vector=query_vector,
            omit_metadata=not return_metadata,
            omit_vector=not return_vector)

        vsres = self.grpc_stub.VectorSearch(vsreq)

        search_res = []
        for i in range(n):
            nnbors = []
            for j in range(k):
                nnbors.append(vsres.rptd__datum[i*k + j].id)
            search_res.append(nnbors)

        return search_res

    def get(self):
        return None

    def add(self, data):
        if self.d != data.shape[1]:
            raise ValueError(f"Input dimensions do not match. Got {data.shape} expected (n, {self.d})")

        data_vec = []

        vec_add_req = VectorAddRequest(index_name=self.name)

        max_GRPC_MSG_SIZE = 4194304

        print(data.shape[0])

        i = 0
        j = 0
        while i < data.shape[0]:
            while i < data.shape[0] and vec_add_req.ByteSize() <= max_GRPC_MSG_SIZE:
                _d = vec_add_req.data.add()
                d = data[i]
                i += 1
                _d.rptd__vector.extend(d)

            if vec_add_req.ByteSize() > max_GRPC_MSG_SIZE:
                del vec_add_req.data[-1]
                i -= 1

            print(f"Adding batch [{j}:{i}] size={vec_add_req.ByteSize()}")
            self.grpc_stub.VectorAdd(vec_add_req)

            j = i

            vec_add_req = VectorAddRequest(index_name=self.name)

        return

    def clear(self):
        return None

    def delete(self):
        return None


class IndexClient(object):

    def __init__(self, grpc_stub):
        self.grpc_stub = grpc_stub
        self.indices = {}

    def create(self, name : str, d: int) -> None:

        try:
            cir = CreateIndexRequest(name=name, dims=d)

            idx = self.grpc_stub.CreateIndex(cir)

            idx = Index(grpc_stub=self.grpc_stub, name=idx.name, d=idx.dims)

            self.indices[name] = idx

            return idx

        except _InactiveRpcError as ex:
            ex_msg = ex.details()
            ex_code = ex.code()
            err_dict = {"code": ex_code, "message": ex_msg}
        except Exception as ex:
            print(ex)

        raise Exception(f"{err_dict}")

    def delete(self, name : str) -> None:
        print(name, d)

        return None

    def __getitem__(self, name):
        if name in self.indices:
            return self.indices[name]
        else:
            try:
                get_idx_pb = IndexPB(name=name)

                idx = self.grpc_stub.GetIndex(get_idx_pb)

                idx = Index(grpc_stub=self.grpc_stub, name=idx.name, d=idx.dims)

                self.indices[name] = idx

                return idx

            except _InactiveRpcError as ex:
                ex_msg = ex.details()
                ex_code = ex.code()
                err_dict = {"code": ex_code, "message": ex_msg}

                return None
            except Exception as ex:
                print(ex)

            raise Exception(err_dict)





