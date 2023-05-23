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

### Common Tasks

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
