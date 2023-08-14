from abc import ABC, abstractmethod
from typing import TypeVar, Generic

from iwf.command_request import CommandRequest
from iwf.command_results import CommandResults
from iwf.communication import Communication
from iwf.persistence import Persistence
from iwf.state_decision import StateDecision
from iwf.workflow_context import WorkflowContext
from iwf.workflow_state_options import WorkflowStateOptions

T = TypeVar("T")


class WorkflowState(ABC, Generic[T]):
    """WorkflowState is the interface to define a workflow state."""

    @abstractmethod
    def get_input_type(self) -> type[T]:
        raise NotImplementedError

    def wait_until(
        self,
        ctx: WorkflowContext,
        input: T,
        persistence: Persistence,
        communication: Communication,
    ) -> CommandRequest:
        """
        WaitUntil is the method to set up commands set up to wait for, before `Execute` API is invoked.
        It's optional -- execute will be invoked instead if this is not implemented.

        Args:
            ctx: the context info of this API invocation, like workflow start time, workflowId, etc
            input: input: the state input
            persistence:  the API for 1) data attributes, 2) search attributes and 3) stateExecutionLocals 4) recordEvent
                        DataObjects and SearchAttributes are defined by ObjectWorkflow interface.
                        StateExecutionLocals are for passing data within the state execution
                        RecordEvent is for storing some tracking info(e.g. RPC call input/output) when executing the API.
                        Note that any write API will be recorded to server after the whole WaitUntil API response is accepted
            communication: the API right now only for publishing value to internalChannel
                        Note that any write API will be recorded to server after the whole start API response is accepted.

        Returns: the requested command
        """
        pass

    @abstractmethod
    def execute(
        self,
        ctx: WorkflowContext,
        input: T,
        command_results: CommandResults,
        persistence: Persistence,
        communication: Communication,
    ) -> StateDecision:
        """
        Execute is the method to execute and decide what to do next. Invoke after commands from WaitUntil are completed, or there is WaitUntil is not implemented for the state.

          Args:
              ctx: the context info of this API invocation, like workflow start time, workflowId, etc
              input:  the state input
              command_results: the results of the command that executed by WaitUntil
              persistence:  the API for 1) data attributes, 2) search attributes and 3) stateExecutionLocals 4) recordEvent
                                  DataObjects and SearchAttributes are defined by ObjectWorkflow interface.
                                  StateExecutionLocals are for passing data within the state execution
                                  RecordEvent is for storing some tracking info(e.g. RPC call input/output) when executing the API.
                                  Note that any write API will be recorded to server after the whole WaitUntil API response is accepted
              communication: the API right now only for publishing value to internalChannel
                                  Note that any write API will be recorded to server after the whole start API response is accepted.

          Returns: the decision of what to do next(e.g. transition to next states or closing workflow)

        """
        raise NotImplementedError

    def get_state_options(self) -> WorkflowStateOptions:
        """GetStateOptions can just return nil to use the default Options
        StateOptions is optional configuration to adjust the state behaviors
        Returns: WorkflowStateOptions
        """
        pass
