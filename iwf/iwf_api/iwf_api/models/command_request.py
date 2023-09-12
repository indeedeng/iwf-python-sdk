from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.command_waiting_type import CommandWaitingType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.command_combination import CommandCombination
    from ..models.inter_state_channel_command import InterStateChannelCommand
    from ..models.signal_command import SignalCommand
    from ..models.timer_command import TimerCommand


T = TypeVar("T", bound="CommandRequest")


@attr.s(auto_attribs=True)
class CommandRequest:
    """
    Attributes:
        command_waiting_type (CommandWaitingType):
        timer_commands (Union[Unset, List['TimerCommand']]):
        signal_commands (Union[Unset, List['SignalCommand']]):
        inter_state_channel_commands (Union[Unset, List['InterStateChannelCommand']]):
        command_combinations (Union[Unset, List['CommandCombination']]):
    """

    command_waiting_type: CommandWaitingType
    timer_commands: Union[Unset, List["TimerCommand"]] = UNSET
    signal_commands: Union[Unset, List["SignalCommand"]] = UNSET
    inter_state_channel_commands: Union[Unset, List["InterStateChannelCommand"]] = UNSET
    command_combinations: Union[Unset, List["CommandCombination"]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        command_waiting_type = self.command_waiting_type.value

        timer_commands: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.timer_commands, Unset):
            timer_commands = []
            for timer_commands_item_data in self.timer_commands:
                timer_commands_item = timer_commands_item_data.to_dict()

                timer_commands.append(timer_commands_item)

        signal_commands: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.signal_commands, Unset):
            signal_commands = []
            for signal_commands_item_data in self.signal_commands:
                signal_commands_item = signal_commands_item_data.to_dict()

                signal_commands.append(signal_commands_item)

        inter_state_channel_commands: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.inter_state_channel_commands, Unset):
            inter_state_channel_commands = []
            for (
                inter_state_channel_commands_item_data
            ) in self.inter_state_channel_commands:
                inter_state_channel_commands_item = (
                    inter_state_channel_commands_item_data.to_dict()
                )

                inter_state_channel_commands.append(inter_state_channel_commands_item)

        command_combinations: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.command_combinations, Unset):
            command_combinations = []
            for command_combinations_item_data in self.command_combinations:
                command_combinations_item = command_combinations_item_data.to_dict()

                command_combinations.append(command_combinations_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "commandWaitingType": command_waiting_type,
            }
        )
        if timer_commands is not UNSET:
            field_dict["timerCommands"] = timer_commands
        if signal_commands is not UNSET:
            field_dict["signalCommands"] = signal_commands
        if inter_state_channel_commands is not UNSET:
            field_dict["interStateChannelCommands"] = inter_state_channel_commands
        if command_combinations is not UNSET:
            field_dict["commandCombinations"] = command_combinations

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.command_combination import CommandCombination
        from ..models.inter_state_channel_command import InterStateChannelCommand
        from ..models.signal_command import SignalCommand
        from ..models.timer_command import TimerCommand

        d = src_dict.copy()
        command_waiting_type = CommandWaitingType(d.pop("commandWaitingType"))

        timer_commands = []
        _timer_commands = d.pop("timerCommands", UNSET)
        for timer_commands_item_data in _timer_commands or []:
            timer_commands_item = TimerCommand.from_dict(timer_commands_item_data)

            timer_commands.append(timer_commands_item)

        signal_commands = []
        _signal_commands = d.pop("signalCommands", UNSET)
        for signal_commands_item_data in _signal_commands or []:
            signal_commands_item = SignalCommand.from_dict(signal_commands_item_data)

            signal_commands.append(signal_commands_item)

        inter_state_channel_commands = []
        _inter_state_channel_commands = d.pop("interStateChannelCommands", UNSET)
        for inter_state_channel_commands_item_data in (
            _inter_state_channel_commands or []
        ):
            inter_state_channel_commands_item = InterStateChannelCommand.from_dict(
                inter_state_channel_commands_item_data
            )

            inter_state_channel_commands.append(inter_state_channel_commands_item)

        command_combinations = []
        _command_combinations = d.pop("commandCombinations", UNSET)
        for command_combinations_item_data in _command_combinations or []:
            command_combinations_item = CommandCombination.from_dict(
                command_combinations_item_data
            )

            command_combinations.append(command_combinations_item)

        command_request = cls(
            command_waiting_type=command_waiting_type,
            timer_commands=timer_commands,
            signal_commands=signal_commands,
            inter_state_channel_commands=inter_state_channel_commands,
            command_combinations=command_combinations,
        )

        command_request.additional_properties = d
        return command_request

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
