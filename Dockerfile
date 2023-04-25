FROM python:3.9

WORKDIR /app

COPY ./api /app
COPY ./requirements /app/requirements

RUN pip install -r requirements/production.txt

ENV DJANGO_SETTINGS_MODULE=project.settings.production

RUN  python manage.py collectstatic --noinput

CMD uwsgi --http=0.0.0.0:80 --module=project.wsgi --honour-stdin --post-buffering=1