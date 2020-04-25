FROM python:3.6
USER root

RUN apt-get update
WORKDIR /app
COPY . /app
RUN pip install --requirement /app/requirements.txt
CMD [ "python","main.py" ]