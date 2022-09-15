cd lokidb_sdk/gen_grpc
python -m grpc_tools.protoc -I ./ --python_out=. --grpc_python_out=. spec.proto

# After generation run 2to3 on the generated files
2to3 -w -n spec_pb2_grpc.py
