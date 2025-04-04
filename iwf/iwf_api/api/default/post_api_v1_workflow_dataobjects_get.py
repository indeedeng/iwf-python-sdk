from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.error_response import ErrorResponse
from ...models.workflow_get_data_objects_request import WorkflowGetDataObjectsRequest
from ...models.workflow_get_data_objects_response import WorkflowGetDataObjectsResponse
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    json_body: WorkflowGetDataObjectsRequest,
) -> Dict[str, Any]:
    url = "{}/api/v1/workflow/dataobjects/get".format(client.base_url)

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
) -> Optional[Union[ErrorResponse, WorkflowGetDataObjectsResponse]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = WorkflowGetDataObjectsResponse.from_dict(response.json())

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
) -> Response[Union[ErrorResponse, WorkflowGetDataObjectsResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Client,
    json_body: WorkflowGetDataObjectsRequest,
) -> Response[Union[ErrorResponse, WorkflowGetDataObjectsResponse]]:
    """get workflow data objects aka data attributes

    Args:
        json_body (WorkflowGetDataObjectsRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, WorkflowGetDataObjectsResponse]]
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
    json_body: WorkflowGetDataObjectsRequest,
) -> Optional[Union[ErrorResponse, WorkflowGetDataObjectsResponse]]:
    """get workflow data objects aka data attributes

    Args:
        json_body (WorkflowGetDataObjectsRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, WorkflowGetDataObjectsResponse]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    json_body: WorkflowGetDataObjectsRequest,
) -> Response[Union[ErrorResponse, WorkflowGetDataObjectsResponse]]:
    """get workflow data objects aka data attributes

    Args:
        json_body (WorkflowGetDataObjectsRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, WorkflowGetDataObjectsResponse]]
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
    json_body: WorkflowGetDataObjectsRequest,
) -> Optional[Union[ErrorResponse, WorkflowGetDataObjectsResponse]]:
    """get workflow data objects aka data attributes

    Args:
        json_body (WorkflowGetDataObjectsRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, WorkflowGetDataObjectsResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
