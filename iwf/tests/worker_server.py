import traceback
from threading import Thread

from flask import Flask, request

from iwf.iwf_api.iwf_api.models import (
    WorkflowStateExecuteRequest,
    WorkflowStateWaitUntilRequest,
    WorkflowWorkerRpcRequest,
)
from iwf.registry import Registry
from iwf.worker_service import (
    WorkerService,
)

debug_mode: bool = False

registry = Registry()

_flask_app = Flask(__name__)

_worker_service = WorkerService(registry)


@_flask_app.route("/")
def index():
    return "hello"


@_flask_app.route(WorkerService.api_path_workflow_state_wait_until, methods=["POST"])
def handle_wait_until():
    req = WorkflowStateWaitUntilRequest.from_dict(request.json)
    resp = _worker_service.handle_workflow_state_wait_until(req)
    return resp.to_dict()


@_flask_app.route(WorkerService.api_path_workflow_state_execute, methods=["POST"])
def handle_execute():
    req = WorkflowStateExecuteRequest.from_dict(request.json)
    resp = _worker_service.handle_workflow_state_execute(req)
    return resp.to_dict()


@_flask_app.route(WorkerService.api_path_workflow_worker_rpc, methods=["POST"])
def handle_rpc():
    req = WorkflowWorkerRpcRequest.from_dict(request.json)
    resp = _worker_service.handle_workflow_worker_rpc(req)
    return resp.to_dict()


@_flask_app.errorhandler(Exception)
def internal_error(exception):
    # TODO: how to print to std ??
    response = exception.get_response()
    # replace the body with JSON
    response.data = traceback.format_exc()
    response.content_type = "application/json"
    response.status_code = 500
    return response


_webApp = Thread(target=_flask_app.run, args=("0.0.0.0", 8802))
# when debugging, keep the thread running so that we can see the error in history
_webApp.setDaemon(not debug_mode)
_webApp.start()
