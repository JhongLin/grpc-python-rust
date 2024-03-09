use tonic::{transport::Server, Request, Response, Status};

use matrix_operation::matrix_operation_server::{MatrixOperation, MatrixOperationServer};
use matrix_operation::{MatrixResponse, MatrixRequest};

pub mod matrix_operation {
    tonic::include_proto!("matrix"); // The string specified here must match the proto package name
}

#[derive(Debug, Default)]
pub struct MyMatrixOperation {}

#[tonic::async_trait]
impl MatrixOperation for MyMatrixOperation {
    async fn multiply(
        &self,
        request: Request<MatrixRequest>, // Accept request of type HelloRequest
    ) -> Result<Response<MatrixResponse>, Status> { // Return an instance of type HelloReply
        //println!("Got a request: {:?}", request);
        let request = request.into_inner();
        let matrix1 = parse_matrix(&request.matrix1_values, request.matrix1_width as usize);
        let matrix2 = parse_matrix(&request.matrix2_values, request.matrix2_width as usize);

        let result_matrix = matrix_multiply(&matrix1, &matrix2);

        let result_values: Vec<i64> = result_matrix.iter().cloned().collect();

        let response = matrix_operation::MatrixResponse {
            result_values,
        };

        Ok(Response::new(response)) // Send back our formatted greeting
    }
}

fn parse_matrix(values: &[i64], width: usize) -> Vec<Vec<i64>> {
    values.chunks(width).map(|chunk| chunk.to_vec()).collect()
}

fn matrix_multiply(matrix1: &[Vec<i64>], matrix2: &[Vec<i64>]) -> Vec<i64> {
    let mut result = vec![0; matrix1.len() * matrix2[0].len()];
    for i in 0..matrix1.len() {
        for j in 0..matrix2[0].len() {
            for k in 0..matrix1[0].len() {
                result[i * matrix2[0].len() + j] += matrix1[i][k] * matrix2[k][j];
            }
        }
    }
    result
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let addr = "[::1]:50052".parse()?;
    let matrix_operation = MyMatrixOperation::default();

    Server::builder()
        .add_service(MatrixOperationServer::new(matrix_operation))
        .serve(addr)
        .await?;

    Ok(())
}
