# DevTrack

A small backend API for tracking engineering issues, built with plain Django.
Reporters file issues, and issues have a priority and a status.

## How to run

1. Clone the repo and open the folder.
2. Create and activate a virtual environment:

       python -m venv .venv
       .venv\Scripts\activate

3. Install dependencies:

       pip install -r requirements.txt

4. Start the server:

       python manage.py runserver

The API is then available at http://127.0.0.1:8000/api/

## Endpoints

| Method | URL | What it does |
|---|---|---|
| POST | /api/reporters/ | Create a reporter |
| GET | /api/reporters/ | List all reporters |
| GET | /api/reporters/?id=1 | Get one reporter |
| POST | /api/issues/ | Create an issue |
| GET | /api/issues/ | List all issues |
| GET | /api/issues/?id=1 | Get one issue |
| GET | /api/issues/?status=open | List issues with a given status |

Status codes: 201 on create, 400 on invalid input, 404 when not found.

## Project structure

- `issues/models.py` has the OOP classes: `BaseEntity` (abstract), `Reporter`,
  `Issue`, `CriticalIssue`, `LowPriorityIssue`.
- `issues/views.py` has the endpoints and the JSON file helpers.
- Data is stored in `reporters.json` and `issues.json`.

## Design decision

[Write your own: one decision and why. Ideas are below.]

## Screenshots

![Create issue, success](screenshots/post-issue-success.png)
![Create issue, empty title](screenshots/post-issue-empty-title.png)
![Issue not found](screenshots/get-issue-not-found.png)
![Filter by status](screenshots/get-issues-by-status.png)