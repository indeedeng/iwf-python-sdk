from dataclasses import dataclass

from iwf.object_encoder import ObjectEncoder


@dataclass
class ClientOptions:
    server_url: str
    worker_url: str
    object_encoder: ObjectEncoder
    api_timeout: int = 60

    @classmethod
    def local_default(cls):
        return ClientOptions(
            server_url="http://localhost:8801",
            worker_url="http://localhost:8802",
            object_encoder=ObjectEncoder.default,
        )
