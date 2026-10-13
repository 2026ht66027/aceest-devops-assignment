from flask import Flask, flash, redirect, render_template, request, url_for


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(SECRET_KEY="development-key-change-me", TESTING=False)
    if test_config:
        app.config.update(test_config)
    workouts, next_id = [], [1]

    @app.get("/")
    def index():
        return render_template("index.html", workouts=workouts)

    @app.post("/workouts")
    def add_workout():
        name = request.form.get("name", "").strip()
        raw_duration = request.form.get("duration", "").strip()
        try:
            duration = int(raw_duration)
        except (TypeError, ValueError):
            duration = 0
        if not name:
            flash("Workout name is required.", "error")
        elif not 1 <= duration <= 1440:
            flash("Duration must be between 1 and 1440 minutes.", "error")
        else:
            workouts.append({"id": next_id[0], "name": name, "duration": duration,
                             "notes": request.form.get("notes", "").strip()})
            next_id[0] += 1
            flash("Workout added successfully.", "success")
        return redirect(url_for("index"))

    @app.post("/workouts/<int:workout_id>/delete")
    def delete_workout(workout_id):
        for index, workout in enumerate(workouts):
            if workout["id"] == workout_id:
                del workouts[index]
                flash("Workout deleted.", "success")
                break
        else:
            flash("Workout not found.", "error")
        return redirect(url_for("index"))

    @app.get("/health")
    def health():
        return {"status": "ok"}, 200

    return app

app = create_app()
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
