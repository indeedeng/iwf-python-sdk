import inspect
import time
import unittest

import httpx

from iwf.client import Client
from iwf.tests.worker_server import registry
from iwf.worker_service import WorkerService


class TestBinaryNullDecodesCorrectly(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = Client(registry)

    def test_binary_null_input_decodes_correctly(self):
        wf_id = f"{inspect.currentframe().f_code.co_name}-{time.time_ns()}"

        response = httpx.post(
            f"http://0.0.0.0:8802/{WorkerService.api_path_workflow_state_execute}",
            json={
                "DataObjects": [
                    {"key": "test-da", "value": {"encoding": "binary/null"}}
                ],
                "commandResults": {
                    "interStateChannelResults": [],
                    "stateStartApiSucceeded": True,
                },
                "context": {
                    "attempt": 1,
                    "firstAttemptTimestamp": 1747935829,
                    "stateExecutionId": "State1-1",
                    "workflowId": wf_id,
                    "workflowRunId": "0196f734-d037-7432-bd63-e1136cd34dbd",
                    "workflowStartedTimestamp": 1747904155,
                },
                "stateInput": {"encoding": "binary/null"},
                "stateLocals": [],
                "workflowStateId": "State1",
                "workflowType": "EmptyDataWorkflow",
            },
        )
        assert response.is_success
        response_json = response.json()
        self.assertEqual(
            response_json,
            {
                "publishToInterStateChannel": [],
                "recordEvents": [],
                "stateDecision": {
                    "nextStates": [
                        {
                            "stateId": "_SYS_GRACEFUL_COMPLETING_WORKFLOW",
                            "stateInput": {
                                "data": '"success"',
                                "encoding": "json/plain",
                            },
                        }
                    ]
                },
                "upsertDataObjects": [],
                "upsertStateLocals": [],
            },
        )
