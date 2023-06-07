# Indeed Open Source Repository Template

A default template repository we can use to bootstrap new open source projects. Replace this text with an overview of your project and what it does.

Your README.md should contain the following sections:

## Getting Started

How does a user get started using this project?

## Getting Help

How does a user ask questions if they are stuck?

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

### Running iwf-server locally

#### VSCode Dev Container

Dev Container is an easy way to get iwf-server running locally. Follow these steps to launch a dev container:
- Install Docker, VSCode, and [VSCode Dev Container plugin](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers).
- Open the project in VSCode.
    ```bash
    cd iwf-python-sdk
    code .
    ```
- Launch the Remote-Containers: Reopen in Container command from Command Palette (Ctrl + Shift + P). You can also click in the bottom left corner to access the remote container menu.
- Once the dev container starts, iwf-server will be listening on port 8801.

### Common Tasks

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
poetry run openapi-python-client update --path iwf-idl/iwf-sdk.yaml --config .openapi-python-client-config.yaml
```

#### Linting

To run linting for this project:

```bash
poetry run pre-commit run --show-diff-on-failure --color=always --all-files
```

## Project Maintainers

Who are the project maintainers, and how can they be reached?

## Code of Conduct
This project is governed by the [Contributor Covenant v 1.4.1](CODE_OF_CONDUCT.md). (Review the Code of Conduct and remove this sentence before publishing your project.)

## License
This project uses the [Apache 2.0](LICENSE) license. (Update this and the LICENSE file if your project uses a different license.)
