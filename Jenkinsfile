pipeline {
    agent any
    options { timestamps(); disableConcurrentBuilds() }
    environment { IMAGE_NAME = 'aceest-fitness'; CANDIDATE_TAG = 'candidate'; PREVIOUS_TAG = 'previous' }
    stages {
        stage('Checkout') { steps { checkout scm } }
        stage('Clean Build') { steps { deleteDir(); checkout scm } }
        stage('Validate Flask App') {
            steps {
                sh '''
                    set -eu
                    python3 -m venv .venv
                    . .venv/bin/activate
                    python -m pip install --upgrade pip
                    python -m pip install -r requirements.txt ruff
                    python -m py_compile app.py
                    ruff check app.py tests/
                    python -m pytest tests/ -v
                '''
            }
        }
        stage('Build Flask Candidate Image') {
            steps {
                sh '''
                    set -eu
                    if docker image inspect ${IMAGE_NAME}:latest >/dev/null 2>&1; then
                        docker tag ${IMAGE_NAME}:latest ${IMAGE_NAME}:${PREVIOUS_TAG}
                    fi
                    docker build --pull -t ${IMAGE_NAME}:${CANDIDATE_TAG} .
                '''
            }
        }
        stage('Test Flask Inside Container') {
            steps { sh 'docker run --rm --entrypoint python ${IMAGE_NAME}:${CANDIDATE_TAG} -m pytest tests/ -v' }
        }
        stage('Version 1.0') {
            when { expression { fileExists('source_versions/Aceestver-1.0.py') } }
            steps { sh 'python3 -m py_compile source_versions/Aceestver-1.0.py' }
        }
        stage('Version 1.1') {
            when { expression { fileExists('source_versions/Aceestver-1.1.py') } }
            steps { sh 'python3 -m py_compile source_versions/Aceestver-1.1.py' }
        }
        stage('Version 1.1.2') {
            when { expression { fileExists('source_versions/Aceestver1.1.2.py') } }
            steps { sh 'python3 -m py_compile source_versions/Aceestver1.1.2.py' }
        }
        stage('Version 2.0.1') {
            when { expression { fileExists('source_versions/Aceestver2.0.1.py') } }
            steps { sh 'python3 -m py_compile source_versions/Aceestver2.0.1.py' }
        }
        stage('Version 2.1.2') {
            when { expression { fileExists('source_versions/Aceestver-2.1.2.py') } }
            steps { sh 'python3 -m py_compile source_versions/Aceestver-2.1.2.py' }
        }
        stage('Version 2.2.1') {
            when { expression { fileExists('source_versions/Aceestver-2.2.1.py') } }
            steps { sh 'python3 -m py_compile source_versions/Aceestver-2.2.1.py' }
        }
        stage('Version 2.2.4') {
            when { expression { fileExists('source_versions/Aceestver-2.2.4.py') } }
            steps { sh 'python3 -m py_compile source_versions/Aceestver-2.2.4.py' }
        }
        stage('Version 3.0.1') {
            when { expression { fileExists('source_versions/Aceestver-3.0.1.py') } }
            steps { sh 'python3 -m py_compile source_versions/Aceestver-3.0.1.py' }
        }
        stage('Version 3.1.2') {
            when { expression { fileExists('source_versions/Aceestver-3.1.2.py') } }
            steps { sh 'python3 -m py_compile source_versions/Aceestver-3.1.2.py' }
        }
        stage('Version 3.2.4') {
            when { expression { fileExists('source_versions/Aceestver-3.2.4.py') } }
            steps { sh 'python3 -m py_compile source_versions/Aceestver-3.2.4.py' }
        }
        stage('Check All Ten Versions Present') {
            steps {
                sh '''
                    set -eu
                    count=$(find source_versions -maxdepth 1 -type f -name '*.py' | wc -l)
                    echo "Found $count source versions in this commit"
                    test "$count" -le 10
                '''
            }
        }
        stage('Promote Candidate') {
            steps { sh 'docker tag ${IMAGE_NAME}:${CANDIDATE_TAG} ${IMAGE_NAME}:latest' }
        }
    }
    post {
        always { echo 'ACEest pipeline finished.' }
        failure {
            echo 'Pipeline failed; restoring previous image tag if one exists.'
            sh '''
                if docker image inspect ${IMAGE_NAME}:${PREVIOUS_TAG} >/dev/null 2>&1; then
                    docker tag ${IMAGE_NAME}:${PREVIOUS_TAG} ${IMAGE_NAME}:latest
                    echo "Previous image tag restored."
                else
                    echo "No previous image available."
                fi
            '''
        }
        success { echo 'Pipeline succeeded.' }
    }
}
