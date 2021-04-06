FROM continuumio/miniconda3:4.9.2-alpine

RUN /opt/conda/bin/conda create -n tethys -c tethysplatform -c conda-forge tethys-platform

RUN /opt/conda/envs/tethys/bin/python -m pip install pipreqs pyyaml

COPY tethys_app_linter.py /tethys_app_linter.py
COPY tethysapp-test_app /tethysapp-test_app

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x entrypoint.sh

ENTRYPOINT ["sh", "./entrypoint.sh"]
