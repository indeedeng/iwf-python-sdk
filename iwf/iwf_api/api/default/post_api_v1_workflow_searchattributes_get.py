from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.error_response import ErrorResponse
from ...models.workflow_get_search_attributes_request import (
    WorkflowGetSearchAttributesRequest,
)
from ...models.workflow_get_search_attributes_response import (
    WorkflowGetSearchAttributesResponse,
)
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    json_body: WorkflowGetSearchAttributesRequest,
) -> Dict[str, Any]:
    url = "{}/api/v1/workflow/searchattributes/get".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
        "json": json_json_body,
    }


def _parse_response(
    *, client: Client, response: httpx.Response
) -> Optional[Union[ErrorResponse, WorkflowGetSearchAttributesResponse]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = WorkflowGetSearchAttributesResponse.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = ErrorResponse.from_dict(response.json())

        return response_400
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[ErrorResponse, WorkflowGetSearchAttributesResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Client,
    json_body: WorkflowGetSearchAttributesRequest,
) -> Response[Union[ErrorResponse, WorkflowGetSearchAttributesResponse]]:
    """get workflow search attributes

    Args:
        json_body (WorkflowGetSearchAttributesRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, WorkflowGetSearchAttributesResponse]]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Client,
    json_body: WorkflowGetSearchAttributesRequest,
) -> Optional[Union[ErrorResponse, WorkflowGetSearchAttributesResponse]]:
    """get workflow search attributes

    Args:
        json_body (WorkflowGetSearchAttributesRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, WorkflowGetSearchAttributesResponse]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    json_body: WorkflowGetSearchAttributesRequest,
) -> Response[Union[ErrorResponse, WorkflowGetSearchAttributesResponse]]:
    """get workflow search attributes

    Args:
        json_body (WorkflowGetSearchAttributesRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, WorkflowGetSearchAttributesResponse]]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client,
    json_body: WorkflowGetSearchAttributesRequest,
) -> Optional[Union[ErrorResponse, WorkflowGetSearchAttributesResponse]]:
    """get workflow search attributes

    Args:
        json_body (WorkflowGetSearchAttributesRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, WorkflowGetSearchAttributesResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
