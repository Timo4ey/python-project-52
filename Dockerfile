FROM python:3.11.0


ENV PYTHONDONTWRITEBYCODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

RUN apt -qy update && apt -qy install gcc gettext cron openssh-client flake8 vim

WORKDIR /app

COPY . .

RUN apt -yq update && pip install poetry && make install

RUN make makemigrations migrate syncdb
RUN make collectstatic

CMD [ "make", "start"]