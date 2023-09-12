from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.timer_status import TimerStatus

T = TypeVar("T", bound="TimerResult")


@attr.s(auto_attribs=True)
class TimerResult:
    """
    Attributes:
        command_id (str):
        timer_status (TimerStatus):
    """

    command_id: str
    timer_status: TimerStatus
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        command_id = self.command_id
        timer_status = self.timer_status.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "commandId": command_id,
                "timerStatus": timer_status,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        command_id = d.pop("commandId")

        timer_status = TimerStatus(d.pop("timerStatus"))

        timer_result = cls(
            command_id=command_id,
            timer_status=timer_status,
        )

        timer_result.additional_properties = d
        return timer_result

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
