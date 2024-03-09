import grpc
import timeit
import matrix_multiply_pb2
import matrix_multiply_pb2_grpc


def matrix_multiply(
        matrix1_values,
        matrix1_width,
        matrix2_values,
        matrix2_width,
    ):
    """
    Perform matrix multiplication of two square matrices.
    """
    matrix1, matrix2 = values_to_matrix(matrix1_values, matrix1_width), values_to_matrix(matrix2_values, matrix2_width)
    m, n = len(matrix1), len(matrix2[0])
    result = [[0] * n for _ in range(m)]

    for i in range(m):
        for j in range(n):
            for k in range(len(matrix1[0])):
                result[i][j] += matrix1[i][k] * matrix2[k][j]

    return result


def values_to_matrix(values: list, width: int):
    return [values[i*width:(i+1)*width] for i in range(len(values) // width)]


def matrix_multiply_on_python_server(
        matrix1_values,
        matrix1_height,
        matrix1_width,
        matrix2_values,
        matrix2_height,
        matrix2_width,
    ):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = matrix_multiply_pb2_grpc.MatrixOperationStub(channel)
        request = matrix_multiply_pb2.MatrixRequest(
            matrix1_values=matrix1_values,
            matrix1_height=matrix1_height,
            matrix1_width=matrix1_width,
            matrix2_values=matrix2_values,
            matrix2_height=matrix2_height,
            matrix2_width=matrix2_width,
            )
        response = stub.Multiply(request)
        result = values_to_matrix(response.result_values, matrix1_width)

        return result


def matrix_multiply_on_rust_server(
        matrix1_values,
        matrix1_height,
        matrix1_width,
        matrix2_values,
        matrix2_height,
        matrix2_width,
    ):
    with grpc.insecure_channel('localhost:50052') as channel:
        stub = matrix_multiply_pb2_grpc.MatrixOperationStub(channel)
        request = matrix_multiply_pb2.MatrixRequest(
            matrix1_values=matrix1_values,
            matrix1_height=matrix1_height,
            matrix1_width=matrix1_width,
            matrix2_values=matrix2_values,
            matrix2_height=matrix2_height,
            matrix2_width=matrix2_width,
            )
        response = stub.Multiply(request)
        result = values_to_matrix(response.result_values, matrix1_width)

        return result


def generate_matrices(n):
    """
    Generate two square matrices of size (n * n) with the specified pattern.
    """
    return [i for i in range(1, n * n + 1)], [i for i in range(n, -1 * n * n + n, -1)]


if __name__ == "__main__":
    matrix_size = 300
    repetitions = 10

    # Generate matrices
    matrix1_values, matrix2_values = generate_matrices(matrix_size)

    # Measure runtime of internal function calls
    execution_times = timeit.repeat(lambda: matrix_multiply(matrix1_values, matrix_size, matrix2_values, matrix_size), number=1, repeat=repetitions)
    average_runtime = sum(execution_times) / repetitions

    print(f"Average runtime of internal function call: {average_runtime:.6f} seconds")

    # Measure runtime of using gRPC on Python
    execution_times = timeit.repeat(lambda: matrix_multiply_on_python_server(matrix1_values, matrix_size, matrix_size, matrix2_values, matrix_size, matrix_size), number=1, repeat=repetitions)
    average_runtime = sum(execution_times) / repetitions

    print(f"Average runtime of using gRPC on Python: {average_runtime:.6f} seconds")

    # Measure runtime of using gRPC on Rust
    execution_times = timeit.repeat(lambda: matrix_multiply_on_rust_server(matrix1_values, matrix_size, matrix_size, matrix2_values, matrix_size, matrix_size), number=1, repeat=repetitions)
    average_runtime = sum(execution_times) / repetitions

    print(f"Average runtime of using gRPC on Rust: {average_runtime:.6f} seconds")
