from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.worker_error_response import WorkerErrorResponse
from ...models.workflow_worker_rpc_request import WorkflowWorkerRpcRequest
from ...models.workflow_worker_rpc_response import WorkflowWorkerRpcResponse
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    json_body: WorkflowWorkerRpcRequest,
) -> Dict[str, Any]:
    url = "{}/api/v1/workflowWorker/rpc".format(client.base_url)

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
) -> Optional[Union[WorkerErrorResponse, WorkflowWorkerRpcResponse]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = WorkflowWorkerRpcResponse.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = WorkerErrorResponse.from_dict(response.json())

        return response_400
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[WorkerErrorResponse, WorkflowWorkerRpcResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Client,
    json_body: WorkflowWorkerRpcRequest,
) -> Response[Union[WorkerErrorResponse, WorkflowWorkerRpcResponse]]:
    """for invoking workflow RPC API in the worker

    Args:
        json_body (WorkflowWorkerRpcRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[WorkerErrorResponse, WorkflowWorkerRpcResponse]]
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
    json_body: WorkflowWorkerRpcRequest,
) -> Optional[Union[WorkerErrorResponse, WorkflowWorkerRpcResponse]]:
    """for invoking workflow RPC API in the worker

    Args:
        json_body (WorkflowWorkerRpcRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[WorkerErrorResponse, WorkflowWorkerRpcResponse]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    json_body: WorkflowWorkerRpcRequest,
) -> Response[Union[WorkerErrorResponse, WorkflowWorkerRpcResponse]]:
    """for invoking workflow RPC API in the worker

    Args:
        json_body (WorkflowWorkerRpcRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[WorkerErrorResponse, WorkflowWorkerRpcResponse]]
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
    json_body: WorkflowWorkerRpcRequest,
) -> Optional[Union[WorkerErrorResponse, WorkflowWorkerRpcResponse]]:
    """for invoking workflow RPC API in the worker

    Args:
        json_body (WorkflowWorkerRpcRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[WorkerErrorResponse, WorkflowWorkerRpcResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
