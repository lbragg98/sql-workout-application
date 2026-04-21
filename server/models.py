from datetime import date

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint, UniqueConstraint
from sqlalchemy.orm import validates


db = SQLAlchemy()


class Exercise(db.Model):
    __tablename__ = "exercises"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    category = db.Column(db.String(50), nullable=False)
    equipment_needed = db.Column(db.Boolean, nullable=False, default=False)

    workout_exercises = db.relationship(
        "WorkoutExercise",
        back_populates="exercise",
        cascade="all, delete-orphan",
    )
    workouts = db.relationship(
        "Workout",
        secondary="workout_exercises",
        back_populates="exercises",
        viewonly=True,
    )

    __table_args__ = (
        CheckConstraint("LENGTH(TRIM(name)) >= 2", name="ck_exercise_name_len"),
    )

    @validates("name")
    def validate_name(self, _key, value):
        if not value or len(value.strip()) < 2:
            raise ValueError("Exercise name must be at least 2 characters.")
        return value.strip()

    @validates("category")
    def validate_category(self, _key, value):
        allowed = {"strength", "cardio", "mobility", "core", "balance", "conditioning"}
        cleaned = (value or "").strip().lower()
        if cleaned not in allowed:
            raise ValueError(f"Category must be one of: {', '.join(sorted(allowed))}.")
        return cleaned


class Workout(db.Model):
    __tablename__ = "workouts"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)

    workout_exercises = db.relationship(
        "WorkoutExercise",
        back_populates="workout",
        cascade="all, delete-orphan",
    )
    exercises = db.relationship(
        "Exercise",
        secondary="workout_exercises",
        back_populates="workouts",
        viewonly=True,
    )

    __table_args__ = (
        CheckConstraint("duration_minutes > 0", name="ck_workout_duration_positive"),
        CheckConstraint("LENGTH(COALESCE(notes, '')) <= 1000", name="ck_workout_notes_max_len"),
    )

    @validates("duration_minutes")
    def validate_duration(self, _key, value):
        if value is None or value <= 0:
            raise ValueError("Workout duration must be greater than 0.")
        if value > 720:
            raise ValueError("Workout duration must be 720 minutes or less.")
        return value

    @validates("date")
    def validate_date(self, _key, value):
        if value is None:
            raise ValueError("Workout date is required.")
        if value > date.today():
            raise ValueError("Workout date cannot be in the future.")
        return value


class WorkoutExercise(db.Model):
    __tablename__ = "workout_exercises"

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey("workouts.id", ondelete="CASCADE"), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey("exercises.id", ondelete="CASCADE"), nullable=False)
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)

    workout = db.relationship("Workout", back_populates="workout_exercises")
    exercise = db.relationship("Exercise", back_populates="workout_exercises")

    __table_args__ = (
        UniqueConstraint("workout_id", "exercise_id", name="uq_workout_exercise_pair"),
        CheckConstraint("reps IS NULL OR reps > 0", name="ck_reps_positive"),
        CheckConstraint("sets IS NULL OR sets > 0", name="ck_sets_positive"),
        CheckConstraint("duration_seconds IS NULL OR duration_seconds > 0", name="ck_duration_seconds_positive"),
        CheckConstraint(
            "reps IS NOT NULL OR sets IS NOT NULL OR duration_seconds IS NOT NULL",
            name="ck_workout_exercise_metric_present",
        ),
    )

    @validates("reps", "sets", "duration_seconds")
    def validate_metrics(self, key, value):
        if value is not None and value <= 0:
            raise ValueError(f"{key} must be greater than 0 when provided.")
        return value