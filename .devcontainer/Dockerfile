# [Choice] Python version (use -bullseye variants on local arm64/Apple Silicon): 3, 3.10, 3-bullseye, 3.10-bullseye, 3-buster, 3.10-buster
ARG VARIANT=3-bullseye
FROM python:3.10

RUN apt-get update && apt-get install -y \
  gcc \
  && rm -rf /var/lib/apt/lists/*

# Install poetry
RUN pip install poetry==1.4.2
