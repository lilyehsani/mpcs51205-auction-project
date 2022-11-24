FROM python:3.8-alpine
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN apk add -u gcc musl-dev
RUN pip install -r requirements.txt
COPY . /app
CMD python3 auction_queue.py