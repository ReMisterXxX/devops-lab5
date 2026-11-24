pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    environment {
        APP_NAME = 'lab5-app'
        NETWORK = 'lab5_net'
        NOTIFY_TO = 'zespol@lab5.local'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                script {
                    env.BRANCH = env.BRANCH_NAME ?: 'main'
                    env.SHORT_SHA = sh(script: 'git rev-parse --short HEAD', returnStdout: true).trim()
                    env.IMAGE = "${APP_NAME}:${env.BUILD_NUMBER}-${env.SHORT_SHA}"
                    env.APP_VERSION = readFile('VERSION').trim()
                }
                echo "Galaz: ${env.BRANCH}, commit: ${env.SHORT_SHA}, wersja: ${env.APP_VERSION}"
            }
        }

        stage('Lint') {
            steps {
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
                    pip install -q -r requirements-dev.txt
                    flake8 app tests
                '''
            }
        }

        stage('Testy jednostkowe') {
            steps {
                sh '''
                    . .venv/bin/activate
                    pytest tests -v --junitxml=test-results.xml
                '''
            }
            post {
                always {
                    junit 'test-results.xml'
                }
            }
        }

        stage('Build') {
            steps {
                sh 'docker build -t $IMAGE .'
            }
        }

        stage('Deploy: test') {
            when {
                expression { env.BRANCH == 'main' || env.BRANCH == 'develop' || env.BRANCH.startsWith('release/') }
            }
            steps {
                sh '''
                    docker rm -f lab5-test || true
                    docker run -d --name lab5-test --network $NETWORK -p 8081:5000 \
                        -e APP_ENV=test -e APP_VERSION=$APP_VERSION $IMAGE
                    for i in 1 2 3 4 5 6 7 8 9 10; do
                        curl -sf http://lab5-test:5000/health && break
                        sleep 2
                    done
                    curl -sf http://lab5-test:5000/
                    curl -sf "http://lab5-test:5000/api/add?a=2&b=3"
                '''
            }
        }

        stage('Akceptacja wdrozenia na produkcje') {
            when {
                expression { env.BRANCH == 'main' }
            }
            steps {
                timeout(time: 30, unit: 'MINUTES') {
                    input message: "Wdrozyc wersje ${env.APP_VERSION} na produkcje?", ok: 'Wdroz'
                }
            }
        }

        stage('Deploy: produkcja') {
            when {
                expression { env.BRANCH == 'main' }
            }
            steps {
                sh '''
                    docker rm -f lab5-prod || true
                    docker run -d --name lab5-prod --network $NETWORK -p 8082:5000 --restart unless-stopped \
                        -e APP_ENV=production -e APP_VERSION=$APP_VERSION $IMAGE
                    for i in 1 2 3 4 5 6 7 8 9 10; do
                        curl -sf http://lab5-prod:5000/health && break
                        sleep 2
                    done
                    curl -sf http://lab5-prod:5000/
                '''
            }
        }
    }

    post {
        always {
            mail to: env.NOTIFY_TO,
                 subject: "[Jenkins] ${env.JOB_NAME} #${env.BUILD_NUMBER}: ${currentBuild.currentResult}",
                 body: """Pipeline: ${env.JOB_NAME}
Build: #${env.BUILD_NUMBER}
Galaz: ${env.BRANCH}
Commit: ${env.SHORT_SHA}
Status: ${currentBuild.currentResult}
Szczegoly: ${env.BUILD_URL}
"""
        }
    }
}
