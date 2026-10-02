from concurrent.futures import ThreadPoolExecutor
from threading import Barrier

import pytest

from iwf.communication import Communication
from iwf.communication_schema import CommunicationMethod
from iwf.errors import WorkflowDefinitionError
from iwf.object_encoder import ObjectEncoder
from iwf.type_store import Type, TypeStore


def make_communication(encoder):
    store = TypeStore(Type.INTERNAL_CHANNEL)
    store.add_internal_channel_def(
        CommunicationMethod.internal_channel_def("events", int)
    )
    return Communication(store, {}, encoder, None, None)


def test_concurrent_first_publications_are_retained():
    barrier = Barrier(2)

    class ConcurrentEncoder(ObjectEncoder):
        def encode(self, value):
            barrier.wait(timeout=5)
            return super().encode(value)

    communication = make_communication(ConcurrentEncoder())
    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = [
            executor.submit(communication.publish_to_internal_channel, "events", value)
            for value in (1, 2)
        ]
        for future in futures:
            future.result(timeout=10)

    publications = communication.get_to_publishing_internal_channel()
    assert len(publications) == 2
    assert all(publication.channel_name == "events" for publication in publications)
    encoder = ObjectEncoder()
    assert sorted(
        encoder.decode(publication.value, int) for publication in publications
    ) == [1, 2]
    assert communication.get_internal_channel_size("events") == 2


def test_sequential_publications_preserve_order():
    encoder = ObjectEncoder()
    communication = make_communication(encoder)
    for value in (3, 1, 2):
        communication.publish_to_internal_channel("events", value)
    assert [
        encoder.decode(publication.value, int)
        for publication in communication.get_to_publishing_internal_channel()
    ] == [3, 1, 2]


@pytest.mark.parametrize("channel,value", [("missing", 1), ("events", "invalid")])
def test_invalid_publications_do_not_change_buffer(channel, value):
    communication = make_communication(ObjectEncoder())
    with pytest.raises(WorkflowDefinitionError):
        communication.publish_to_internal_channel(channel, value)
    assert communication.get_to_publishing_internal_channel() == []
