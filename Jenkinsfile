pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "gimmick3205/fuzzy-match:latest"
    }

    stages {
        stage('Clone Repository') {
            steps {
                git 'https://github.com/Gimmick3205/fuzzy-match'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t fuzzy-match .'
            }
        }

        stage('Login to Docker Hub') {
            steps {
                withDockerRegistry([credentialsId: 'docker-hub-credentials', url: '']) {
                    sh 'docker login'
                }
            }
        }

        stage('Tag and Push to Docker Hub') {
            steps {
                withDockerRegistry([credentialsId: 'docker-hub-credentials', url: '']) {
                    sh '''
                    docker tag fuzzy-match $DOCKER_IMAGE
                    docker push $DOCKER_IMAGE
                    '''
                }
            }
        }
    }
}
