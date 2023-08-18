import traceback
from threading import Thread

from flask import Flask, request
from iwf_api.models import WorkflowStateWaitUntilRequest, WorkflowStateExecuteRequest

from iwf.registry import Registry
from iwf.worker_service import (
    workflow_state_wait_until_api_path,
    WorkerService,
    workflow_state_execute_api_path,
)

debug_mode = False

registry = Registry()

_flask_app = Flask(__name__)

_worker_service = WorkerService(registry)


@_flask_app.route("/")
def index():
    return "hello"


@_flask_app.route(workflow_state_wait_until_api_path, methods=["POST"])
def handle_wait_until():
    req = WorkflowStateWaitUntilRequest.from_dict(request.json)
    resp = _worker_service.handle_workflow_state_wait_until(req)
    return resp.to_dict()


@_flask_app.route(workflow_state_execute_api_path, methods=["POST"])
def handle_execute():
    req = WorkflowStateExecuteRequest.from_dict(request.json)
    resp = _worker_service.handle_workflow_state_execute(req)
    return resp.to_dict()


@_flask_app.errorhandler(Exception)
def internal_error(exception):
    print("500 error caught")
    print(traceback.format_exc())
    response = exception.get_response()
    # replace the body with JSON
    response.data = traceback.format_exc()
    response.content_type = "application/json"
    response.status_code = 500
    return response


_webApp = Thread(target=_flask_app.run, args=("127.0.0.1", 8802))
# when debugging, keep the thread running so that we can see the error in history
_webApp.setDaemon(not debug_mode)
_webApp.start()