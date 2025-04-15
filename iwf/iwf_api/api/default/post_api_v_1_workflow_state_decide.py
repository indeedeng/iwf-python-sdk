from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.worker_error_response import WorkerErrorResponse
from ...models.workflow_state_execute_request import WorkflowStateExecuteRequest
from ...models.workflow_state_execute_response import WorkflowStateExecuteResponse
from ...types import Response


def _get_kwargs(
    *,
    body: WorkflowStateExecuteRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/workflowState/decide",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[WorkerErrorResponse, WorkflowStateExecuteResponse]]:
    if response.status_code == 200:
        response_200 = WorkflowStateExecuteResponse.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = WorkerErrorResponse.from_dict(response.json())

        return response_400
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[WorkerErrorResponse, WorkflowStateExecuteResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: WorkflowStateExecuteRequest,
) -> Response[Union[WorkerErrorResponse, WorkflowStateExecuteResponse]]:
    """for invoking WorkflowState.execute API

    Args:
        body (WorkflowStateExecuteRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[WorkerErrorResponse, WorkflowStateExecuteResponse]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    body: WorkflowStateExecuteRequest,
) -> Optional[Union[WorkerErrorResponse, WorkflowStateExecuteResponse]]:
    """for invoking WorkflowState.execute API

    Args:
        body (WorkflowStateExecuteRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[WorkerErrorResponse, WorkflowStateExecuteResponse]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: WorkflowStateExecuteRequest,
) -> Response[Union[WorkerErrorResponse, WorkflowStateExecuteResponse]]:
    """for invoking WorkflowState.execute API

    Args:
        body (WorkflowStateExecuteRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[WorkerErrorResponse, WorkflowStateExecuteResponse]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: WorkflowStateExecuteRequest,
) -> Optional[Union[WorkerErrorResponse, WorkflowStateExecuteResponse]]:
    """for invoking WorkflowState.execute API

    Args:
        body (WorkflowStateExecuteRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[WorkerErrorResponse, WorkflowStateExecuteResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
