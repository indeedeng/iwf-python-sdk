from threading import Thread

import pytest
from flask import Flask, request
from iwf_api.models import WorkflowStateWaitUntilRequest, WorkflowStateExecuteRequest

from iwf.registry import Registry
from iwf.worker_service import (
    workflow_state_wait_until_api_path,
    WorkerService,
    workflow_state_execute_api_path,
)

workflow_worker = Flask(__name__)

registry = Registry()
worker_service = WorkerService(registry)


@workflow_worker.route("/")
def index():
    return "hello"


@workflow_worker.route(workflow_state_wait_until_api_path, methods=["POST"])
def handle_wait_until():
    req = WorkflowStateWaitUntilRequest.from_dict(request.json)
    resp = worker_service.handle_workflow_state_wait_until(req)
    return resp.to_dict()


@workflow_worker.route(workflow_state_execute_api_path, methods=["POST"])
def handle_execute():
    req = WorkflowStateExecuteRequest.from_dict(request.json)
    resp = worker_service.handle_workflow_state_execute(req)
    return resp.to_dict()


@pytest.fixture(autouse=True)
def run_around_tests():
    thread = Thread(target=workflow_worker.run, args=("127.0.0.1", 8802))
    thread.start()

    yield

    thread._stop()
