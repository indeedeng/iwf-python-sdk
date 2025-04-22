from dataclasses import dataclass
from typing import Optional
from iwf.data_attribute_state import DataAttributePrefixState, DataAttributeState
from iwf.iwf_api.models.workflow_status import WorkflowStatus
from iwf.rpc import RPCInfo
from iwf.search_attribute_state import SearchAttributeState


@dataclass
class WorkflowDefinition:
    search_attributes: dict[str, SearchAttributeState]
    data_attributes: dict[str, DataAttributeState]
    data_attribute_prefixes: dict[str, DataAttributePrefixState]
    workflow_status: Optional[WorkflowStatus]
    signal_channel_types: dict[str, Optional[type]]
    rpc_infos: dict[str, RPCInfo]
