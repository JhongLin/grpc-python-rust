import grpc
import helloworld_pb2
import helloworld_pb2_grpc


def say_hello_to_rust_server(name: str):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = helloworld_pb2_grpc.GreeterStub(channel)
        request = helloworld_pb2.HelloRequest(name=name)
        response = stub.SayHello(request)

        return response


if __name__ == "__main__":
    name = input('Enter your name: ')
    print(say_hello_to_rust_server(name).message)
