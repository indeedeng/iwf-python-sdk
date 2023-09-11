from dataclasses import dataclass
from functools import wraps
from inspect import signature
from typing import Any, Callable, Optional

from iwf_api.models import PersistenceLoadingPolicy, PersistenceLoadingType

from iwf.errors import WorkflowDefinitionError


@dataclass
class RPCInfo:
    method_func: Callable
    timeout_seconds: int
    data_attribute_loading_policy: Optional[PersistenceLoadingPolicy] = None
    params_order: Optional[
        list
    ] = None  # store this so that the rpc can be invoked with correct parameters


rpc_definition_err = WorkflowDefinitionError(
    "an RPC must have at most 5 params: self, context:WorkflowContext, input:Any, persistence:Persistence, "
    'communication:Communication, where input can be any type as long as the param name is "input" '
)


def rpc(
    timeout_seconds: int = 10,
    data_attribute_loading_policy: Optional[PersistenceLoadingPolicy] = None,
):
    def decorator(func):
        # preserve the properties of the original function.
        @wraps(func)
        def wrapper(*args, **kwargs):
            # TODO need to add type hint for decorated method
            return func(*args, **kwargs)

        wrapper._is_iwf_rpc = True
        wrapper._timeout_seconds = timeout_seconds
        wrapper._data_attribute_loading_policy = data_attribute_loading_policy
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
        need_persistence = False
        params_order = []
        if len(params) > 5:
            raise rpc_definition_err

        for k, v in params.items():
            if k != "self":
                params_order.append(v.annotation)
            if k == "input":
                continue
            if v.annotation == Persistence:
                need_persistence = True
            if v.annotation not in valid_param_types:
                raise rpc_definition_err
        if not need_persistence:
            wrapper._data_attribute_loading_policy = PersistenceLoadingPolicy(
                persistence_loading_type=PersistenceLoadingType.LOAD_NONE
            )
        wrapper._params_order = params_order
        return wrapper

    return decorator
