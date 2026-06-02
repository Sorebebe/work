pipeline {
    agent any

    environment {
        //docker-сущности
        DOCKER_IMAGE = "employment_app_image"
        CONTAINER_NAME = "employment_app_container"
        HOST_PORT = "8001" 
    }

    stages {
        stage('Сборка (Build)') {
            steps {
                echo 'Собираем Docker-образ...'
                sh 'docker build -t ${DOCKER_IMAGE} .'
            }
        }

        stage('Тестирование (Test)') {
            steps {
                echo 'Запускаем автоматические тесты...'
                sh 'docker run --rm ${DOCKER_IMAGE} python manage.py test vacancies'
            }
        }

        stage('Доставка (Deploy)') {
            steps {
                echo 'Развертываем приложение на сервере...'
                sh 'docker stop ${CONTAINER_NAME} || true'
                sh 'docker rm ${CONTAINER_NAME} || true'
                sh 'docker run -d -p ${HOST_PORT}:8000 --name ${CONTAINER_NAME} ${DOCKER_IMAGE}'
            }
        }
    }
}