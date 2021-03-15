FROM python:3.7-slim

ADD requirements.txt /requirements.txt
RUN pip install --use-deprecated=legacy-resolver -r /requirements.txt

ADD . /py-surveillance
WORKDIR /py-surveillance/
# RUN echo '{"api-key": "{API_KEy}"} ' > config.json
# RUN cat config.json

CMD ["streamlit", "run", "streamlit_show.py", "--server.port", "8080"]
