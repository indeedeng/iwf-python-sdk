import inspect
import time
import unittest

from iwf.client import Client
from iwf.iwf_api.models.workflow_stop_type import WorkflowStopType
from iwf.stop_workflow_options import StopWorkflowOptions
from iwf.tests import registry
from iwf.tests.workflows.rpc_memo_workflow import (
    RpcMemoWorkflow,
    TEST_DATA_OBJECT_KEY,
    TEST_SEARCH_ATTRIBUTE_INT,
    TEST_SEARCH_ATTRIBUTE_KEY,
    RPC_INPUT,
    RPC_OUTPUT,
    TEST_STR,
    TEST_DELAY,
)


class TestRpcWithMemo(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = Client(registry)

    def test_rpc_memo_workflow_func1(self):
        wf_id = f"{inspect.currentframe().f_code.co_name}-{time.time_ns()}"
        run_id = self.client.start_workflow(RpcMemoWorkflow, wf_id, 30, 999)

        self.client.invoke_rpc(
            wf_id, RpcMemoWorkflow.test_rpc_set_data_attribute, TEST_STR
        )
        value = self.client.invoke_rpc(
            wf_id, RpcMemoWorkflow.test_rpc_get_data_attribute_strong_consistency
        )
        assert value == TEST_STR
        time.sleep(TEST_DELAY)
        value = self.client.invoke_rpc(
            wf_id, RpcMemoWorkflow.test_rpc_get_data_attribute, None, str
        )

        self.client.invoke_rpc(wf_id, RpcMemoWorkflow.test_rpc_set_data_attribute, None)
        value = self.client.invoke_rpc(
            wf_id, RpcMemoWorkflow.test_rpc_get_data_attribute_strong_consistency
        )
        assert value is None
        time.sleep(TEST_DELAY)
        value = self.client.invoke_rpc(
            wf_id, RpcMemoWorkflow.test_rpc_get_data_attribute
        )
        assert value is None

        self.client.invoke_rpc(wf_id, RpcMemoWorkflow.test_rpc_set_keyword, TEST_STR)
        value = self.client.invoke_rpc(
            wf_id, RpcMemoWorkflow.test_rpc_get_keyword_strong_consistency
        )
        assert value == TEST_STR
        time.sleep(TEST_DELAY)
        value = self.client.invoke_rpc(wf_id, RpcMemoWorkflow.test_rpc_get_keyword)
        assert value == TEST_STR

        self.client.invoke_rpc(wf_id, RpcMemoWorkflow.test_rpc_set_keyword, None)
        value = self.client.invoke_rpc(
            wf_id, RpcMemoWorkflow.test_rpc_get_keyword_strong_consistency
        )
        assert value is None
        time.sleep(TEST_DELAY)
        value = self.client.invoke_rpc(wf_id, RpcMemoWorkflow.test_rpc_get_keyword)
        assert value is None

        rpc_output = self.client.invoke_rpc(
            wf_id, RpcMemoWorkflow.test_rpc_func1, RPC_INPUT
        )
        assert RPC_OUTPUT == rpc_output

        self.client.wait_for_workflow_completion(wf_id)

        data_attributes = self.client.get_workflow_data_attributes(
            RpcMemoWorkflow, wf_id, run_id, [TEST_DATA_OBJECT_KEY]
        )
        assert TEST_DATA_OBJECT_KEY in data_attributes
        assert data_attributes[TEST_DATA_OBJECT_KEY] == RPC_INPUT

        search_attributes = self.client.get_workflow_search_attributes(
            RpcMemoWorkflow,
            wf_id,
            [TEST_SEARCH_ATTRIBUTE_KEY, TEST_SEARCH_ATTRIBUTE_INT],
            run_id,
        )
        assert TEST_SEARCH_ATTRIBUTE_INT in search_attributes
        assert TEST_SEARCH_ATTRIBUTE_KEY in search_attributes
        assert search_attributes[TEST_SEARCH_ATTRIBUTE_INT] == RPC_OUTPUT
        assert search_attributes[TEST_SEARCH_ATTRIBUTE_KEY] == RPC_INPUT

    def test_rpc_memo_workflow_func0(self):
        wf_id = f"{inspect.currentframe().f_code.co_name}-{time.time_ns()}"
        run_id = self.client.start_workflow(RpcMemoWorkflow, wf_id, 30, 999)

        rpc_output = self.client.invoke_rpc(
            wf_id, RpcMemoWorkflow.test_rpc_func0, TEST_STR
        )
        assert RPC_OUTPUT == rpc_output

        self.client.wait_for_workflow_completion(wf_id)

        data_attributes = self.client.get_workflow_data_attributes(
            RpcMemoWorkflow, wf_id, run_id, [TEST_DATA_OBJECT_KEY]
        )
        assert TEST_DATA_OBJECT_KEY in data_attributes
        assert data_attributes[TEST_DATA_OBJECT_KEY] == TEST_STR

        search_attributes = self.client.get_workflow_search_attributes(
            RpcMemoWorkflow,
            wf_id,
            [TEST_SEARCH_ATTRIBUTE_KEY, TEST_SEARCH_ATTRIBUTE_INT],
            run_id,
        )
        assert TEST_SEARCH_ATTRIBUTE_INT in search_attributes
        assert TEST_SEARCH_ATTRIBUTE_KEY in search_attributes
        assert search_attributes[TEST_SEARCH_ATTRIBUTE_INT] == RPC_OUTPUT
        assert search_attributes[TEST_SEARCH_ATTRIBUTE_KEY] == TEST_STR

    def test_rpc_memo_workflow_proc1(self):
        wf_id = f"{inspect.currentframe().f_code.co_name}-{time.time_ns()}"
        run_id = self.client.start_workflow(RpcMemoWorkflow, wf_id, 30, 999)

        self.client.invoke_rpc(wf_id, RpcMemoWorkflow.test_rpc_proc1, RPC_INPUT)
        self.client.wait_for_workflow_completion(wf_id)

        data_attributes = self.client.get_workflow_data_attributes(
            RpcMemoWorkflow, wf_id, run_id, [TEST_DATA_OBJECT_KEY]
        )
        assert TEST_DATA_OBJECT_KEY in data_attributes
        assert data_attributes[TEST_DATA_OBJECT_KEY] == RPC_INPUT

        search_attributes = self.client.get_workflow_search_attributes(
            RpcMemoWorkflow,
            wf_id,
            [TEST_SEARCH_ATTRIBUTE_KEY, TEST_SEARCH_ATTRIBUTE_INT],
            run_id,
        )
        assert TEST_SEARCH_ATTRIBUTE_INT in search_attributes
        assert TEST_SEARCH_ATTRIBUTE_KEY in search_attributes
        assert search_attributes[TEST_SEARCH_ATTRIBUTE_INT] == RPC_OUTPUT
        assert search_attributes[TEST_SEARCH_ATTRIBUTE_KEY] == RPC_INPUT

    def test_rpc_memo_workflow_proc0(self):
        wf_id = f"{inspect.currentframe().f_code.co_name}-{time.time_ns()}"
        run_id = self.client.start_workflow(RpcMemoWorkflow, wf_id, 30, 999)

        self.client.invoke_rpc(wf_id, RpcMemoWorkflow.test_rpc_proc0)
        self.client.wait_for_workflow_completion(wf_id)

        data_attributes = self.client.get_workflow_data_attributes(
            RpcMemoWorkflow, wf_id, run_id, [TEST_DATA_OBJECT_KEY]
        )
        assert TEST_DATA_OBJECT_KEY in data_attributes
        assert data_attributes[TEST_DATA_OBJECT_KEY] == TEST_STR

        search_attributes = self.client.get_workflow_search_attributes(
            RpcMemoWorkflow,
            wf_id,
            [TEST_SEARCH_ATTRIBUTE_KEY, TEST_SEARCH_ATTRIBUTE_INT],
            run_id,
        )
        assert TEST_SEARCH_ATTRIBUTE_INT in search_attributes
        assert TEST_SEARCH_ATTRIBUTE_KEY in search_attributes
        assert search_attributes[TEST_SEARCH_ATTRIBUTE_INT] == RPC_OUTPUT
        assert search_attributes[TEST_SEARCH_ATTRIBUTE_KEY] == TEST_STR

    def test_rpc_memo_workflow_func1_readonly(self):
        wf_id = f"{inspect.currentframe().f_code.co_name}-{time.time_ns()}"
        self.client.start_workflow(RpcMemoWorkflow, wf_id, 30, 999)

        rpc_output = self.client.invoke_rpc(
            wf_id, RpcMemoWorkflow.test_rpc_func1_readonly, RPC_INPUT
        )
        assert RPC_OUTPUT == rpc_output

        self.client.stop_workflow(
            wf_id,
            StopWorkflowOptions(
                workflow_stop_type=WorkflowStopType.FAIL,
                reason=TEST_STR,
            ),
        )
