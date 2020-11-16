FROM ufoym/deepo

COPY requirements.txt /
RUN pip install -r requirements.txt

ENTRYPOINT ["bash", "run.sh"]