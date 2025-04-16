from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.key_value import KeyValue


T = TypeVar("T", bound="WorkflowSetDataObjectsRequest")


@_attrs_define
class WorkflowSetDataObjectsRequest:
    """
    Attributes:
        workflow_id (str):
        workflow_run_id (Union[Unset, str]):
        objects (Union[Unset, list['KeyValue']]):
    """

    workflow_id: str
    workflow_run_id: Union[Unset, str] = UNSET
    objects: Union[Unset, list["KeyValue"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        workflow_id = self.workflow_id

        workflow_run_id = self.workflow_run_id

        objects: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.objects, Unset):
            objects = []
            for objects_item_data in self.objects:
                objects_item = objects_item_data.to_dict()
                objects.append(objects_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "workflowId": workflow_id,
            }
        )
        if workflow_run_id is not UNSET:
            field_dict["workflowRunId"] = workflow_run_id
        if objects is not UNSET:
            field_dict["objects"] = objects

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.key_value import KeyValue

        d = dict(src_dict)
        workflow_id = d.pop("workflowId")

        workflow_run_id = d.pop("workflowRunId", UNSET)

        objects = []
        _objects = d.pop("objects", UNSET)
        for objects_item_data in _objects or []:
            objects_item = KeyValue.from_dict(objects_item_data)

            objects.append(objects_item)

        workflow_set_data_objects_request = cls(
            workflow_id=workflow_id,
            workflow_run_id=workflow_run_id,
            objects=objects,
        )

        workflow_set_data_objects_request.additional_properties = d
        return workflow_set_data_objects_request

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
