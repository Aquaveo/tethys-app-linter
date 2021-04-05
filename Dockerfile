FROM continuumio/miniconda3:4.9.2-alpine

RUN /opt/conda/bin/conda create -n tethys -c tethysplatform -c conda-forge tethys-platform

RUN /bin/bash -c '. /opt/conda/bin/activate tethys \
  ; /opt/conda/bin/conda install pipreqs pyyaml -c conda-forge'

COPY tethys_app_linter.py /tethys_app_linter.py

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x entrypoint.sh

ENTRYPOINT ["sh", "./entrypoint.sh"]
