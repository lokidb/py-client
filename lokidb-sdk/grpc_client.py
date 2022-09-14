from typing import List

import grpc

from gen_grpc.spec_pb2 import (
    SetRequest,
    GetRequest,
    DelRequest,
)
from gen_grpc.spec_pb2_grpc import LokiDBServiceStub


class Client:
    def __init__(self, address: tuple, timeout):
        self.channel = grpc.insecure_channel(f'{address[0]}:{address[1]}')
        self.stub = LokiDBServiceStub(self.channel)

    def get(self, key: str) -> str:
        resp = self.stub.Get(GetRequest(key=key))
        return resp.value

    def set(self, key: str, value: str):
        self.stub.Set(SetRequest(key=key, value=value))

    def delete(self, key: str) -> bool:
        return self.stub.Del(DelRequest(key=key)).deleted

    def keys(self) -> List[str]:
        return self.stub.Keys().keys

    def flush(self):
        self.stub.Flush()

    def close(self):
        self.channel.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
