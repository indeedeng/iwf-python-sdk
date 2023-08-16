from iwf_api.models import ErrorResponse, WorkflowGetResponse


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


def process_http_error_get_api(status: int, err_resp: ErrorResponse) -> HttpError:
    """
    special handling for 420 for get API
    """
    if status == 420:
        return WorkflowStillRunningError(status, err_resp)
    return process_http_error(status, err_resp)


def process_http_error(status: int, err_resp: ErrorResponse) -> HttpError:
    if 400 <= status < 500:
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
