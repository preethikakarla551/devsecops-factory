pipeline {
    agent any

    environment {
        IMAGE_NAME = 'devsecops-factory'
        IMAGE_TAG = "${BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps { checkout scm }
        }
        stage('Install and test') {
            steps {
                bat 'py -3 -m venv .venv'
                bat '.venv\\Scripts\\python -m pip install --upgrade pip'
                bat '.venv\\Scripts\\python -m pip install -r requirements-dev.txt'
                bat '.venv\\Scripts\\python -m pytest -q'
            }
        }
        stage('Build image') {
            steps { bat 'docker build -t %IMAGE_NAME%:%IMAGE_TAG% .' }
        }
        stage('Trivy image scan') {
            steps {
                bat 'trivy image --exit-code 1 --severity HIGH,CRITICAL %IMAGE_NAME%:%IMAGE_TAG%'
            }
        }
    }
    post {
        always { echo 'Pipeline finished. Review the stage results and Trivy report.' }
    }
}
