from marshmallow import ValidationError, validates_schema
from marshmallow import fields as ma_fields
from flask_marshmallow import Marshmallow

from models import Exercise, Workout, WorkoutExercise


ma = Marshmallow()


class ExerciseSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Exercise
        load_instance = True

    id = ma.auto_field(dump_only=True)
    name = ma.auto_field(required=True)
    category = ma.auto_field(required=True)
    equipment_needed = ma.auto_field(required=True)

    @validates_schema
    def validate_exercise(self, data, **_kwargs):
        if "name" in data and len(data["name"].strip()) < 2:
            raise ValidationError("Name must be at least 2 characters.", field_name="name")
        if "category" in data:
            allowed = {"strength", "cardio", "mobility", "core", "balance", "conditioning"}
            category = data["category"].strip().lower()
            if category not in allowed:
                raise ValidationError(
                    f"Category must be one of: {', '.join(sorted(allowed))}.",
                    field_name="category",
                )


class WorkoutExerciseFlatSchema(ma.SQLAlchemySchema):
    class Meta:
        model = WorkoutExercise
        load_instance = True

    id = ma.auto_field(dump_only=True)
    workout_id = ma.auto_field(required=True)
    exercise_id = ma.auto_field(required=True)
    reps = ma.auto_field(allow_none=True)
    sets = ma.auto_field(allow_none=True)
    duration_seconds = ma.auto_field(allow_none=True)

    @validates_schema
    def validate_metrics(self, data, **_kwargs):
        if not any(data.get(field) is not None for field in ["reps", "sets", "duration_seconds"]):
            raise ValidationError(
                "At least one of reps, sets, or duration_seconds is required.",
                field_name="reps",
            )


class WorkoutExerciseDetailSchema(ma.SQLAlchemySchema):
    class Meta:
        model = WorkoutExercise

    id = ma.auto_field()
    reps = ma.auto_field()
    sets = ma.auto_field()
    duration_seconds = ma.auto_field()
    exercise = ma.Nested(ExerciseSchema)


class WorkoutSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Workout
        load_instance = True

    id = ma.auto_field(dump_only=True)
    date = ma.auto_field(required=True)
    duration_minutes = ma.auto_field(required=True)
    notes = ma.auto_field(allow_none=True)

    workout_exercises = ma.Nested(WorkoutExerciseDetailSchema, many=True, dump_only=True)

    @validates_schema
    def validate_workout(self, data, **_kwargs):
        if "duration_minutes" in data and data["duration_minutes"] <= 0:
            raise ValidationError("duration_minutes must be greater than 0.", field_name="duration_minutes")
        if "notes" in data and data["notes"] is not None and len(data["notes"]) > 1000:
            raise ValidationError("notes must be 1000 characters or fewer.", field_name="notes")


class WorkoutWithSummarySchema(ma.SQLAlchemySchema):
    class Meta:
        model = Workout

    id = ma.auto_field()
    date = ma.auto_field()
    duration_minutes = ma.auto_field()
    notes = ma.auto_field()


class ExerciseWithWorkoutsSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Exercise

    id = ma.auto_field()
    name = ma.auto_field()
    category = ma.auto_field()
    equipment_needed = ma.auto_field()
    workouts = ma.Nested(WorkoutWithSummarySchema, many=True)


exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)

workout_exercise_schema = WorkoutExerciseFlatSchema()
workout_exercises_schema = WorkoutExerciseFlatSchema(many=True)

exercise_with_workouts_schema = ExerciseWithWorkoutsSchema()