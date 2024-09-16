FROM python:3.8-slim-buster

RUN apt-get update && \
    apt-get install -y libpq-dev gcc

WORKDIR /app

COPY requirements.txt requirements.txt


RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]