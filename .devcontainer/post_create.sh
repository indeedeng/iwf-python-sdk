#!/bin/bash

set -ex

git config --global --add safe.directory /workspace

poetry install
