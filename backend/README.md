# Backend

## Usage

```sh
python manage.py test
python manage.py makemigrations
python manage.py migrate
```

## Setup

```sh
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