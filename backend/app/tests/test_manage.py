import io
import shutil
import tempfile
import zipfile
from datetime import timedelta

from django.contrib.auth.models import Group
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.utils import timezone
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from app.models import ClassificationUser, Study, User

MEDIA = tempfile.mkdtemp()


def make_zip(names):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        for name in names:
            z.writestr(name, b"\x89PNG\r\n\x1a\n")
    return buf.getvalue()


def client_for(user):
    token, _ = Token.objects.get_or_create(user=user)
    api = APIClient()
    api.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    return api


@override_settings(MEDIA_ROOT=MEDIA)
class ManagementApi(TestCase):
    """What the muROMI dataset manager does: create a study from a crop archive and follow the reviewers."""

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(MEDIA, ignore_errors=True)

    def setUp(self):
        self.admin = User.objects.create_user(username="manager", password="x", is_staff=True, is_superuser=True)
        self.group = Group.objects.create(name="experts")
        self.experts = [User.objects.create_user(username=f"expert{i}", password="x") for i in range(3)]
        for e in self.experts:
            e.groups.add(self.group)

        self.api = client_for(self.admin)

    def create_study(self, files=("a.png", "b.png")):
        dataset = self.api.post("/v1/datasets/", {
            "title": "crops", "archive": SimpleUploadedFile("crops.zip", make_zip(files)),
        }, format="multipart")
        self.assertEqual(dataset.status_code, 201, dataset.content)

        ui = self.api.post("/v1/uis/", {"title": "mf", "labels": {
            "left": {"text": "Non-mitotic", "icon": None, "color": None},
            "right": {"text": "Mitotic figure", "icon": None, "color": None},
            "up": None, "down": None,
        }}, format="json")
        self.assertEqual(ui.status_code, 201, ui.content)

        now = timezone.now()
        study = self.api.post("/v1/studies/", {
            "title": "batch", "description": "d", "pub_date": now.isoformat(),
            "end_date": (now + timedelta(days=365)).isoformat(),
            "group": self.group.id, "anonymous": False,
            "dataset": dataset.json()["id"], "ui": ui.json()["id"],
        }, format="json")
        self.assertEqual(study.status_code, 201, study.content)
        return dataset.json(), study.json()

    def classify(self, study_id, user, index, file, choice):
        ClassificationUser.objects.create(
            date=timezone.now(), user=user, study_id=study_id, file=file, choice=choice, index=index,
        )

    def test_token_required(self):
        self.assertEqual(APIClient().get("/v1/groups/").status_code, 403)
        self.assertEqual(self.api.get("/v1/groups/").status_code, 200)

    def test_non_admin_cannot_manage(self):
        api = client_for(self.experts[0])
        self.assertEqual(api.post("/v1/studies/", {}, format="json").status_code, 403)
        self.assertEqual(api.post("/v1/datasets/", {}, format="multipart").status_code, 403)
        self.assertEqual(api.get("/v1/groups/").status_code, 403)

    def test_dataset_rejects_non_zip(self):
        response = self.api.post("/v1/datasets/", {
            "title": "x", "archive": SimpleUploadedFile("x.zip", b"not a zip"),
        }, format="multipart")
        self.assertEqual(response.status_code, 400)

    def test_groups_list_members(self):
        data = self.api.get("/v1/groups/").json()
        self.assertEqual([m["username"] for m in data[0]["user_set"]], ["expert0", "expert1", "expert2"])

    def test_create_study_lists_files(self):
        dataset, study = self.create_study()
        self.assertEqual(dataset["file_count"], 2)
        self.assertEqual(dataset["file_list"], ["a.png", "b.png"])
        self.assertEqual(Study.objects.get(pk=study["id"]).dataset.file_count, 2)

    def test_study_end_before_start(self):
        _, study = self.create_study()
        created = Study.objects.get(pk=study["id"])
        now = timezone.now()
        response = self.api.post("/v1/studies/", {
            "title": "bad", "pub_date": now.isoformat(), "end_date": (now - timedelta(days=1)).isoformat(),
            "dataset": created.dataset_id, "ui": created.ui_id,
        }, format="json")
        self.assertEqual(response.status_code, 400)

    def test_progress_and_results(self):
        _, study = self.create_study()
        sid = study["id"]

        progress = self.api.get(f"/v1/studies/{sid}/progress/").json()
        self.assertEqual(progress["file_count"], 2)
        self.assertEqual(progress["complete_reviewers"], 0)
        self.assertEqual([r["classified"] for r in progress["reviewers"]], [0, 0, 0])

        # expert0 changes their mind on one image (latest answer wins), expert1 finishes, expert2 is half way.
        # Every reviewer sees their own shuffled order, so the index differs between reviewers.
        self.classify(sid, self.experts[0], 0, "b.png", "left")
        self.classify(sid, self.experts[0], 1, "a.png", "left")
        self.classify(sid, self.experts[0], 1, "a.png", "right")
        self.classify(sid, self.experts[1], 0, "a.png", "right")
        self.classify(sid, self.experts[1], 1, "b.png", "right")
        self.classify(sid, self.experts[2], 0, "a.png", "left")

        progress = self.api.get(f"/v1/studies/{sid}/progress/").json()
        by_user = {r["username"]: r for r in progress["reviewers"]}
        self.assertEqual(by_user["expert0"]["classified"], 2)
        self.assertTrue(by_user["expert0"]["complete"])
        self.assertTrue(by_user["expert1"]["complete"])
        self.assertFalse(by_user["expert2"]["complete"])
        self.assertEqual(progress["complete_reviewers"], 2)

        # the staff overview: study meta, group and the distribution of the latest answers (2 x left, 3 x right)
        self.assertEqual(progress["title"], "batch")
        self.assertEqual(progress["group"], "experts")
        self.assertEqual(progress["dataset_title"], "crops")
        answers = {a["choice"]: (a["label"], a["count"]) for a in progress["answers"]}
        self.assertEqual(answers, {"left": ("Non-mitotic", 2), "right": ("Mitotic figure", 3)})

        results = self.api.get(f"/v1/export/{sid}/results/").json()
        got = {(c["username"], c["file"]): c["label"] for c in results["classifications"]}
        self.assertEqual(got[("expert0", "a.png")], "Mitotic figure")
        self.assertEqual(got[("expert0", "b.png")], "Non-mitotic")
        self.assertEqual(len(got), 5)
        self.assertEqual(results["file_count"], 2)

    def test_overview_of_all_studies_for_staff(self):
        self.create_study()
        self.create_study()
        data = self.api.get("/v1/studies/all/").json()
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["file_count"], 2)
        self.assertEqual([r["username"] for r in data[0]["reviewers"]], ["expert0", "expert1", "expert2"])
        self.assertEqual(client_for(self.experts[0]).get("/v1/studies/all/").status_code, 403)
        self.assertEqual(APIClient().get("/v1/studies/all/").status_code, 403)

    def test_auth_status_tells_staff(self):
        self.assertTrue(self.api.get("/v1/auth/status/").json()["staff"])
        self.assertFalse(client_for(self.experts[0]).get("/v1/auth/status/").json()["staff"])

    def test_progress_requires_admin(self):
        _, study = self.create_study()
        api = client_for(self.experts[0])
        self.assertEqual(api.get(f"/v1/studies/{study['id']}/progress/").status_code, 403)
