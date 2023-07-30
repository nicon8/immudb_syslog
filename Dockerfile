# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /immudb_syslog
ADD /src /src
ADD requirements.txt /immudb_syslog

COPY . .
RUN pip3 install -r requirements.txt
RUN python -m pip install -e .

CMD ["bash"]

#CMD ["python3", "-m" , "flask", "run", "--host=0.0.0.0"]
