from pydantic.main import BaseModel

from iwf.object_encoder import ObjectEncoder


class ClientOptions(BaseModel):
    server_url: str
    worker_url: str
    converter: ObjectEncoder


def localDefault() -> ClientOptions:
    return minimum(
        server_url="http://localhost:8801",
        worker_url="http://localhost:8802",
    )


def dockerDefault() -> ClientOptions:
    return minimum(
        server_url="http://localhost:8801",
        worker_url="http://host.docker.internal:8802",
    )


def minimum(
    worker_url: str,
    server_url: str,
) -> ClientOptions:
    return ClientOptions(
        server_url=server_url,
        worker_url=worker_url,
        object_encoder=ObjectEncoder.default,
    )
