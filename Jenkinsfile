pipeline {
    agent any

    environment {
        // Названия для наших Docker-сущностей
        DOCKER_IMAGE = "employment_app_image"
        CONTAINER_NAME = "employment_app_container"
        // Тот самый свободный порт на сервере
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
                // Поднимаем временный контейнер только для прогона тестов из vacancies/tests.py
                sh 'docker run --rm ${DOCKER_IMAGE} python manage.py test vacancies'
            }
        }

        stage('Доставка (Deploy)') {
            // Этот этап сработает ТОЛЬКО если мы запушили в ветку vroom
            when {
                branch 'vroom'
            }
            steps {
                echo 'Развертываем приложение на сервере...'
                // Останавливаем и удаляем старый контейнер, если он был
                sh 'docker stop ${CONTAINER_NAME} || true'
                sh 'docker rm ${CONTAINER_NAME} || true'
                
                // Запускаем новый контейнер, связывая порт 8001 сервера с 8000 контейнера
                sh 'docker run -d -p ${HOST_PORT}:8000 --name ${CONTAINER_NAME} ${DOCKER_IMAGE}'
            }
        }
    }
}