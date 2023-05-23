from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.command_carry_over_type import CommandCarryOverType
from ..types import UNSET, Unset

T = TypeVar("T", bound="CommandCarryOverPolicy")


@attr.s(auto_attribs=True)
class CommandCarryOverPolicy:
    """
    Attributes:
        command_carry_over_type (Union[Unset, CommandCarryOverType]):
    """

    command_carry_over_type: Union[Unset, CommandCarryOverType] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        command_carry_over_type: Union[Unset, str] = UNSET
        if not isinstance(self.command_carry_over_type, Unset):
            command_carry_over_type = self.command_carry_over_type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if command_carry_over_type is not UNSET:
            field_dict["commandCarryOverType"] = command_carry_over_type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _command_carry_over_type = d.pop("commandCarryOverType", UNSET)
        command_carry_over_type: Union[Unset, CommandCarryOverType]
        if isinstance(_command_carry_over_type, Unset):
            command_carry_over_type = UNSET
        else:
            command_carry_over_type = CommandCarryOverType(_command_carry_over_type)

        command_carry_over_policy = cls(
            command_carry_over_type=command_carry_over_type,
        )

        command_carry_over_policy.additional_properties = d
        return command_carry_over_policy

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
