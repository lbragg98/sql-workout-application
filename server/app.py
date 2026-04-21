"""Flask application entrypoint and REST API routes."""

from pathlib import Path

from flask import Flask, jsonify, request
from flask_migrate import Migrate
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from models import Exercise, Workout, WorkoutExercise, db
from schemas import (
    exercise_schema,
    exercise_with_workouts_schema,
    exercises_schema,
    ma,
    workout_exercise_schema,
    workout_schema,
    workouts_schema,
)

app = Flask(__name__)
# Use an absolute SQLite path so running from different directories uses the same DB file.
db_path = Path(__file__).resolve().parent / "app.db"
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path.as_posix()}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

migrate = Migrate(app, db)
db.init_app(app)
ma.init_app(app)


@app.errorhandler(ValidationError)
def handle_validation_error(error):
    """Return Marshmallow validation errors in a consistent JSON shape."""
    return jsonify({"errors": error.messages}), 400


@app.route("/workouts", methods=["GET"])
def get_workouts():
    workouts = Workout.query.order_by(Workout.date.desc()).all()
    return workouts_schema.dump(workouts), 200


@app.route("/workouts/<int:id>", methods=["GET"])
def get_workout(id):
    workout = Workout.query.get_or_404(id)
    return workout_schema.dump(workout), 200


@app.route("/workouts", methods=["POST"])
def create_workout():
    data = request.get_json() or {}
    workout = workout_schema.load(data)
    db.session.add(workout)
    db.session.commit()
    return workout_schema.dump(workout), 201


@app.route("/workouts/<int:id>", methods=["DELETE"])
def delete_workout(id):
    workout = Workout.query.get_or_404(id)
    db.session.delete(workout)
    db.session.commit()
    return {"message": f"Workout {id} deleted."}, 200


@app.route("/exercises", methods=["GET"])
def get_exercises():
    exercises = Exercise.query.order_by(Exercise.name.asc()).all()
    return exercises_schema.dump(exercises), 200


@app.route("/exercises/<int:id>", methods=["GET"])
def get_exercise(id):
    exercise = Exercise.query.get_or_404(id)
    return exercise_with_workouts_schema.dump(exercise), 200


@app.route("/exercises", methods=["POST"])
def create_exercise():
    data = request.get_json() or {}
    exercise = exercise_schema.load(data)
    db.session.add(exercise)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return {"error": "Exercise name must be unique."}, 400
    return exercise_schema.dump(exercise), 201


@app.route("/exercises/<int:id>", methods=["DELETE"])
def delete_exercise(id):
    exercise = Exercise.query.get_or_404(id)
    db.session.delete(exercise)
    db.session.commit()
    return {"message": f"Exercise {id} deleted."}, 200


@app.route("/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises", methods=["POST"])
def add_exercise_to_workout(workout_id, exercise_id):
    Workout.query.get_or_404(workout_id)
    Exercise.query.get_or_404(exercise_id)

    payload = request.get_json() or {}
    payload["workout_id"] = workout_id
    payload["exercise_id"] = exercise_id

    workout_exercise = workout_exercise_schema.load(payload)
    db.session.add(workout_exercise)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return {"error": "This exercise is already added to this workout, or data violates constraints."}, 400

    return workout_exercise_schema.dump(workout_exercise), 201


if __name__ == "__main__":
    app.run(port=5555, debug=True)
