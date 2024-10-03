from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.encoded_object import EncodedObject
    from ..models.persistence_loading_policy import PersistenceLoadingPolicy
    from ..models.search_attribute_key_and_type import SearchAttributeKeyAndType


T = TypeVar("T", bound="WorkflowRpcRequest")


@attr.s(auto_attribs=True)
class WorkflowRpcRequest:
    """
    Attributes:
        workflow_id (str):
        rpc_name (str):
        workflow_run_id (Union[Unset, str]):
        input_ (Union[Unset, EncodedObject]):
        search_attributes_loading_policy (Union[Unset, PersistenceLoadingPolicy]):
        data_attributes_loading_policy (Union[Unset, PersistenceLoadingPolicy]):
        timeout_seconds (Union[Unset, int]):
        use_memo_for_data_attributes (Union[Unset, bool]):
        search_attributes (Union[Unset, List['SearchAttributeKeyAndType']]):
    """

    workflow_id: str
    rpc_name: str
    workflow_run_id: Union[Unset, str] = UNSET
    input_: Union[Unset, "EncodedObject"] = UNSET
    search_attributes_loading_policy: Union[Unset, "PersistenceLoadingPolicy"] = UNSET
    data_attributes_loading_policy: Union[Unset, "PersistenceLoadingPolicy"] = UNSET
    timeout_seconds: Union[Unset, int] = UNSET
    use_memo_for_data_attributes: Union[Unset, bool] = UNSET
    search_attributes: Union[Unset, List["SearchAttributeKeyAndType"]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        workflow_id = self.workflow_id
        rpc_name = self.rpc_name
        workflow_run_id = self.workflow_run_id
        input_: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.input_, Unset):
            input_ = self.input_.to_dict()

        search_attributes_loading_policy: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.search_attributes_loading_policy, Unset):
            search_attributes_loading_policy = (
                self.search_attributes_loading_policy.to_dict()
            )

        data_attributes_loading_policy: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.data_attributes_loading_policy, Unset):
            data_attributes_loading_policy = (
                self.data_attributes_loading_policy.to_dict()
            )

        timeout_seconds = self.timeout_seconds
        use_memo_for_data_attributes = self.use_memo_for_data_attributes
        search_attributes: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.search_attributes, Unset):
            search_attributes = []
            for search_attributes_item_data in self.search_attributes:
                search_attributes_item = search_attributes_item_data.to_dict()

                search_attributes.append(search_attributes_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "workflowId": workflow_id,
                "rpcName": rpc_name,
            }
        )
        if workflow_run_id is not UNSET:
            field_dict["workflowRunId"] = workflow_run_id
        if input_ is not UNSET:
            field_dict["input"] = input_
        if search_attributes_loading_policy is not UNSET:
            field_dict["searchAttributesLoadingPolicy"] = (
                search_attributes_loading_policy
            )
        if data_attributes_loading_policy is not UNSET:
            field_dict["dataAttributesLoadingPolicy"] = data_attributes_loading_policy
        if timeout_seconds is not UNSET:
            field_dict["timeoutSeconds"] = timeout_seconds
        if use_memo_for_data_attributes is not UNSET:
            field_dict["useMemoForDataAttributes"] = use_memo_for_data_attributes
        if search_attributes is not UNSET:
            field_dict["searchAttributes"] = search_attributes

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.encoded_object import EncodedObject
        from ..models.persistence_loading_policy import PersistenceLoadingPolicy
        from ..models.search_attribute_key_and_type import SearchAttributeKeyAndType

        d = src_dict.copy()
        workflow_id = d.pop("workflowId")

        rpc_name = d.pop("rpcName")

        workflow_run_id = d.pop("workflowRunId", UNSET)

        _input_ = d.pop("input", UNSET)
        input_: Union[Unset, EncodedObject]
        if isinstance(_input_, Unset):
            input_ = UNSET
        else:
            input_ = EncodedObject.from_dict(_input_)

        _search_attributes_loading_policy = d.pop(
            "searchAttributesLoadingPolicy", UNSET
        )
        search_attributes_loading_policy: Union[Unset, PersistenceLoadingPolicy]
        if isinstance(_search_attributes_loading_policy, Unset):
            search_attributes_loading_policy = UNSET
        else:
            search_attributes_loading_policy = PersistenceLoadingPolicy.from_dict(
                _search_attributes_loading_policy
            )

        _data_attributes_loading_policy = d.pop("dataAttributesLoadingPolicy", UNSET)
        data_attributes_loading_policy: Union[Unset, PersistenceLoadingPolicy]
        if isinstance(_data_attributes_loading_policy, Unset):
            data_attributes_loading_policy = UNSET
        else:
            data_attributes_loading_policy = PersistenceLoadingPolicy.from_dict(
                _data_attributes_loading_policy
            )

        timeout_seconds = d.pop("timeoutSeconds", UNSET)

        use_memo_for_data_attributes = d.pop("useMemoForDataAttributes", UNSET)

        search_attributes = []
        _search_attributes = d.pop("searchAttributes", UNSET)
        for search_attributes_item_data in _search_attributes or []:
            search_attributes_item = SearchAttributeKeyAndType.from_dict(
                search_attributes_item_data
            )

            search_attributes.append(search_attributes_item)

        workflow_rpc_request = cls(
            workflow_id=workflow_id,
            rpc_name=rpc_name,
            workflow_run_id=workflow_run_id,
            input_=input_,
            search_attributes_loading_policy=search_attributes_loading_policy,
            data_attributes_loading_policy=data_attributes_loading_policy,
            timeout_seconds=timeout_seconds,
            use_memo_for_data_attributes=use_memo_for_data_attributes,
            search_attributes=search_attributes,
        )

        workflow_rpc_request.additional_properties = d
        return workflow_rpc_request

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
