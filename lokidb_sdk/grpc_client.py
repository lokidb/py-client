from typing import List

import grpc

from .gen_grpc.spec_pb2 import (
    SetRequest,
    GetRequest,
    DelRequest,
    google_dot_protobuf_dot_empty__pb2
)
from .gen_grpc.spec_pb2_grpc import LokiDBServiceStub

Empty = google_dot_protobuf_dot_empty__pb2.Empty


class Client:
    def __init__(self, address: tuple, timeout):
        self._channel = grpc.insecure_channel(f'{address[0]}:{address[1]}')
        self._stub = LokiDBServiceStub(self._channel)

    def get(self, key: str) -> str:
        resp = self._stub.Get(GetRequest(key=key))
        return resp.value

    def set(self, key: str, value: str):
        self._stub.Set(SetRequest(key=key, value=value))

    def delete(self, key: str) -> bool:
        return self._stub.Del(DelRequest(key=key)).deleted

    def keys(self) -> List[str]:
        return self._stub.Keys(Empty()).keys

    def flush(self):
        self._stub.Flush(Empty())

    def close(self):
        self._channel.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
