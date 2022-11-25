FROM ubuntu:22.04

RUN apt-get update && \
    apt-get install -y python3 python3-pip

COPY . /app

RUN python3 -m pip install -r /app/requirements.txt

ENTRYPOINT [ "python3" ]

CMD [ "app/app.py" ]
