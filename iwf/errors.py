import json as jsonlib

from httpx._utils import guess_json_utf
from iwf_api.models import (
    ErrorResponse,
    ErrorSubStatus,
    WorkflowGetResponse,
    WorkflowStatus,
)


class WorkflowDefinitionError(Exception):
    pass


class InvalidArgumentError(Exception):
    pass


class HttpError(RuntimeError):
    def __init__(self, status: int, err_resp: ErrorResponse):
        super().__init__(err_resp.detail)
        self.sub_status = err_resp.sub_status
        self.error_resp = err_resp
        self.status = status


class ClientSideError(HttpError):
    pass


class ServerSideError(HttpError):
    pass


class WorkflowStillRunningError(ClientSideError):
    pass


class WorkflowRPCExecutionError(ClientSideError):
    pass


class WorkflowRPCAcquiringLockFailure(ClientSideError):
    pass


class WorkflowAlreadyStartedError(ClientSideError):
    pass


class WorkflowNotExistsError(ClientSideError):
    pass


def process_http_error(status: int, err_resp: ErrorResponse) -> HttpError:
    if 400 <= status < 500:
        if err_resp.sub_status == ErrorSubStatus.WORKFLOW_ALREADY_STARTED_SUB_STATUS:
            return WorkflowAlreadyStartedError(status, err_resp)
        elif err_resp.sub_status == ErrorSubStatus.WORKFLOW_NOT_EXISTS_SUB_STATUS:
            return WorkflowNotExistsError(status, err_resp)
        else:
            return ClientSideError(status, err_resp)
    else:
        return ServerSideError(status, err_resp)


class WorkflowAbnormalExitError(RuntimeError):
    def __init__(self, get_response: WorkflowGetResponse):
        self.run_id = get_response.workflow_run_id
        self.workflow_status = get_response.workflow_status
        self.error_type = get_response.error_type
        self.error_message = get_response.error_message
        # TODO add methods to decode the state results into objects
        self._state_results = get_response.results


class WorkflowFailed(WorkflowAbnormalExitError):
    pass


class WorkflowTimeout(WorkflowAbnormalExitError):
    pass


class WorkflowTerminated(WorkflowAbnormalExitError):
    pass


class WorkflowCanceled(WorkflowAbnormalExitError):
    pass


def process_workflow_abnormal_exit_error(
    get_response: WorkflowGetResponse,
) -> WorkflowAbnormalExitError:
    status = get_response.workflow_status
    if status == WorkflowStatus.CANCELED:
        return WorkflowCanceled(get_response)
    elif status == WorkflowStatus.FAILED:
        return WorkflowFailed(get_response)
    elif status == WorkflowStatus.TERMINATED:
        return WorkflowTerminated(get_response)
    elif status == WorkflowStatus.TIMEOUT:
        return WorkflowTimeout(get_response)
    return WorkflowAbnormalExitError(get_response)


def parse_unexpected_error(err) -> ErrorResponse:
    encoding = guess_json_utf(err.content)
    if encoding is not None:
        err_dict = jsonlib.loads(err.content.decode(encoding))
    else:
        err_dict = jsonlib.loads(err.content)
    return ErrorResponse.from_dict(err_dict)
