from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.context import Context
    from ..models.encoded_object import EncodedObject
    from ..models.key_value import KeyValue
    from ..models.search_attribute import SearchAttribute


T = TypeVar("T", bound="WorkflowWorkerRpcRequest")


@attr.s(auto_attribs=True)
class WorkflowWorkerRpcRequest:
    """
    Attributes:
        context (Context):
        workflow_type (str):
        rpc_name (str):
        input_ (Union[Unset, EncodedObject]):
        search_attributes (Union[Unset, List['SearchAttribute']]):
        data_attributes (Union[Unset, List['KeyValue']]):
    """

    context: "Context"
    workflow_type: str
    rpc_name: str
    input_: Union[Unset, "EncodedObject"] = UNSET
    search_attributes: Union[Unset, List["SearchAttribute"]] = UNSET
    data_attributes: Union[Unset, List["KeyValue"]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        context = self.context.to_dict()

        workflow_type = self.workflow_type
        rpc_name = self.rpc_name
        input_: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.input_, Unset):
            input_ = self.input_.to_dict()

        search_attributes: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.search_attributes, Unset):
            search_attributes = []
            for search_attributes_item_data in self.search_attributes:
                search_attributes_item = search_attributes_item_data.to_dict()

                search_attributes.append(search_attributes_item)

        data_attributes: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.data_attributes, Unset):
            data_attributes = []
            for data_attributes_item_data in self.data_attributes:
                data_attributes_item = data_attributes_item_data.to_dict()

                data_attributes.append(data_attributes_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "context": context,
                "workflowType": workflow_type,
                "rpcName": rpc_name,
            }
        )
        if input_ is not UNSET:
            field_dict["input"] = input_
        if search_attributes is not UNSET:
            field_dict["searchAttributes"] = search_attributes
        if data_attributes is not UNSET:
            field_dict["dataAttributes"] = data_attributes

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.context import Context
        from ..models.encoded_object import EncodedObject
        from ..models.key_value import KeyValue
        from ..models.search_attribute import SearchAttribute

        d = src_dict.copy()
        context = Context.from_dict(d.pop("context"))

        workflow_type = d.pop("workflowType")

        rpc_name = d.pop("rpcName")

        _input_ = d.pop("input", UNSET)
        input_: Union[Unset, EncodedObject]
        if isinstance(_input_, Unset):
            input_ = UNSET
        else:
            input_ = EncodedObject.from_dict(_input_)

        search_attributes = []
        _search_attributes = d.pop("searchAttributes", UNSET)
        for search_attributes_item_data in _search_attributes or []:
            search_attributes_item = SearchAttribute.from_dict(
                search_attributes_item_data
            )

            search_attributes.append(search_attributes_item)

        data_attributes = []
        _data_attributes = d.pop("dataAttributes", UNSET)
        for data_attributes_item_data in _data_attributes or []:
            data_attributes_item = KeyValue.from_dict(data_attributes_item_data)

            data_attributes.append(data_attributes_item)

        workflow_worker_rpc_request = cls(
            context=context,
            workflow_type=workflow_type,
            rpc_name=rpc_name,
            input_=input_,
            search_attributes=search_attributes,
            data_attributes=data_attributes,
        )

        workflow_worker_rpc_request.additional_properties = d
        return workflow_worker_rpc_request

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
