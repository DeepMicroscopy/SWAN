# Backend

## Testing

Generates fixtures for the frontend:

```sh
./manage.py test
```

## Exploring

```sh
./manage.py testserver data.json
./manage.py shell
./manage.py dbshell
```

## Example data

```sh
./manage.py dumpdata | jq 'map(select(.model as $in | ["admin.logentry", "auth.permission", "contenttypes.contenttype", "sessions.session"] | index($in) | not))' > data.json
```