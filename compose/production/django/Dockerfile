FROM python:3.6-jessie

ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN apt-get install apt-utils python3-pip git zsh redis-tools nano -y

RUN pip install --upgrade pip

# Requirements are installed here to ensure they will be cached.
COPY ./requirements /requirements
RUN pip install --no-cache-dir -r /requirements/local.txt
RUN pip install --no-cache-dir -r /requirements/production.txt
RUN rm -rf /requirements

COPY ./compose/production/django/entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r//' /entrypoint.sh
RUN chmod +x /entrypoint.sh

# create a local django start to cram everything into one dockerfile since i dislike maintaining two similar
# but different dockerfiles
COPY ./compose/local/django/local_django_start.sh /local_django_start.sh
RUN sed -i 's/\r//' /local_django_start.sh
RUN chmod +x /local_django_start.sh

# this is the actual production start script
COPY ./compose/production/django/start.sh /start.sh
RUN sed -i 's/\r//' /start.sh
RUN chmod +x /start.sh

COPY ./compose/production/django/celery/worker/start.sh /start-celeryworker.sh
RUN sed -i 's/\r//' /start-celeryworker.sh
RUN chmod +x /start-celeryworker.sh

COPY ./compose/production/django/celery/beat/start.sh /start-celerybeat.sh
RUN sed -i 's/\r//' /start-celerybeat.sh
RUN chmod +x /start-celerybeat.sh

RUN wget https://github.com/robbyrussell/oh-my-zsh/raw/master/tools/install.sh -O - | zsh || true
COPY ./compose/.zshrc /root/.zshrc

WORKDIR /app

ENTRYPOINT ["/entrypoint.sh"]
