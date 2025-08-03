# Backend

## Docker

```shell
python manage.py makemigrations
docker-compose build && docker-compose up
docker-compose exec swan python manage.py migrate
docker-compose exec swan python manage.py loaddata data.json
docker-compose exec swan python manage.py dumpdata | jq 'map(select(.model as $in | ["admin.logentry", "auth.permission", "contenttypes.contenttype", "sessions.session"] | index($in) | not))' > data.json
```

## Setup

```sh
python manage.py test
python manage.py createsuperuser --username admin --email admin@localhost
```

## Exploring

```sh
python manage.py testserver mydata.json
python manage.py shell
```

## Deployment

```sh
python manage.py check --deploy
```