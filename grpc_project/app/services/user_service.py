from grpc_project.generated import user_pb2, user_pb2_grpc


class UserService(user_pb2_grpc.UserServiceServicer):
    def GetUser(self, request, context):
        # здесь может быть БД, кеш, внешние сервисы
        return user_pb2.UserResponse(
            id=request.user_id,
            name="Ivan",
            email="ivan@example.com",
        )
