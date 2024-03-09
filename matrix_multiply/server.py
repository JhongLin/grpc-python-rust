import grpc
from concurrent import futures
import matrix_multiply_pb2
import matrix_multiply_pb2_grpc


class MatrixOperationServicer(matrix_multiply_pb2_grpc.MatrixOperationServicer):
    def Multiply(self, request, context):
        matrix1_values, matrix1_width = request.matrix1_values, request.matrix1_width
        matrix2_values, matrix2_width = request.matrix2_values, request.matrix2_width
        result = self.matrix_multiply(
            matrix1_values, matrix1_width,
            matrix2_values, matrix2_width
        )

        return matrix_multiply_pb2.MatrixResponse(result_values=[value for row in result for value in row])

    def matrix_multiply(self, matrix1_values, matrix1_width, matrix2_values, matrix2_width):
        """
        Perform matrix multiplication of two square matrices.
        """
        matrix1, matrix2 = self._values_to_matrix(matrix1_values, matrix1_width), self._values_to_matrix(matrix2_values, matrix2_width)
        m, n = len(matrix1), len(matrix2[0])
        result = [[0] * n for _ in range(m)]

        for i in range(m):
            for j in range(n):
                for k in range(len(matrix1[0])):
                    result[i][j] += matrix1[i][k] * matrix2[k][j]

        return result

    @staticmethod
    def _values_to_matrix(values: list, width: int):
        return [values[i*width:(i+1)*width] for i in range(len(values) // width)]


if __name__ == '__main__':
    try:
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        matrix_multiply_pb2_grpc.add_MatrixOperationServicer_to_server(MatrixOperationServicer(), server)
        server.add_insecure_port('[::]:50051')
        server.start()
        server.wait_for_termination()

    except KeyboardInterrupt:
        server.stop(0)
