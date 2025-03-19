pipeline {
    agent any
    
    environment {
        DOCKER_HUB_CREDS = credentials('docker-hub-credentials')
        DOCKER_IMAGE = "gimmick3205/fuzzy_match"
        DOCKER_TAG = "${BUILD_NUMBER}"
    }
    
    stages {
        stage('Clone Repository') {
            steps {
                git url: 'https://github.com/Femarleycode/fuzzy-match.git', branch: 'main'
            }
        }
        
        stage('Build and Push Docker Image') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', 'docker-hub-credentials') {
                        def customImage = docker.build("${DOCKER_IMAGE}:${DOCKER_TAG}")
                        customImage.push()
                        customImage.push('latest')
                    }
                }
            }
        }
    }
    
    post {
        success {
            echo "Successfully built and pushed ${DOCKER_IMAGE}:${DOCKER_TAG} to Docker Hub"
        }
        failure {
            echo "Failed to build/push Docker image"
        }
    }
}
