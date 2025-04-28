from dataclasses import dataclass


@dataclass
class PersistenceOptions:
    enable_caching: bool

    @classmethod
    def get_default(cls):
        return PersistenceOptions(False)
