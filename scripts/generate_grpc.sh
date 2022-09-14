cd lokidb-sdk/gen_grpc
python -m grpc_tools.protoc -I ./ --python_out=. --grpc_python_out=. ./spec.proto