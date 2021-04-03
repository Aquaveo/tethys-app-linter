FROM python:alpine

RUN python -m pip install flake8

COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
