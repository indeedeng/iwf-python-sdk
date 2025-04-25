from iwf.registry import Registry
from iwf.tests.workflows.java_duplicate_rpc_memo_workflow import (
    JavaDuplicateRpcMemoWorkflow,
)
from iwf.tests.workflows.abnormal_exit_workflow import AbnormalExitWorkflow
from iwf.tests.workflows.basic_workflow import BasicWorkflow
from iwf.tests.workflows.conditional_complete_workflow import (
    ConditionalCompleteWorkflow,
)
from iwf.tests.workflows.describe_workflow import DescribeWorkflow
from iwf.tests.workflows.internal_channel_workflow import InternalChannelWorkflow
from iwf.tests.workflows.internal_channel_workflow_with_no_prefix_channel import (
    InternalChannelWorkflowWithNoPrefixChannel,
)
from iwf.tests.workflows.persistence_data_attributes_workflow import (
    PersistenceDataAttributesWorkflow,
)
from iwf.tests.workflows.persistence_search_attributes_workflow import (
    PersistenceSearchAttributesWorkflow,
)
from iwf.tests.workflows.persistence_state_execution_local_workflow import (
    PersistenceStateExecutionLocalWorkflow,
)
from iwf.tests.workflows.recovery_workflow import RecoveryWorkflow
from iwf.tests.workflows.rpc_memo_workflow import RpcMemoWorkflow
from iwf.tests.workflows.rpc_workflow import RPCWorkflow
from iwf.tests.workflows.state_options_override_workflow import (
    StateOptionsOverrideWorkflow,
)
from iwf.tests.workflows.timer_workflow import TimerWorkflow
from iwf.tests.workflows.wait_for_state_with_state_execution_id_workflow import (
    WaitForStateWithStateExecutionIdWorkflow,
)
from iwf.tests.workflows.wait_for_state_with_wait_for_key_workflow import (
    WaitForStateWithWaitForKeyWorkflow,
)
from iwf.tests.workflows.wait_internal_channel_workflow import (
    WaitInternalChannelWorkflow,
)
from iwf.tests.workflows.wait_signal_workflow import WaitSignalWorkflow

registry = Registry()

registry.add_workflow(AbnormalExitWorkflow())
registry.add_workflow(BasicWorkflow())
registry.add_workflow(ConditionalCompleteWorkflow())
registry.add_workflow(DescribeWorkflow())
registry.add_workflow(InternalChannelWorkflow())
registry.add_workflow(InternalChannelWorkflowWithNoPrefixChannel())
registry.add_workflow(JavaDuplicateRpcMemoWorkflow())
registry.add_workflow(PersistenceDataAttributesWorkflow())
registry.add_workflow(PersistenceSearchAttributesWorkflow())
registry.add_workflow(PersistenceStateExecutionLocalWorkflow())
registry.add_workflow(RecoveryWorkflow())
registry.add_workflow(RpcMemoWorkflow())
registry.add_workflow(RPCWorkflow())
registry.add_workflow(TimerWorkflow())
registry.add_workflow(StateOptionsOverrideWorkflow())
registry.add_workflow(WaitForStateWithStateExecutionIdWorkflow())
registry.add_workflow(WaitForStateWithWaitForKeyWorkflow())
registry.add_workflow(WaitInternalChannelWorkflow())
registry.add_workflow(WaitSignalWorkflow())
