# WeatherApp
Задание было выполнено на Ubuntu 17.10

# Getting Started
--Для начала работы активируйте окружение:

$ source env_name/bin/activate

# Requirements backend
--Для работы бекенда требуется предустановленный RabbitMQ и Celery.
https://www.rabbitmq.com/download.html


--Зависимости:
$ pip install -r requirements.txt установит зависимости drf & celery & flower.

--В файле settings.py установите secret key а так же api key, выданный вам openweathermap.org

--Сконфигурируйте CORS в settings.py. Сейчас настроен на localhost:4200 - dev server angular 5. Необходимость из-за возможности работы фронтенда и бекенда в разных контекстах.

--Примените миграции:

$ python manage.py makemigrations

$ python manage.py migrate

--Запуск воркеров производить из папки проекта командой :

$ celery worker --app=main_app.tasks --loglevel=info

--Для отслеживания и ведения статистики нагрузки и выполения tasks используйте flower

$ flower --port 5555

,откройте localhost:5555

# Requirements frontend
--Особых зависимостей нет. Одна из них MaterializeCSS.

Необходим предустановленный NodeJS, AngularCLI, npm.

Версия на dev pc:

Angular CLI: 1.7.4
Node: 6.11.4
OS: linux x64
Angular: 5.2.11
... animations, common, compiler, compiler-cli, core, forms
... http, language-service, platform-browser
... platform-browser-dynamic, router

@angular/cli: 1.7.4
@angular-devkit/build-optimizer: 0.3.2
@angular-devkit/core: 0.3.2
@angular-devkit/schematics: 0.3.2
@ngtools/json-schema: 1.2.0
@ngtools/webpack: 1.10.2
@schematics/angular: 0.3.2
@schematics/package-update: 0.3.2
typescript: 2.5.3
webpack: 3.11.0


