from dataclasses import dataclass
from functools import wraps
from inspect import signature
from typing import Any, Callable

from iwf.errors import WorkflowDefinitionError


@dataclass
class RPCInfo:
    method_func: Callable
    timeout_seconds: int


rpc_definition_err = WorkflowDefinitionError(
    "an RPC must have at most 5 params: self, context:WorkflowContext, input:Any, persistence:Persistence, "
    'communication:Communication, where input can be any type as long as the param name is "input" '
)


def rpc(timeout_seconds: int = 10):
    def decorator(func):
        # preserve the properties of the original function.
        @wraps(func)
        def wrapper(*args, **kwargs):
            # TODO need to add type hint for decorated method
            return func(*args, **kwargs)

        wrapper._is_iwf_rpc = True
        wrapper._timeout_seconds = timeout_seconds
        params = signature(func).parameters

        from inspect import _empty  # ignored.
        from iwf.persistence import Persistence
        from iwf.workflow_context import WorkflowContext
        from iwf.communication import Communication

        valid_param_types = {
            _empty: True,
            Any: True,
            Persistence: True,
            WorkflowContext: True,
            Communication: True,
        }
        if len(params) > 5:
            raise rpc_definition_err

        for k, v in params.items():
            if k == "input":
                continue
            if v.annotation not in valid_param_types:
                raise rpc_definition_err

        return wrapper

    return decorator
