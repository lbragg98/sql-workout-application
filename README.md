# sql-workout-application

Workout tracking backend API for personal trainers using Flask, SQLAlchemy, Marshmallow, and Flask-Migrate.

## Features
- Create, view, and delete workouts
- Create, view, and delete exercises
- Add an exercise to a workout through a join table (`workout_exercises`)
- SQL table constraints, model-level validations, and schema-level validations

## Tech Stack
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-Marshmallow
- Marshmallow
- SQLite

## Project Structure
- `server/app.py` - app setup and routes
- `server/models.py` - database models, relationships, and model validations
- `server/schemas.py` - serialization/deserialization and schema validations
- `server/seed.py` - reset and seed example data

## Setup
1. Install dependencies:
```bash
pipenv install
```

2. Activate shell:
```bash
pipenv shell
```

3. Set Flask app:
```bash
set FLASK_APP=server/app.py
```

4. Initialize and run migrations:
```bash
flask db init
flask db migrate -m "initial workout schema"
flask db upgrade
```

5. Seed database:
```bash
python server/seed.py
```

6. Run server:
```bash
python server/app.py
```

Server runs on `http://127.0.0.1:5555`.

## Endpoints
### Workouts
- `GET /workouts`
- `GET /workouts/<id>`
- `POST /workouts`
- `DELETE /workouts/<id>`

### Exercises
- `GET /exercises`
- `GET /exercises/<id>`
- `POST /exercises`
- `DELETE /exercises/<id>`

### Join Resource
- `POST /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises`

## Example JSON Payloads
Create exercise (`POST /exercises`):
```json
{
  "name": "Goblet Squat",
  "category": "strength",
  "equipment_needed": true
}
```

Create workout (`POST /workouts`):
```json
{
  "date": "2026-04-21",
  "duration_minutes": 40,
  "notes": "Lower body + conditioning"
}
```

Add exercise to workout (`POST /workouts/1/exercises/2/workout_exercises`):
```json
{
  "reps": 10,
  "sets": 4,
  "duration_seconds": null
}
```

## Validation Highlights
- Table constraints:
  - positive duration, reps, sets, and duration_seconds
  - unique `(workout_id, exercise_id)` pair in join table
  - at least one of reps/sets/duration_seconds must be present in join row
- Model validations:
  - category must be from allowed values
  - workout date cannot be in the future
  - duration must be within allowed range
- Schema validations:
  - payload-level checks for required metrics and field bounds

## Notes
- No update actions are implemented (per spec).
- Exercise removal from workout is not implemented (per spec).
- Deleting workouts/exercises cascades through join records.