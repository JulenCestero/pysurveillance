FROM python:3

ADD . /py-surveillance
WORKDIR /py-surveillance/

RUN pip install -r requirements.txt
RUN echo '{"api-key": "{API_KEy}"} ' > config.json
RUN cat config.json

CMD ["streamlit", "run", "streamlit_show.py"]
