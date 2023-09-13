from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.encoded_object import EncodedObject


T = TypeVar("T", bound="WorkflowRpcResponse")


@attr.s(auto_attribs=True)
class WorkflowRpcResponse:
    """
    Attributes:
        output (Union[Unset, EncodedObject]):
    """

    output: Union[Unset, "EncodedObject"] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        output: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.output, Unset):
            output = self.output.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if output is not UNSET:
            field_dict["output"] = output

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.encoded_object import EncodedObject

        d = src_dict.copy()
        _output = d.pop("output", UNSET)
        output: Union[Unset, EncodedObject]
        if isinstance(_output, Unset):
            output = UNSET
        else:
            output = EncodedObject.from_dict(_output)

        workflow_rpc_response = cls(
            output=output,
        )

        workflow_rpc_response.additional_properties = d
        return workflow_rpc_response

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
