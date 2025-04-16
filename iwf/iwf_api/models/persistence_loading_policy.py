from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.persistence_loading_type import PersistenceLoadingType
from ..types import UNSET, Unset

T = TypeVar("T", bound="PersistenceLoadingPolicy")


@_attrs_define
class PersistenceLoadingPolicy:
    """
    Attributes:
        persistence_loading_type (Union[Unset, PersistenceLoadingType]):
        partial_loading_keys (Union[Unset, list[str]]):
        locking_keys (Union[Unset, list[str]]):
        use_key_as_prefix (Union[Unset, bool]):
    """

    persistence_loading_type: Union[Unset, PersistenceLoadingType] = UNSET
    partial_loading_keys: Union[Unset, list[str]] = UNSET
    locking_keys: Union[Unset, list[str]] = UNSET
    use_key_as_prefix: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        persistence_loading_type: Union[Unset, str] = UNSET
        if not isinstance(self.persistence_loading_type, Unset):
            persistence_loading_type = self.persistence_loading_type.value

        partial_loading_keys: Union[Unset, list[str]] = UNSET
        if not isinstance(self.partial_loading_keys, Unset):
            partial_loading_keys = self.partial_loading_keys

        locking_keys: Union[Unset, list[str]] = UNSET
        if not isinstance(self.locking_keys, Unset):
            locking_keys = self.locking_keys

        use_key_as_prefix = self.use_key_as_prefix

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if persistence_loading_type is not UNSET:
            field_dict["persistenceLoadingType"] = persistence_loading_type
        if partial_loading_keys is not UNSET:
            field_dict["partialLoadingKeys"] = partial_loading_keys
        if locking_keys is not UNSET:
            field_dict["lockingKeys"] = locking_keys
        if use_key_as_prefix is not UNSET:
            field_dict["useKeyAsPrefix"] = use_key_as_prefix

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _persistence_loading_type = d.pop("persistenceLoadingType", UNSET)
        persistence_loading_type: Union[Unset, PersistenceLoadingType]
        if isinstance(_persistence_loading_type, Unset):
            persistence_loading_type = UNSET
        else:
            persistence_loading_type = PersistenceLoadingType(_persistence_loading_type)

        partial_loading_keys = cast(list[str], d.pop("partialLoadingKeys", UNSET))

        locking_keys = cast(list[str], d.pop("lockingKeys", UNSET))

        use_key_as_prefix = d.pop("useKeyAsPrefix", UNSET)

        persistence_loading_policy = cls(
            persistence_loading_type=persistence_loading_type,
            partial_loading_keys=partial_loading_keys,
            locking_keys=locking_keys,
            use_key_as_prefix=use_key_as_prefix,
        )

        persistence_loading_policy.additional_properties = d
        return persistence_loading_policy

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
