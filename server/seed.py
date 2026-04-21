#!/usr/bin/env python3

from datetime import date

from app import app
from models import Exercise, Workout, WorkoutExercise, db

with app.app_context():
    print("Clearing existing data...")
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()

    print("Creating exercises...")
    push_up = Exercise(name="Push Up", category="strength", equipment_needed=False)
    jump_rope = Exercise(name="Jump Rope", category="cardio", equipment_needed=True)
    plank = Exercise(name="Plank", category="core", equipment_needed=False)

    print("Creating workouts...")
    monday = Workout(date=date(2026, 4, 20), duration_minutes=45, notes="Upper body focus")
    tuesday = Workout(date=date(2026, 4, 21), duration_minutes=30, notes="Core and cardio")

    db.session.add_all([push_up, jump_rope, plank, monday, tuesday])
    db.session.commit()

    print("Creating workout exercise links...")
    links = [
        WorkoutExercise(workout_id=monday.id, exercise_id=push_up.id, reps=12, sets=4),
        WorkoutExercise(workout_id=tuesday.id, exercise_id=plank.id, duration_seconds=90, sets=3),
        WorkoutExercise(workout_id=tuesday.id, exercise_id=jump_rope.id, duration_seconds=300),
    ]

    db.session.add_all(links)
    db.session.commit()

    print("Seeding complete.")