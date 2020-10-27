FROM python:3.6

EXPOSE 5000

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get install -y
RUN apt-get -y install curl
RUN apt-get install -y unixodbc-dev
RUN apt-get install -y python3-dev
RUN pip install -r requirements.txt

CMD python webplots.py