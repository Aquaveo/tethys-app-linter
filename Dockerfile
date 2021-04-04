FROM python:alpine

RUN python -m pip install pipreqs pyyaml

COPY tethys_app_linter.py /tethys_app_linter.py

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x entrypoint.sh

ENTRYPOINT ["sh", "./entrypoint.sh"]
