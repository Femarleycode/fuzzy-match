pipeline {
    agent any
    
    environment {
        // Set your Docker Hub credentials ID configured in Jenkins
        DOCKER_HUB_CREDS = credentials('docker-hub-credentials')
        // Set your Docker image name based on your Docker Hub account
        DOCKER_IMAGE = "gimmick3205/fuzzy_match"
        DOCKER_TAG = "${BUILD_NUMBER}"
    }
    
    stages {
        stage('Prepare Environment') {
            steps {
                // Fix Docker socket permissions - use with caution in production
                sh '''
                    if [ -S /var/run/docker.sock ]; then
                        chmod 666 /var/run/docker.sock
                    else
                        echo "Docker socket not found at expected location"
                        exit 1
                    fi
                '''
            }
        }
        
        stage('Clone Repository') {
            steps {
                git url: 'https://github.com/Femarleycode/fuzzy-match.git', branch: 'main'
            }
        }
        
        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} ."
                sh "docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKER_IMAGE}:latest"
            }
        }
        
        stage('Login to Docker Hub') {
            steps {
                sh "echo ${DOCKER_HUB_CREDS_PSW} | docker login -u ${DOCKER_HUB_CREDS_USR} --password-stdin"
            }
        }
        
        stage('Push to Docker Hub') {
            steps {
                sh "docker push ${DOCKER_IMAGE}:${DOCKER_TAG}"
                sh "docker push ${DOCKER_IMAGE}:latest"
            }
        }
        
        stage('Cleanup') {
            steps {
                // Clean up - logout from Docker Hub and remove local images
                sh 'docker logout'
                sh "docker rmi ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKER_IMAGE}:latest || true"
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
