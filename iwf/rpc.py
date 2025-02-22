from dataclasses import dataclass
from functools import wraps
from inspect import signature
from typing import Callable, Optional

from iwf.errors import WorkflowDefinitionError
from iwf.iwf_api.models import PersistenceLoadingPolicy, PersistenceLoadingType


@dataclass
class RPCInfo:
    method_func: Callable
    timeout_seconds: int
    input_type: Optional[type] = None
    data_attribute_loading_policy: Optional[PersistenceLoadingPolicy] = None
    params_order: Optional[list] = (
        None  # store this so that the rpc can be invoked with correct parameters
    )


rpc_definition_err = WorkflowDefinitionError(
    "an RPC must have at most 5 params: self, context:WorkflowContext, input:Any, persistence:Persistence, "
    "communication:Communication, where input can be any type"
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
        rpc_info = RPCInfo(
            method_func=func,
            timeout_seconds=timeout_seconds,
            data_attribute_loading_policy=data_attribute_loading_policy,
        )
        params = signature(func).parameters

        from inspect import _empty  # ignored.
        from iwf.persistence import Persistence
        from iwf.workflow_context import WorkflowContext
        from iwf.communication import Communication

        valid_param_types_exclude_input = {
            _empty: True,
            Persistence: True,
            WorkflowContext: True,
            Communication: True,
        }
        need_persistence = False
        params_order = []
        if len(params) > 5:
            raise rpc_definition_err

        has_input = False
        for k, v in params.items():
            if k != "self":
                params_order.append(v.annotation)

            if v.annotation == Persistence:
                need_persistence = True
            if v.annotation not in valid_param_types_exclude_input:
                if not has_input:
                    has_input = True
                    rpc_info.input_type = v.annotation
                else:
                    raise rpc_definition_err
        if not need_persistence:
            rpc_info.data_attribute_loading_policy = PersistenceLoadingPolicy(
                persistence_loading_type=PersistenceLoadingType.LOAD_NONE
            )
        rpc_info.params_order = params_order
        wrapper._rpc_info = rpc_info
        return wrapper

    return decorator
