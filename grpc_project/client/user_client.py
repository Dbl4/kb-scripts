import grpc
from grpc_project.generated import user_pb2, user_pb2_grpc


def main():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = user_pb2_grpc.UserServiceStub(channel)

        response = stub.GetUser(
            user_pb2.GetUserRequest(user_id=1)
        )

        print(response)


if __name__ == "__main__":
    main()
