import inspect
import time
import unittest
from time import sleep

from iwf.client import Client
from iwf.command_request import CommandRequest, TimerCommand
from iwf.command_results import CommandResults
from iwf.communication import Communication
from iwf.iwf_api.models import SearchAttributeValueType
from iwf.persistence import Persistence
from iwf.persistence_schema import PersistenceField, PersistenceSchema
from iwf.state_decision import StateDecision
from iwf.state_schema import StateSchema
from iwf.tests.worker_server import registry
from iwf.workflow import ObjectWorkflow
from iwf.workflow_context import WorkflowContext
from iwf.workflow_options import WorkflowOptions
from iwf.workflow_state import T, WorkflowState

sa_keyword_key = "CustomKeywordField"
sa_double_key = "CustomDoubleField"
sa_int_key = "CustomIntField"
sa_bool_key = "CustomBoolField"
sa_datetime_key = "CustomDatetimeField"
sa_keyword_array_key = "CustomKeywordArrayField"

initial_sa_keyword: str = "initial_keyword"
initial_sa_double: float = 1.11
initial_sa_int: int = 1
initial_sa_bool: bool = True
initial_sa_datetime: str = "2024-11-09T16:00:01.731455544-08:00"
initial_sa_keyword_array: list[str] = ["initial_keyword-1", "initial_keyword-2"]

sa_keyword: str = "keyword"
sa_double: float = 2.34
sa_int: int = 234
sa_bool: bool = False
sa_datetime: str = "2024-11-12T16:00:01.731455544-08:00"
sa_keyword_array: list[str] = ["keyword-1", "keyword-2"]

final_sa_keyword: str = "final_keyword"
final_sa_int: int = 567
final_sa_bool: bool = False
final_sa_datetime: str = "2024-12-13T16:00:01.731455544-08:00"
final_sa_keyword_array: list[str] = ["final_keyword-1", "final_keyword-2"]


class SearchAttributeStateInit(WorkflowState[None]):
    def wait_until(
        self,
        ctx: WorkflowContext,
        input: T,
        persistence: Persistence,
        communication: Communication,
    ) -> CommandRequest:
        return CommandRequest.for_all_command_completed(
            TimerCommand.by_seconds(2),
        )

    def execute(
        self,
        ctx: WorkflowContext,
        input: T,
        command_results: CommandResults,
        persistence: Persistence,
        communication: Communication,
    ) -> StateDecision:
        persistence.set_search_attribute_keyword(sa_keyword_key, sa_keyword)
        persistence.set_search_attribute_double(sa_double_key, sa_double)
        persistence.set_search_attribute_boolean(sa_bool_key, sa_bool)
        persistence.set_search_attribute_keyword_array(
            sa_keyword_array_key, sa_keyword_array
        )
        persistence.set_search_attribute_int64(sa_int_key, sa_int)
        persistence.set_search_attribute_datetime(sa_datetime_key, sa_datetime)
        return StateDecision.single_next_state(SearchAttributeState1)


class SearchAttributeState1(WorkflowState[None]):
    def wait_until(
        self,
        ctx: WorkflowContext,
        input: T,
        persistence: Persistence,
        communication: Communication,
    ) -> CommandRequest:
        return CommandRequest.for_all_command_completed(
            TimerCommand.by_seconds(2),
        )

    def execute(
        self,
        ctx: WorkflowContext,
        input: T,
        command_results: CommandResults,
        persistence: Persistence,
        communication: Communication,
    ) -> StateDecision:
        return StateDecision.single_next_state(SearchAttributeState2)


class SearchAttributeState2(WorkflowState[None]):
    def wait_until(
        self,
        ctx: WorkflowContext,
        input: T,
        persistence: Persistence,
        communication: Communication,
    ) -> CommandRequest:
        return CommandRequest.empty()

    def execute(
        self,
        ctx: WorkflowContext,
        input: T,
        command_results: CommandResults,
        persistence: Persistence,
        communication: Communication,
    ) -> StateDecision:
        # Delay updating search attributes to allow for the previous assertion
        sleep(1)
        persistence.set_search_attribute_keyword(sa_keyword_key, final_sa_keyword)
        persistence.set_search_attribute_boolean(sa_bool_key, final_sa_bool)
        persistence.set_search_attribute_keyword_array(
            sa_keyword_array_key, final_sa_keyword_array
        )
        persistence.set_search_attribute_int64(sa_int_key, final_sa_int)
        persistence.set_search_attribute_datetime(sa_datetime_key, final_sa_datetime)
        return StateDecision.graceful_complete_workflow()


class PersistenceSearchAttributesWorkflow(ObjectWorkflow):
    def get_workflow_states(self) -> StateSchema:
        return StateSchema.with_starting_state(
            SearchAttributeStateInit(), SearchAttributeState1(), SearchAttributeState2()
        )

    def get_persistence_schema(self) -> PersistenceSchema:
        return PersistenceSchema.create(
            PersistenceField.search_attribute_def(
                sa_keyword_key, SearchAttributeValueType.KEYWORD
            ),
            PersistenceField.search_attribute_def(
                sa_double_key, SearchAttributeValueType.DOUBLE
            ),
            PersistenceField.search_attribute_def(
                sa_bool_key, SearchAttributeValueType.BOOL
            ),
            PersistenceField.search_attribute_def(
                sa_keyword_array_key, SearchAttributeValueType.KEYWORD_ARRAY
            ),
            PersistenceField.search_attribute_def(
                sa_int_key, SearchAttributeValueType.INT
            ),
            PersistenceField.search_attribute_def(
                sa_datetime_key, SearchAttributeValueType.DATETIME
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

        wf_opts = WorkflowOptions(
            initial_search_attributes={
                sa_keyword_key: initial_sa_keyword,
                sa_double_key: initial_sa_double,
                sa_int_key: initial_sa_int,
                sa_bool_key: initial_sa_bool,
                sa_datetime_key: initial_sa_datetime,
                sa_keyword_array_key: initial_sa_keyword_array,
            }
        )
        wf_opts.add_wait_for_completion_state_ids(SearchAttributeState1)
        self.client.start_workflow(
            PersistenceSearchAttributesWorkflow, wf_id, 100, None, wf_opts
        )

        initial_returned_search_attributes = self.client.get_all_search_attributes(
            PersistenceSearchAttributesWorkflow,
            wf_id,
        )

        initial_expected_search_attributes = dict()
        initial_expected_search_attributes[sa_keyword_key] = initial_sa_keyword
        initial_expected_search_attributes[sa_double_key] = initial_sa_double
        initial_expected_search_attributes[sa_bool_key] = initial_sa_bool
        initial_expected_search_attributes[sa_keyword_array_key] = (
            initial_sa_keyword_array
        )
        initial_expected_search_attributes[sa_int_key] = initial_sa_int
        initial_expected_search_attributes[sa_datetime_key] = (
            "2024-11-10T00:00:01.731455544Z"  # This is a bug. The iwf-server always returns utc time. See https://github.com/indeedeng/iwf/issues/261
            # "2024-11-09T18:00:01.731455544-06:00"
        )

        assert initial_expected_search_attributes == initial_returned_search_attributes

        self.client.wait_for_state_execution_completion_with_state_execution_id(
            SearchAttributeState1, wf_id
        )

        returned_search_attributes = self.client.get_all_search_attributes(
            PersistenceSearchAttributesWorkflow,
            wf_id,
        )

        expected_search_attributes = dict()
        expected_search_attributes[sa_keyword_key] = sa_keyword
        expected_search_attributes[sa_double_key] = sa_double
        expected_search_attributes[sa_bool_key] = sa_bool
        expected_search_attributes[sa_keyword_array_key] = sa_keyword_array
        expected_search_attributes[sa_int_key] = sa_int
        expected_search_attributes[sa_datetime_key] = (
            "2024-11-13T00:00:01.731455544Z"  # This is a bug. The iwf-server always returns utc time. See https://github.com/indeedeng/iwf/issues/261
            # "2024-11-12T18:00:01.731455544-06:00"
        )

        assert expected_search_attributes == returned_search_attributes

        self.client.wait_for_workflow_completion(wf_id)

        final_expected_search_attributes = dict()
        final_expected_search_attributes[sa_keyword_key] = final_sa_keyword
        final_expected_search_attributes[sa_double_key] = sa_double
        final_expected_search_attributes[sa_int_key] = final_sa_int
        final_expected_search_attributes[sa_bool_key] = final_sa_bool
        final_expected_search_attributes[sa_keyword_array_key] = final_sa_keyword_array
        final_expected_search_attributes[sa_datetime_key] = (
            "2024-12-14T00:00:01.731455544Z"  # This is a bug. The iwf-server always returns utc time. See https://github.com/indeedeng/iwf/issues/261
            # "2024-12-13T18:00:01.731455544-06:00"
        )

        final_returned_search_attributes = self.client.get_all_search_attributes(
            PersistenceSearchAttributesWorkflow,
            wf_id,
        )

        assert final_expected_search_attributes == final_returned_search_attributes
