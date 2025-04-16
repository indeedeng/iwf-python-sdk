from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.error_sub_status import ErrorSubStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="ErrorResponse")


@_attrs_define
class ErrorResponse:
    """
    Attributes:
        detail (Union[Unset, str]):
        sub_status (Union[Unset, ErrorSubStatus]):
        original_worker_error_detail (Union[Unset, str]):
        original_worker_error_type (Union[Unset, str]):
        original_worker_error_status (Union[Unset, int]):
    """

    detail: Union[Unset, str] = UNSET
    sub_status: Union[Unset, ErrorSubStatus] = UNSET
    original_worker_error_detail: Union[Unset, str] = UNSET
    original_worker_error_type: Union[Unset, str] = UNSET
    original_worker_error_status: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        detail = self.detail

        sub_status: Union[Unset, str] = UNSET
        if not isinstance(self.sub_status, Unset):
            sub_status = self.sub_status.value

        original_worker_error_detail = self.original_worker_error_detail

        original_worker_error_type = self.original_worker_error_type

        original_worker_error_status = self.original_worker_error_status

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if detail is not UNSET:
            field_dict["detail"] = detail
        if sub_status is not UNSET:
            field_dict["subStatus"] = sub_status
        if original_worker_error_detail is not UNSET:
            field_dict["originalWorkerErrorDetail"] = original_worker_error_detail
        if original_worker_error_type is not UNSET:
            field_dict["originalWorkerErrorType"] = original_worker_error_type
        if original_worker_error_status is not UNSET:
            field_dict["originalWorkerErrorStatus"] = original_worker_error_status

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        detail = d.pop("detail", UNSET)

        _sub_status = d.pop("subStatus", UNSET)
        sub_status: Union[Unset, ErrorSubStatus]
        if isinstance(_sub_status, Unset):
            sub_status = UNSET
        else:
            sub_status = ErrorSubStatus(_sub_status)

        original_worker_error_detail = d.pop("originalWorkerErrorDetail", UNSET)

        original_worker_error_type = d.pop("originalWorkerErrorType", UNSET)

        original_worker_error_status = d.pop("originalWorkerErrorStatus", UNSET)

        error_response = cls(
            detail=detail,
            sub_status=sub_status,
            original_worker_error_detail=original_worker_error_detail,
            original_worker_error_type=original_worker_error_type,
            original_worker_error_status=original_worker_error_status,
        )

        error_response.additional_properties = d
        return error_response

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
