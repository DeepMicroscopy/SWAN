import json
from functools import wraps
from pathlib import Path

from django.core.serializers.json import DjangoJSONEncoder

from app.models import User

FIXTURE_OUTPUT_DIR = Path(__file__).resolve().parent.parent.parent.parent / "frontend" / "cypress" / "fixtures"
assert FIXTURE_OUTPUT_DIR.exists()

DEFAULT_USER = 'test-user'
DEFAULT_PASSWORD = 'test-pass'

# do not add the file suffix here, as otherwise the refactoring will not pick up the string
def save_fixture(path: Path, name: str, data):
    #print(f"saving fixture: {path}/{name}")
    with open(FIXTURE_OUTPUT_DIR / path / f"{name}", "w", encoding="utf-8") as f:
        json.dump(data, f, cls=DjangoJSONEncoder, indent=2)


def with_testuser(func, username=DEFAULT_USER, password=DEFAULT_PASSWORD):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        self.user = User.objects.create_user(username=username, password=password)
        return func(self, *args, **kwargs)

    return wrapper


def with_login(func, username=DEFAULT_USER, password=DEFAULT_PASSWORD):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        assert self.client.login(username=username, password=password)
        return func(self, *args, **kwargs)

    return wrapper
