from typing import List
from hashlib import sha1

import grpc

from .gen_grpc.spec_pb2 import (
    SetRequest,
    GetRequest,
    DelRequest,
    google_dot_protobuf_dot_empty__pb2
)
from .gen_grpc.spec_pb2_grpc import LokiDBServiceStub

Empty = google_dot_protobuf_dot_empty__pb2.Empty

V_BUCKETS = 1024
HASH_USE_LENGTH = 4


class Client:
    def __init__(self, nodes_address: List[tuple]):
        self._v_buckets = []
        for v_bucket_index in range(V_BUCKETS):
            distances = []

            for address in nodes_address:
                if address[0] == "localhost":
                    address = ("127.0.0.1", address[1])

                has = int.from_bytes(sha1(f'{address[0]}:{address[1]}'.encode()).digest()[:HASH_USE_LENGTH], 'big')
                mod = ((v_bucket_index+1)*V_BUCKETS)
                dis = has % mod
                distances.append(dis)

            node_index = distances.index(min(distances))
            self._v_buckets.append(nodes_address[node_index])

        self._nodes = {}
        for address in nodes_address:
            channel = grpc.insecure_channel(f'{address[0]}:{address[1]}')
            stub = LokiDBServiceStub(channel)
            self._nodes[address] = {"channel": channel, 'stub': stub}

    def _node_by_key(self, key: str):
        hash_bytes = sha1(key.encode()).digest()[:HASH_USE_LENGTH]
        num = int.from_bytes(hash_bytes, 'big')
        node_id = self._v_buckets[num % V_BUCKETS]
        return self._nodes[node_id]['stub']

    def get(self, key: str) -> str:
        node = self._node_by_key(key)
        resp = node.Get(GetRequest(key=key))
        return resp.value

    def set(self, key: str, value: str):
        node = self._node_by_key(key)
        node.Set(SetRequest(key=key, value=value))

    def delete(self, key: str) -> bool:
        node = self._node_by_key(key)
        return node.Del(DelRequest(key=key)).deleted

    def keys(self) -> List[str]:
        keys = []
        for node_dict in self._nodes.values():
            node = node_dict['stub']
            keys.extend(node.Keys(Empty()).keys)
        return keys

    def flush(self):
        for node_dict in self._nodes.values():
            node = node_dict['stub']
            node.Flush(Empty())

    def close(self):
        for node_dict in self._nodes.values():
            channel = node_dict['channel']
            channel.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
