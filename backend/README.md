# Backend

## Management API (services)

Services such as the muROMI dataset manager create and follow studies through the API with a token of a staff user:

```sh
python manage.py migrate                      # creates the authtoken table
python manage.py drf_create_token <username>  # use as: Authorization: Token <key>
```

| Endpoint | Purpose |
|---|---|
| `POST /v1/datasets/` | upload a zip archive (multipart: `title`, `archive`) |
| `GET/POST /v1/uis/` | list / create swipe interfaces |
| `GET /v1/groups/` | groups with their members |
| `POST /v1/studies/` | create a study (`title`, `pub_date`, `end_date`, `dataset`, `ui`, optional `group`) |
| `GET /v1/studies/{id}/progress/` | per reviewer: images classified, finished? |
| `GET /v1/export/{id}/results/` | latest answer per reviewer and image as JSON |

All of them require a staff user. Session login keeps working unchanged. Uploads need a matching
`client_max_body_size` in the reverse proxy.

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