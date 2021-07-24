# Foodgram
Проект сервиса публикации кулинарных рецептов.
Демо проекта [Продуктовый помощник](http://emelyaart.ru)

## Ключевые возможности сервиса:
1. Регистрация пользователей.
2. Создание, Изменение, Удаление рецептов.
3. Добавление рецептов в избранное и простмотр всех избранных рецептов.
4. Фильтрация рецептов по тегам.
6. Подписка на авторов и просмотр рецептов определенного автора.
7. Добавление рецептов и формирование списка покупок для их приготовления.

## Установка сервиса на сервер.

### ВАЖНО! Для работы сервиса необходим заранее установленный [Docker](https://www.docker.com)
Если Docker установлен, можно начать.

1. Клонируйте репозиторий к себе на сервер командой:
```bash
git clone https://github.com/emelyaart/foodgram-project-react.git
```
2. Перейдите в каталог командой:
```bash
cd foodgram-project-react/backend/
```
3. Выполнить команду для создания файла env:
```bash
touch .env
```
4. Добавьте настройки выполнив команды:
```bash
echo "DJANGO_SECRET_KEY=your_secret_key" >> .env && # Здесь нужно ввести секретный код
echo "DB_ENGINE=django.db.backends.postgresql_psycopg2" >> .env &&
echo "DB_NAME=postgres" >> .env &&
echo "POSTGRES_USER=postgres" >> .env &&
echo "POSTGRES_PASSWORD=your_password" >> .env && #Здесь необходимо ввести свой пароль
echo "DB_HOST=db" >> .env &&
echo "DB_PORT=5432" >> .env
```
> Для генерации случайного секретного кода можно воспользоваться сервисом [Djecrety.ir](https://djecrety.ir/)

5. Перейдите в каталог infra командой:
```bash
cd ../infra/
```
6. Запустите создание контейнеров командой:
```bash
docker compose up -d
```
7. Через некоторое время вы увидите примерно такой вывод:
 ```bash
 [+] Running 5/5
 ⠿ Network infra_default       Created                                     0.6s
 ⠿ Container infra_frontend_1  Started                                     3.4s
 ⠿ Container infra_nginx_1     Started                                     3.8s
 ⠿ Container infra_db_1        Started                                     3.6s
 ⠿ Container infra_backend_1   Started                                     6.7s
```
На этом сборка завершена, сервис запущен и доступен по адресу your_domain.com/, либо localhost/ если это локальный сервер.
