FROM python:3.8-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app
COPY requirements.txt ./

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY ./entrypoint.sh ./entrypoint.sh
COPY . .
RUN chmod -R 777  ./entrypoint.sh
ENTRYPOINT ["bash", "./entrypoint.sh" ]
