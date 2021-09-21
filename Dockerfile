FROM python:3.8-slim-buster

RUN apt update && apt install gcc -y
ADD requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

ADD . /py-surveillance
WORKDIR /py-surveillance/
# RUN echo '{"api-key": "{API_KEy}"} ' > config.json
# RUN cat config.json

CMD ["streamlit", "run", "streamlit_show.py", "--server.port", "8080"]
