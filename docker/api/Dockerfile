FROM python:3.11-slim

RUN useradd -ms /bin/bash python

USER python

WORKDIR /home/python/app

COPY --chown=python src requirements.txt ./

RUN python3 -m pip install --no-cache-dir --no-warn-script-location --upgrade pip && \
    python3 -m pip install --no-cache-dir --no-warn-script-location -r requirements.txt
