pipeline {
    agent any
    
    tools {
        jdk 'jdk21'
    }

    environment {
        NEXUS_URL = "http://52.66.155.250:8081/repository/weather-app/"
        SONAR_PROJECT_KEY = "weather-app"
        DOCKERHUB_USERNAME = 'parte15'
        IMAGE_NAME = "${DOCKERHUB_USERNAME}/weather-api"
    }

    stages {
        stage('Initial Setup') {
            steps {
                checkout scm
            }
        }

        stage('Parallel Operations') {
            parallel {
                // Branch 1: Quality & Security Analysis
                stage('Static Analysis') {
                    environment {
                        SCANNER_HOME = tool('sonar-scanner')
                    }
                    steps {
                        withSonarQubeEnv('sonar-server') {
                            sh """
                                ${SCANNER_HOME}/bin/sonar-scanner \
                                -Dsonar.projectKey=${SONAR_PROJECT_KEY} \
                                -Dsonar.sources=app \
                                -Dsonar.tests=tests \
                                -Dsonar.python.version=3.10
                            """
                        }
                        // Wait for Quality Gate inside this branch
                        timeout(time: 1, unit: 'HOURS') {
                            waitForQualityGate abortPipeline: true
                        }
                    }
                }

                // Branch 2: Testing, Artifact Management, and Dockerization
                stage('Build and Release') {
                    steps {
                        // 1. Install & Test
                        sh '''
                            python3 -m venv venv
                            . venv/bin/activate
                            pip install -e .[test]
                            pytest tests/ --junitxml=test-results.xml
                        '''
                        
                        // 2. Package & Push to Nexus
                        sh '''
                            . venv/bin/activate
                            pip install build twine
                            python -m build
                            twine upload --repository-url ${NEXUS_URL} -u admin -p admin@123 dist/*
                        '''

                        // 3. Build & Push Docker Image
                        script {
                            def app = docker.build("${IMAGE_NAME}:${env.BUILD_ID}")
                            docker.withRegistry('https://index.docker.io/v1/', 'docker-cred') {
                                app.push()
                                app.push('latest')
                            }
                        }
                    }
                }
            }
        }
    }
}
