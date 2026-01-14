from concurrent import futures
import grpc

from grpc_project.generated import user_pb2_grpc
from services.user_service import UserService


def create_server() -> grpc.Server:
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10),
        interceptors=[],  # auth, logging, metrics
    )

    user_pb2_grpc.add_UserServiceServicer_to_server(
        UserService(),
        server,
    )

    server.add_insecure_port("[::]:50051")
    return server


if __name__ == "__main__":
    server = create_server()
    server.start()
    print("gRPC server started on :50051")
    server.wait_for_termination()
