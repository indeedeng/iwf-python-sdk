import inspect
import time
import unittest

from iwf.client import Client
from iwf.command_request import CommandRequest, TimerCommand
from iwf.command_results import CommandResults
from iwf.communication import Communication
from iwf.communication_schema import CommunicationSchema, CommunicationMethod
from iwf.iwf_api.models import SearchAttributeValueType
from iwf.persistence import Persistence
from iwf.persistence_schema import PersistenceField, PersistenceSchema
from iwf.state_decision import StateDecision
from iwf.state_schema import StateSchema
from iwf.tests.worker_server import registry
from iwf.workflow import ObjectWorkflow
from iwf.workflow_context import WorkflowContext
from iwf.workflow_state import T, WorkflowState
from iwf.rpc import rpc

test_internal_channel = "test-1"

sa_keyword_key = "CustomKeywordField"
sa_text_key = "CustomTextField"
sa_double_key = "CustomDoubleField"
sa_int_key = "CustomIntField"
sa_bool_key = "CustomBoolField"
sa_datetime_key = "CustomDatetimeField"
sa_keyword_array_key = "CustomKeywordArrayField"

sa_keyword: str = "keyword"
sa_text: str = "text"
sa_double: float = 2.34
sa_int: int = 234
sa_datetime: str = "2024-11-12T16:00:01.731455544-08:00"
sa_keyword_array: list[str] = ["keyword-1", "keyword-2"]

final_sa_keyword: str = "final_keyword"
final_sa_text = None
final_sa_int: int = 567
final_sa_bool: bool = False
final_sa_datetime: str = "2024-12-13T16:00:01.731455544-08:00"
final_sa_keyword_array: list[str] = ["final_keyword-1", "final_keyword-2"]

class SearchAttributeState(WorkflowState[None]):
    def wait_until(
        self,
        ctx: WorkflowContext,
        input: T,
        persistence: Persistence,
        communication: Communication,
    ) -> CommandRequest:
        return CommandRequest.for_all_command_completed(
            TimerCommand.by_seconds(10),
        )

    def execute(
        self,
        ctx: WorkflowContext,
        input: T,
        command_results: CommandResults,
        persistence: Persistence,
        communication: Communication,
    ) -> StateDecision:
        persistence.set_search_attribute_keyword(sa_keyword_key, final_sa_keyword)
        persistence.set_search_attribute_text(sa_text_key, final_sa_text)
        persistence.set_search_attribute_int64(sa_int_key, final_sa_int)
        persistence.set_search_attribute_boolean(sa_bool_key, final_sa_bool)
        persistence.set_search_attribute_datetime(sa_datetime_key, final_sa_datetime)
        persistence.set_search_attribute_keyword_array(
            sa_keyword_array_key, final_sa_keyword_array
        )
        return StateDecision.graceful_complete_workflow()


class PersistenceSearchAttributesWorkflow(ObjectWorkflow):
    def get_communication_schema(self) -> CommunicationSchema:
        return CommunicationSchema.create(
            CommunicationMethod.internal_channel_def(test_internal_channel, int),
        )

    def get_workflow_states(self) -> StateSchema:
        return StateSchema.with_starting_state(
            SearchAttributeState()
        )

    def get_persistence_schema(self) -> PersistenceSchema:
        return PersistenceSchema.create(
            PersistenceField.search_attribute_def(
                sa_keyword_key, SearchAttributeValueType.KEYWORD
            ),
            PersistenceField.search_attribute_def(
                sa_text_key, SearchAttributeValueType.TEXT
            ),
            PersistenceField.search_attribute_def(
                sa_double_key, SearchAttributeValueType.DOUBLE
            ),
            PersistenceField.search_attribute_def(
                sa_int_key, SearchAttributeValueType.INT
            ),
            PersistenceField.search_attribute_def(
                sa_bool_key, SearchAttributeValueType.BOOL
            ),
            PersistenceField.search_attribute_def(
                sa_datetime_key, SearchAttributeValueType.DATETIME
            ),
            PersistenceField.search_attribute_def(
                sa_keyword_array_key, SearchAttributeValueType.KEYWORD_ARRAY
            ),
        )

    @rpc()
    def test_persistence_set_search_attribute(self, persistence: Persistence):
        return (
            persistence.set_search_attribute_keyword(sa_keyword_key, sa_keyword),
            persistence.set_search_attribute_text(sa_text_key, sa_text),
            persistence.set_search_attribute_double(sa_double_key, sa_double),
            persistence.set_search_attribute_int64(sa_int_key, sa_int),
            persistence.set_search_attribute_datetime(sa_datetime_key, sa_datetime),
            persistence.set_search_attribute_keyword_array(
                sa_keyword_array_key, sa_keyword_array
            ),
        )


class TestPersistenceSearchAttributes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        wf = PersistenceSearchAttributesWorkflow()
        registry.add_workflow(wf)
        cls.client = Client(registry)

    def test_persistence_search_attributes_workflow(self):
        wf_id = f"{inspect.currentframe().f_code.co_name}-{time.time_ns()}"

        self.client.start_workflow(
            PersistenceSearchAttributesWorkflow, wf_id, 100, None
        )

        self.client.invoke_rpc(
            wf_id, PersistenceSearchAttributesWorkflow.test_persistence_set_search_attribute
        )

        time.sleep(1)

        returned_search_attributes = self.client.get_all_search_attributes(
            PersistenceSearchAttributesWorkflow, wf_id
        )

        expected_search_attributes = dict()
        expected_search_attributes[sa_keyword_key] = sa_keyword
        expected_search_attributes[sa_text_key] = sa_text
        expected_search_attributes[sa_double_key] = sa_double
        expected_search_attributes[sa_int_key] = sa_int
        expected_search_attributes[sa_keyword_array_key] = sa_keyword_array
        expected_search_attributes[sa_datetime_key] = (
            "2024-11-13T00:00:01.731455544Z"  # This is a bug. The iwf-server always returns utc time. See https://github.com/indeedeng/iwf/issues/261
            # "2024-11-12T18:00:01.731455544-06:00"
        )

        assert expected_search_attributes == returned_search_attributes

        self.client.wait_for_workflow_completion(wf_id, None)

        final_returned_search_attributes = self.client.get_all_search_attributes(
            PersistenceSearchAttributesWorkflow, wf_id
        )

        final_expected_search_attributes = dict()
        final_expected_search_attributes[sa_keyword_key] = final_sa_keyword
        final_expected_search_attributes[sa_text_key] = ""
        final_expected_search_attributes[sa_double_key] = sa_double
        final_expected_search_attributes[sa_int_key] = final_sa_int
        final_expected_search_attributes[sa_bool_key] = final_sa_bool
        final_expected_search_attributes[sa_keyword_array_key] = final_sa_keyword_array
        final_expected_search_attributes[sa_datetime_key] = (
            "2024-12-14T00:00:01.731455544Z"  # This is a bug. The iwf-server always returns utc time. See https://github.com/indeedeng/iwf/issues/261
            # "2024-12-13T18:00:01.731455544-06:00"
        )

        assert final_expected_search_attributes == final_returned_search_attributes
