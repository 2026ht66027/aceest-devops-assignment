# ACEest Fitness & Gym — DevOps Assignment

## Features
Starter Flask application to add, view, and delete workout records. Data is in memory and resets when the server restarts.

## Local setup
```bash
python -m venv .venv
# macOS/Linux: source .venv/bin/activate
# Windows PowerShell: .venv\\Scripts\\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```
Open http://127.0.0.1:5000.

## Run tests
```bash
python -m pytest tests/ -v
```

## Docker
```bash
docker build --pull -t aceest-fitness:local .
docker run --rm -p 5000:5000 aceest-fitness:local
docker run --rm --entrypoint python aceest-fitness:local -m pytest tests/ -v
```

## GitHub Actions
`.github/workflows/main.yml` runs on every push and pull request. It compiles/lints the Flask app, builds a Docker image, runs pytest inside the image, and checks `/health`.

## Jenkins
`Jenkinsfile` validates/tests Flask, builds a candidate image, runs containerized tests, validates each supplied version in its own stage, checks the version inventory, and promotes the candidate. Configure a Jenkins Pipeline job to use this repository and `Jenkinsfile`. Enable **GitHub hook trigger for GITScm polling** and configure the GitHub webhook to the publicly reachable Jenkins HTTPS endpoint ending in `/github-webhook/`.

## Rollback
The pipeline saves an existing `latest` image tag as `previous` before building a candidate and attempts to restore it after failure. This is a local Docker-tag rollback mechanism. Demonstrate it with a controlled failure and retain Jenkins console output before claiming rollback is verified.

## Supplied versions
Keep the ten original scripts in `source_versions/`. Per-version stages currently validate syntax; syntax checks do not prove GUI/runtime behaviour. Confirm the intended failing version before adding a dedicated defect test.
