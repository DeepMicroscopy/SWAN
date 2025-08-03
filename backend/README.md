# Backend

## Usage

```sh
python manage.py dumpdata | jq 'map(select(.model as $in | ["admin.logentry", "auth.permission", "contenttypes.contenttype", "sessions.session"] | index($in) | not))' > data.json
rm db.sqlite3 && python manage.py makemigrations && python manage.py migrate && python manage.py loaddata data.json && python manage.py runserver
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