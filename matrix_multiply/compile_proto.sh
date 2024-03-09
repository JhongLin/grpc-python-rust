#!/usr/bin/bash

../venv/bin/python -m grpc_tools.protoc -I ./proto --python_out=. --grpc_python_out=. ./proto/matrix_multiply.proto
