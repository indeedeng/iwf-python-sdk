
# iwf-python-sdk

Python SDK for [iWF workflow engine](https://github.com/indeedeng/iwf)

```
pip install iwf-python-sdk==0.2.0
```

See [samples](https://github.com/indeedeng/iwf-python-samples) for use case examples.

## Requirements

- Python 3.9+
- [iWF server](https://github.com/indeedeng/iwf#how-to-use)

## Concepts

To implement a workflow, the two most core interfaces are

* [Workflow interface](https://github.com/indeedeng/iwf-python-sdk/blob/main/iwf/workflow.py)
  defines the workflow definition

* [WorkflowState interface](https://github.com/indeedeng/iwf-python-sdk/blob/main/iwf/workflow_state.py)
  defines the workflow states for workflow definitions

A workflow can contain any number of WorkflowStates.

See more in https://github.com/indeedeng/iwf#what-is-iwf


# Development Plan

## 1.0 -- the basic and most frequently needed features
- [x] Start workflow API
- [x] Executing `wait_until`/`execute` APIs and completing workflow
- [x] Parallel execution of multiple states
- [x] GetWorkflowResultsWithWait API
- [x] StateOption: WaitUntil(optional)/Execute API timeout and retry policy
- [x] Get workflow with wait API
- [x] Timer command
- [x] AnyCommandCompleted and AllCommandCompleted waitingType
- [x] InternalChannel command
- [x] DataAttribute
- [x] Stop workflow API
- [x] Improve workflow uncompleted error return(canceled, failed, timeout, terminated)
- [x] Support execute API failure policy
- [x] Support workflow RPC
- [x] Signal command
- [x] Reset workflow API
- [x] Skip timer API for testing/operation

### Running iwf-server locally

#### Option 1: use docker compose
See [iwf README](https://github.com/indeedeng/iwf#using-docker-image--docker-compose)

#### Option 2: VSCode Dev Container

Dev Container is an easy way to get iwf-server running locally. Follow these steps to launch a dev container:
- Install Docker, VSCode, and [VSCode Dev Container plugin](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers).
- Open the project in VSCode.
    ```bash
    cd iwf-python-sdk
    code .
    ```
- Launch the Remote-Containers: Reopen in Container command from Command Palette (Ctrl + Shift + P). You can also click in the bottom left corner to access the remote container menu.
- Once the dev container starts, iwf-server will be listening on port 8801.

## How To Contribute

This project uses [Poetry](https://python-poetry.org/) as a dependency manager. Check out Poetry's [documentation on how to install it](https://python-poetry.org/docs/#installing-with-the-official-installer) on your system before proceeding.

> ❗Note: If you use Conda or Pyenv as your environment / package manager, avoid dependency conflicts by doing the following first:
1. Before installing Poetry, create and activate a new Conda env (e.g. conda create -n langchain python=3.9)
2. Install Poetry (see above)
3. Tell Poetry to use the virtualenv python environment (poetry config virtualenvs.prefer-active-python true)
4. Continue with the following steps.

To install requirements:

```bash
poetry install
```

#### Update IDL
Initialize the IDL Git submodule
```bash
git submodule update --init --recursive
```

Update IDL to the latest commit.
```bash
git submodule update --remote --merge
```

#### Generate API client from IDL

This project uses [openapi-python-client](https://github.com/openapi-generators/openapi-python-client) to generate an API client from the IDL. To update the generated client:

```bash
mkdir iwf/iwf_api/iwf_api
cd iwf && poetry run openapi-python-client update --path ../iwf-idl/iwf-sdk.yaml --config .openapi-python-client-config.yaml
cd .. && cp -R iwf/iwf_api/iwf_api/* iwf/iwf_api && rm -R iwf/iwf_api/iwf_api && poetry update
```

The last command will:
* Fix the api package path
* Update the local path dependency.
#### Linting

To run linting for this project:

```bash
poetry run pre-commit run --show-diff-on-failure --color=always --all-files
```

## Code of Conduct
This project is governed by the [Contributor Covenant v 1.4.1](CODE_OF_CONDUCT.md). (Review the Code of Conduct and remove this sentence before publishing your project.)

## License
This project uses the [Apache 2.0](LICENSE) license. (Update this and the LICENSE file if your project uses a different license.)
