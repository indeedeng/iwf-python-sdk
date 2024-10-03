from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="RetryPolicy")


@attr.s(auto_attribs=True)
class RetryPolicy:
    """
    Attributes:
        initial_interval_seconds (Union[Unset, int]):
        backoff_coefficient (Union[Unset, float]):
        maximum_interval_seconds (Union[Unset, int]):
        maximum_attempts (Union[Unset, int]):
        maximum_attempts_duration_seconds (Union[Unset, int]):
    """

    initial_interval_seconds: Union[Unset, int] = UNSET
    backoff_coefficient: Union[Unset, float] = UNSET
    maximum_interval_seconds: Union[Unset, int] = UNSET
    maximum_attempts: Union[Unset, int] = UNSET
    maximum_attempts_duration_seconds: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        initial_interval_seconds = self.initial_interval_seconds
        backoff_coefficient = self.backoff_coefficient
        maximum_interval_seconds = self.maximum_interval_seconds
        maximum_attempts = self.maximum_attempts
        maximum_attempts_duration_seconds = self.maximum_attempts_duration_seconds

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if initial_interval_seconds is not UNSET:
            field_dict["initialIntervalSeconds"] = initial_interval_seconds
        if backoff_coefficient is not UNSET:
            field_dict["backoffCoefficient"] = backoff_coefficient
        if maximum_interval_seconds is not UNSET:
            field_dict["maximumIntervalSeconds"] = maximum_interval_seconds
        if maximum_attempts is not UNSET:
            field_dict["maximumAttempts"] = maximum_attempts
        if maximum_attempts_duration_seconds is not UNSET:
            field_dict["maximumAttemptsDurationSeconds"] = (
                maximum_attempts_duration_seconds
            )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        initial_interval_seconds = d.pop("initialIntervalSeconds", UNSET)

        backoff_coefficient = d.pop("backoffCoefficient", UNSET)

        maximum_interval_seconds = d.pop("maximumIntervalSeconds", UNSET)

        maximum_attempts = d.pop("maximumAttempts", UNSET)

        maximum_attempts_duration_seconds = d.pop(
            "maximumAttemptsDurationSeconds", UNSET
        )

        retry_policy = cls(
            initial_interval_seconds=initial_interval_seconds,
            backoff_coefficient=backoff_coefficient,
            maximum_interval_seconds=maximum_interval_seconds,
            maximum_attempts=maximum_attempts,
            maximum_attempts_duration_seconds=maximum_attempts_duration_seconds,
        )

        retry_policy.additional_properties = d
        return retry_policy

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
