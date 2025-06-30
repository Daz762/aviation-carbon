FROM python:3.12-slim

RUN mkdir aviation-carbon

COPY src aviation-carbon
COPY tests aviation-carbon
COPY pyproject.toml aviation-carbon
COPY requirements.txt aviation-carbon
COPY setup.py aviation-carbon

RUN pip install -r aviation-carbon/requirements.txt
RUN pip install ./aviation-carbon >> build.log

ENV CARBON_INTERFACE=""
ENV SHARPAPI=""

WORKDIR ./aviation-carbon