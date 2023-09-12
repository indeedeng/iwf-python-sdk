from typing import Callable, Optional

from iwf.communication_schema import CommunicationMethodType
from iwf.errors import InvalidArgumentError, WorkflowDefinitionError
from iwf.persistence_schema import PersistenceFieldType
from iwf.rpc import RPCInfo
from iwf.workflow import ObjectWorkflow, get_workflow_type
from iwf.workflow_state import WorkflowState, get_state_id


class Registry:
    _workflow_store: dict[str, ObjectWorkflow]
    _starting_state_store: dict[str, WorkflowState]
    _state_store: dict[str, dict[str, WorkflowState]]
    _internal_channel_type_store: dict[str, dict[str, Optional[type]]]
    _signal_channel_type_store: dict[str, dict[str, Optional[type]]]
    _data_attribute_types: dict[str, dict[str, Optional[type]]]
    _rpc_infos: dict[str, dict[str, RPCInfo]]

    def __init__(self):
        self._workflow_store = dict()
        self._starting_state_store = dict()
        self._state_store = dict()
        self._internal_channel_type_store = dict()
        self._signal_channel_type_store = dict()
        self._data_attribute_types = dict()
        self._rpc_infos = dict()

    def add_workflow(self, wf: ObjectWorkflow):
        self._register_workflow_type(wf)
        self._register_workflow_state(wf)
        self._register_internal_channels(wf)
        self._register_signal_channels(wf)
        self._register_data_attributes(wf)
        self._register_workflow_rpcs(wf)

    def add_workflows(self, *wfs: ObjectWorkflow):
        for wf in wfs:
            self.add_workflow(wf)

    def get_workflow_with_check(self, wf_type: str) -> ObjectWorkflow:
        wf = self._workflow_store.get(wf_type)
        if wf is None:
            raise InvalidArgumentError(f"workflow {wf_type} is not registered")
        return wf

    def get_workflow_starting_state(self, wf_type: str) -> Optional[WorkflowState]:
        return self._starting_state_store.get(wf_type)

    def get_workflow_state_with_check(
        self, wf_type: str, state_id: str
    ) -> WorkflowState:
        states = self._state_store.get(wf_type)
        if states is None:
            raise InvalidArgumentError(f"workflow {wf_type} is not registered")
        state = states.get(state_id)
        if state is None:
            raise InvalidArgumentError(
                f"workflow {wf_type} state {state_id} is not registered"
            )
        return state

    def get_state_store(self, wf_type: str) -> dict[str, WorkflowState]:
        return self._state_store[wf_type]

    def get_internal_channel_types(self, wf_type: str) -> dict[str, Optional[type]]:
        return self._internal_channel_type_store[wf_type]

    def get_signal_channel_types(self, wf_type: str) -> dict[str, Optional[type]]:
        return self._signal_channel_type_store[wf_type]

    def get_data_attribute_types(self, wf_type: str) -> dict[str, Optional[type]]:
        return self._data_attribute_types[wf_type]

    def get_rpc_infos(self, wf_type: str) -> dict[str, RPCInfo]:
        return self._rpc_infos[wf_type]

    def _register_workflow_type(self, wf: ObjectWorkflow):
        wf_type = get_workflow_type(wf)
        if wf_type in self._workflow_store:
            raise WorkflowDefinitionError("workflow type conflict: ", wf_type)
        self._workflow_store[wf_type] = wf

    def _register_internal_channels(self, wf: ObjectWorkflow):
        wf_type = get_workflow_type(wf)
        types: dict[str, Optional[type]] = {}
        for method in wf.get_communication_schema().communication_methods:
            if method.method_type == CommunicationMethodType.InternalChannel:
                types[method.name] = method.value_type
        self._internal_channel_type_store[wf_type] = types

    def _register_signal_channels(self, wf: ObjectWorkflow):
        wf_type = get_workflow_type(wf)
        types: dict[str, Optional[type]] = {}
        for method in wf.get_communication_schema().communication_methods:
            if method.method_type == CommunicationMethodType.SignalChannel:
                types[method.name] = method.value_type
        self._signal_channel_type_store[wf_type] = types

    def _register_data_attributes(self, wf: ObjectWorkflow):
        wf_type = get_workflow_type(wf)
        types: dict[str, Optional[type]] = {}
        for field in wf.get_persistence_schema().persistence_fields:
            if field.field_type == PersistenceFieldType.DataAttribute:
                types[field.key] = field.value_type
        self._data_attribute_types[wf_type] = types

    def _register_workflow_state(self, wf):
        wf_type = get_workflow_type(wf)
        state_map = {}
        starting_state = None
        for state_def in wf.get_workflow_states().states:
            state_id = get_state_id(state_def.state)
            if state_id in state_map:
                raise WorkflowDefinitionError(
                    f"Workflow {wf_type} cannot have duplicate stateId {state_id}"
                )
            state_map[state_id] = state_def.state
            if state_def.can_start_workflow:
                if starting_state is not None:
                    raise WorkflowDefinitionError(
                        f"Workflow {wf_type} cannot contain more than one starting "
                        f"state"
                    )
                starting_state = state_def.state
            self._state_store[wf_type] = state_map
            self._starting_state_store[wf_type] = starting_state

    @staticmethod
    def _is_decorated_by_rpc(func: Callable):
        return getattr(func, "_is_iwf_rpc", False)

    @staticmethod
    def _get_rpc_info(func: Callable):
        info = getattr(func, "_rpc_info")
        assert isinstance(info, RPCInfo)
        # NOTE: we have to override the method here so that it's associated the object
        info.method_func = func
        return info

    def _register_workflow_rpcs(self, wf):
        wf_type = get_workflow_type(wf)
        rpc_infos = {}
        for method_name in dir(wf):
            method = getattr(wf, method_name)
            if callable(method) and self._is_decorated_by_rpc(method):
                rpc_infos[method_name] = self._get_rpc_info(method)
        self._rpc_infos[wf_type] = rpc_infos
