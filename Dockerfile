FROM python:3.11

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /SolonaVolumeBot

COPY ./requirements.txt ./
RUN pip install gunicorn==19.9.0
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r ./requirements.txt
RUN pip install git+https://github.com/benoitc/gunicorn.git
COPY ./ ./

RUN chmod -R 777 ./
