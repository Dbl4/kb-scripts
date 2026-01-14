## grpc_project

👉 Важно:
````
proto/ — контракт (API)

generated/ — автосгенерированный код (не трогаем руками)

services/ — бизнес-логика

server.py — сборка и запуск сервера
````

generated:

`python -m grpc_tools.protoc \
-I proto \
--python_out=generated \
--grpc_python_out=generated \
proto/user.proto`

