FROM python:3.10

ENV PYTHONDONTWRITEBYCODE 1
ENV PYTHONBUFFERED 1

RUN pip install --upgrade pip

WORKDIR /drf_blog

ADD . /drf_blog

RUN pip install -r requirements.txt

COPY . .

ENV C_FORCE_ROOT=true

CMD celery -A drf_blog worker -l info
