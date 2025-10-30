# SWipeable ANnotations

SWAN (SWipeable ANnotations) is an open-source, MIT-licensed web application for fast and intuitive histopathology image
annotation. Instead of slow, folder-based sorting, SWAN enables swipe-based classification on both desktop and mobile
devices, supports flexible label mapping, and logs annotations and metadata in real time. Designed to reduce fatigue and
make large-scale annotation more accessible, SWAN offers a lightweight, browser-based interface that allows pathologists
and researchers to efficiently label image patches anytime, including on the go.

## Features

- **Swipe-based annotation** — Classify images by swiping left, right, up, or down.
- **Configurable directions** — Each direction can be assigned to a specific label or disabled entirely.
- **Postpone option** — One swipe direction can be configured to defer decisions for later review.
- **Responsive design** — The UI adapts to desktop, tablet, and mobile devices.
- **Admin dashboard** — Manage studies, upload image sets, and configure UI behavior directly in the Django admin.
- **Anonymous participation** — Users can join via QR code without registration; sessions are tracked using unique
  session IDs.
- **Lightweight deployment** — No Docker or PostgreSQL required; compatible with SQLite for simple hosting.
- **MIT licensed** — Open for academic, personal, or commercial use.

## Architecture

| Component    | Technology       | Description                              |
|--------------|------------------|------------------------------------------|
| **Frontend** | Vue.js + Vuetify | Swipe-based image annotation interface   |
| **Backend**  | Django           | Core logic, API endpoints, and admin     |
| **Database** | SQLite (default) | Can also support PostgreSQL if available |
| **Server**   | Hypercorn        | ASGI server for production deployments   |

## Interface Example

This is the final result of a fully configured application and dataset in educational mode.

![Swipe Interface in Educational Mode](docs/ui-swipe-example.png)

## Getting Started

Run `make dev` to get a development environment up and running.
This will install all python dependencies to a virtual environment and start the development server after creating and
applying the database migrations.
See [frontend/README.md](frontend/README.md) and [backend/README.md](backend/README.md) for more information.

After that run `make -C backend/ admin` in a second terminal to create the `admin` user. You will be prompted for a
password.

You can load example data using `make -C backend/ example` which will create `admin` / `admin` and `expert` / `expert`
users..

## Installation

Run `make` to build frontend and backend in the correct order, including auto-generated api documentation and the
corresponding client using `openapi-fetch`.

After that, use `make run` to start `hypercorn`. Currently, the backend also serves static files to reduce operational complexity.
We recommend caching static paths in the reverse proxy if performance is a concern.

### Production

Set the following environment variables to run the application in production mode:

```env
PRODUCTION=true
API_DOCS=true
ALLOWED_HOSTS=<your-domain-here>
SECRET_KEY=<your-secret-here>
```

## Usage

For a detailed guide on how to use the application, see [docs/usage.md](docs/usage.md).

## Post User-Study Questionnaires

The following are the links to the post-study questionnaires that were filled by the study participants:

SWAN (Initial Phase) - https://forms.gle/N5tsQu185kVoqUki8 <br>
SWAN (Enhanced) - https://forms.gle/fsEnC4iupWuspQHaA

## Security

### Verifying commits

```sh
# configure allowed signers
git config gpg.ssh.allowedSignersFile known_signers

# view signatures for commits
git log --show-signature
```
