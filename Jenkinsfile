pipeline {
    agent any
    
    environment {
        PYTHON_VERSION = '3.9'
        VENV_PATH = 'venv'
    }
    
    stages {
        stage('Setup') {
            steps {
                sh '''
                    python3 -m venv ${VENV_PATH}
                    . ${VENV_PATH}/bin/activate
                    pip install -r requirements.txt
                    pip install pylint flake8 mypy
                '''
            }
        }
        
        stage('Static Analysis') {
            steps {
                sh '''
                    . ${VENV_PATH}/bin/activate
                    
                    # Run pylint
                    echo "Running pylint..."
                    pylint fuzzy_matcher.py || true
                    
                    # Run flake8
                    echo "Running flake8..."
                    flake8 fuzzy_matcher.py || true
                    
                    # Run mypy for type checking
                    echo "Running mypy..."
                    mypy fuzzy_matcher.py || true
                '''
            }
        }
        
        stage('Test') {
            steps {
                sh '''
                    . ${VENV_PATH}/bin/activate
                    python fuzzy_matcher.py
                '''
            }
        }
    }
    
    post {
        always {
            cleanWs()
        }
    }
}
