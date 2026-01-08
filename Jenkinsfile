pipeline {
  agent any
  environment {
    DOCKERHUB_REPO = "23127174/dath3-flask-cicd"
    IMAGE_TAG = "${BUILD_NUMBER}"
    CONTAINER_NAME = "dath3_flask_cicd_app"
    APP_PORT = "5000"
    HOST_PORT = "8081"
  }
  stages {
    stage('Checkout') { steps { checkout scm } }

    stage('Test') {
      steps {
        sh '''
        python3 -m venv .venv
        . .venv/bin/activate
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pytest -q
        '''
      }
    }

    stage('Build Docker image') {
      steps {
        sh 'docker build -t $DOCKERHUB_REPO:$IMAGE_TAG -t $DOCKERHUB_REPO:latest .'
      }
    }

    stage('Push DockerHub') {
      steps {
        withCredentials([usernamePassword(credentialsId: "dockerhub-creds", usernameVariable: "DH_USER", passwordVariable: "DH_PASS")]) {
          sh 'echo $DH_PASS | docker login -u $DH_USER --password-stdin'
          sh 'docker push $DOCKERHUB_REPO:$IMAGE_TAG'
          sh 'docker push $DOCKERHUB_REPO:latest'
        }
      }
    }

    stage('Deploy') {
      steps {
        sh """
            docker rm -f ${CONTAINER_NAME} || true
            docker run -d --name ${CONTAINER_NAME} -p ${HOST_PORT}:${APP_PORT} ${DOCKERHUB_REPO}:latest
            docker ps --filter "name=${CONTAINER_NAME}"
            
            echo "Waiting for app to be ready..."
            for i in \$(seq 1 20); do
                if curl -fsS http://localhost:8081/health > /dev/null; then
                echo "App is ready!"
                break
                fi
                sleep 1
            done

            # Check one last time (and fail with logs if still not ready)
            curl -fsS http://localhost:8081/health
            echo
            docker ps --filter name=dath3_flask_cicd_app
        """
      }
    }
  }
}
