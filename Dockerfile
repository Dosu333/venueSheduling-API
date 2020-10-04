FROM python:3.8

ENV PYTHONUNBUFFERED=1

RUN mkdir /code 
WORKDIR /code
COPY . /code

COPY requirements.txt /code/
RUN pip install -r requirements.txt
RUN useradd appuser && chown -R appuser /code
USER appuser