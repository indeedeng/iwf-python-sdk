from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.inter_state_channel_result import InterStateChannelResult
    from ..models.signal_result import SignalResult
    from ..models.timer_result import TimerResult


T = TypeVar("T", bound="CommandResults")


@attr.s(auto_attribs=True)
class CommandResults:
    """
    Attributes:
        signal_results (Union[Unset, List['SignalResult']]):
        inter_state_channel_results (Union[Unset, List['InterStateChannelResult']]):
        timer_results (Union[Unset, List['TimerResult']]):
        state_start_api_succeeded (Union[Unset, bool]):
    """

    signal_results: Union[Unset, List["SignalResult"]] = UNSET
    inter_state_channel_results: Union[Unset, List["InterStateChannelResult"]] = UNSET
    timer_results: Union[Unset, List["TimerResult"]] = UNSET
    state_start_api_succeeded: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        signal_results: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.signal_results, Unset):
            signal_results = []
            for signal_results_item_data in self.signal_results:
                signal_results_item = signal_results_item_data.to_dict()

                signal_results.append(signal_results_item)

        inter_state_channel_results: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.inter_state_channel_results, Unset):
            inter_state_channel_results = []
            for (
                inter_state_channel_results_item_data
            ) in self.inter_state_channel_results:
                inter_state_channel_results_item = (
                    inter_state_channel_results_item_data.to_dict()
                )

                inter_state_channel_results.append(inter_state_channel_results_item)

        timer_results: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.timer_results, Unset):
            timer_results = []
            for timer_results_item_data in self.timer_results:
                timer_results_item = timer_results_item_data.to_dict()

                timer_results.append(timer_results_item)

        state_start_api_succeeded = self.state_start_api_succeeded

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if signal_results is not UNSET:
            field_dict["signalResults"] = signal_results
        if inter_state_channel_results is not UNSET:
            field_dict["interStateChannelResults"] = inter_state_channel_results
        if timer_results is not UNSET:
            field_dict["timerResults"] = timer_results
        if state_start_api_succeeded is not UNSET:
            field_dict["stateStartApiSucceeded"] = state_start_api_succeeded

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.inter_state_channel_result import InterStateChannelResult
        from ..models.signal_result import SignalResult
        from ..models.timer_result import TimerResult

        d = src_dict.copy()
        signal_results = []
        _signal_results = d.pop("signalResults", UNSET)
        for signal_results_item_data in _signal_results or []:
            signal_results_item = SignalResult.from_dict(signal_results_item_data)

            signal_results.append(signal_results_item)

        inter_state_channel_results = []
        _inter_state_channel_results = d.pop("interStateChannelResults", UNSET)
        for inter_state_channel_results_item_data in _inter_state_channel_results or []:
            inter_state_channel_results_item = InterStateChannelResult.from_dict(
                inter_state_channel_results_item_data
            )

            inter_state_channel_results.append(inter_state_channel_results_item)

        timer_results = []
        _timer_results = d.pop("timerResults", UNSET)
        for timer_results_item_data in _timer_results or []:
            timer_results_item = TimerResult.from_dict(timer_results_item_data)

            timer_results.append(timer_results_item)

        state_start_api_succeeded = d.pop("stateStartApiSucceeded", UNSET)

        command_results = cls(
            signal_results=signal_results,
            inter_state_channel_results=inter_state_channel_results,
            timer_results=timer_results,
            state_start_api_succeeded=state_start_api_succeeded,
        )

        command_results.additional_properties = d
        return command_results

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
