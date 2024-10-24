## Варианты запуска приложения:

1) **docker-compose up -d**  
Проект запущен, дополнительных настроек не требуется. PostgreSQL в данном варианте устанавливается как отдельный сервис внутри контейнера с образом `postgres:13`, автоматически создавая пользователя, пароль и базу данных, указанные в переменных окружения.

2) **Локальный PostgreSQL**  
  - Раскомментировать код подключения к локальному PostgreSQL в файле `settings.py` (`SimbirHealth/core/settings.py`).
  - Указать пользовательские настройки для подключения к БД (`NAME`, `USER`, `PASSWORD`, `HOST`, `PORT`).
  - Удалить образ `postgres:13` из файла `docker-compose.yml`.
  - Запустить `docker-compose up -d`.

![image](https://github.com/user-attachments/assets/0b19991c-3244-4235-b4c9-06e780b744de)

## Swagger-документация

- **Account**: [Swagger Account](http://127.0.0.1:8000/account/ui-swagger/)
- **Hospital**: [Swagger Hospital](http://127.0.0.1:8000/hospital/ui-swagger/)
- **Timetable**: [Swagger Timetable](http://127.0.0.1:8000/timetable/ui-swagger/)
- **Document**: [Swagger Document](http://127.0.0.1:8000/document/ui-swagger/)  
(пути в Swagger показываются без `/api`)

## Пользователи по умолчанию:

1) login: **admin**, password: **admin**, id: 1  
2) login: **manager**, password: **manager**, id: 2  
3) login: **doctor**, password: **doctor**, id: 3  
4) login: **user**, password: **user**, id: 4  

## Инструкция по выполнению API-запросов через Swagger с авторизацией (пример для пользователя admin):

1) Переходим по адресу [http://127.0.0.1:8000/account/ui-swagger/](http://127.0.0.1:8000/account/ui-swagger/), ищем API `/Authentication/SignIn/`:
![image](https://github.com/user-attachments/assets/6722e4f2-10eb-4fed-86be-a73520fa6e77)

2) Нажимаем на данный API, затем на кнопку **Try it out** (все запросы в Swagger выполняются через эту кнопку):
![image](https://github.com/user-attachments/assets/b0a5edf4-3cfd-45a1-b2d0-42531290f003)

3) Заполняем поля **username** и **password**, нажимаем кнопку **Execute**:
![image](https://github.com/user-attachments/assets/418ec446-89d6-4e3e-bac1-1ebb8c8ba4b8)

4) Пролистываем вниз и копируем **access токен**:
![image](https://github.com/user-attachments/assets/b6a19f4c-de46-4ebc-905e-47c2da01fce9)

5) Переходим в Swagger нужного сервиса (например, **Hospital**), нажимаем кнопку **Authorize**:
![image](https://github.com/user-attachments/assets/a4a7b30c-f565-4559-95c9-76d4fa5442b8)

6) В появившейся форме вводим `Bearer <access токен>`, нажимаем **Authorize**:
![image](https://github.com/user-attachments/assets/43e6cbd0-ec72-491b-bba8-26ac2c8eceb5)

7) Нажимаем кнопку **Close**. Авторизация выполнена, теперь можно выполнять запросы от пользователя **admin** (с остальными пользователями аналогичные действия).

> **ВАЖНО**: при обновлении страницы Swagger авторизация не сохраняется, необходимо выполнить пункты 1–6 заново.

## Пример выполнения запросов:

1) **Изменение администратора аккаунта по ID** (`/Accounts/{id}/`):
![image](https://github.com/user-attachments/assets/65ac5d98-7b64-4ce8-9220-b383d52ccc5f)
![image](https://github.com/user-attachments/assets/8b520dff-34ac-4207-a364-73bd5ded3439)

2) **Создание записи о новой больнице** (`/Hospitals/`):
![image](https://github.com/user-attachments/assets/25809094-656e-4f51-8c82-b306cca85cc8)

