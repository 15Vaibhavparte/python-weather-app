pipeline {
    agent any

    environment {
        // Variables for your pipeline
        NEXUS_URL = "http://52.66.155.250:8081/repository/weather-app/"
        SONAR_PROJECT_KEY = "weather-app"
        DOCKERHUB_USERNAME = 'parte15'
        IMAGE_NAME = "weather-api"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install & Test') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -e .[test]
                    pytest tests/ --junitxml=test-results.xml
                '''
            }
        }

        stage('SonarQube Analysis') {
            steps {
                // Requires SonarQube Scanner configured in Jenkins
                withSonarQubeEnv('SonarQube-Server') {
                    sh """
                        sonar-scanner \
                        -Dsonar.projectKey=${SONAR_PROJECT_KEY} \
                        -Dsonar.sources=app \
                        -Dsonar.tests=tests \
                        -Dsonar.python.version=3.10
                    """
                }
            }
        }

        stage('Quality Gate') {
            steps {
                // Pauses pipeline until SonarQube confirms code meets standards
                timeout(time: 1, unit: 'HOURS') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        stage('Package & Push to Nexus') {
            steps {
                sh '''
                    . venv/bin/activate
                    pip install build twine
                    
                    # Build Wheel and Source dist
                    python -m build
                    
                    # Upload to Nexus (Using credentials stored in Jenkins)
                    # Note: In a real environment, use Jenkins credentials binding
                    twine upload --repository-url ${NEXUS_URL} -u admin -p your_nexus_password dist/*
                '''
            }
        }

        stage('Build & Push Docker Image') {
            steps {
                script {
                    // Build the multi-stage image
                    def app = docker.build("${IMAGE_NAME}:${env.BUILD_ID}")
                    
                    // Push to Docker Hub (Requires Docker Hub credentials in Jenkins)
                    docker.withRegistry('https://index.docker.io/v1/', 'dockerhub-credentials') {
                        app.push()
                        app.push('latest')
                    }
                }
            }
        }
    }
}