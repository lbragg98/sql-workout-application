# SQL Workout Application API

## Project Description
This project is a Flask backend API for a workout tracking app used by personal trainers. It supports creating, viewing, and deleting workouts and exercises, and linking exercises to workouts with reps, sets, or duration data.

## Installation Instructions
From the project root:

```bash
pipenv install
pipenv shell
```

Set Flask app:

```bash
export FLASK_APP=server/app.py
```

Initialize and apply migrations (first time setup):

```bash
flask db init
flask db migrate -m "initial schema"
flask db upgrade
```

Seed the database:

```bash
python server/seed.py
```

## Run Instructions
Run with Flask:

```bash
flask run --port 5555
```

Or run directly:

```bash
python server/app.py
```

API base URL: `http://127.0.0.1:5555`

## API Endpoints
- `GET /workouts`: List all workouts.
- `GET /workouts/<id>`: Show a single workout with its associated exercises and workout_exercise details.
- `POST /workouts`: Create a workout.
- `DELETE /workouts/<id>`: Delete a workout (associated join records are cascade-deleted).
- `GET /exercises`: List all exercises.
- `GET /exercises/<id>`: Show one exercise and its associated workouts.
- `POST /exercises`: Create an exercise.
- `DELETE /exercises/<id>`: Delete an exercise (associated join records are cascade-deleted).
- `POST /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises`: Add an exercise to a workout with reps/sets/duration values.

## Pipfile Dependencies
From `Pipfile`:
- `flask`
- `flask-sqlalchemy`
- `flask-migrate`
- `flask-marshmallow`
- `marshmallow`
- `marshmallow-sqlalchemy`

Dev dependency:
- `ipython`

## Test Files
No automated test files are included in this submission.

