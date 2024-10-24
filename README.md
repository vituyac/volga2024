Варианты запуска приложения:
  1) docker-compose up -d. Проект запушен, дополнительных настроек не требуется. PostgreSQL в данном варианте устанавливается как отдельный сервис внутри контейнера с образом postgres:13, автоматически создавая пользователя, пароль и базу данных, указанные в переменных окружения.
  2) Раскомментировать код подключения к локальному PostgreSQL в файле settings.py (SimbirHealth/core/settings.py), указать пользовательские настройки для подключения к БД (NAME, USER, PASSWORD, HOST, PORT), удалить образ postgres:13 из файла docker-compose.yml, запустить docker-compose up -d.
![image](https://github.com/user-attachments/assets/0b19991c-3244-4235-b4c9-06e780b744de)

Swagger Account: http://127.0.0.1:8000/account/ui-swagger/
Swagger Hospital: http://127.0.0.1:8000/hospital/ui-swagger/
Swagger Timetable: http://127.0.0.1:8000/timetable/ui-swagger/
Swagger Document: http://127.0.0.1:8000/document/ui-swagger/
(пути в сваггере показываются без /api)

Инструкция по выполнению api запросов через сваггер с авторизацией (пример для пользователя admin):
1) Переходим http://127.0.0.1:8000/account/ui-swagger/, ищем api /Authentication/SignIn/:
![image](https://github.com/user-attachments/assets/6722e4f2-10eb-4fed-86be-a73520fa6e77)
2) Нажимаем на данный api, потом на кнопку Try it out (все запросы в сваггере делаются через эту кнопку):
![image](https://github.com/user-attachments/assets/b0a5edf4-3cfd-45a1-b2d0-42531290f003)
3) Заполняем поля username и password, нажимаем на кнопку Execute:
![image](https://github.com/user-attachments/assets/418ec446-89d6-4e3e-bac1-1ebb8c8ba4b8)
4) Пролистываем вниз и копируем access токен:
![image](https://github.com/user-attachments/assets/b6a19f4c-de46-4ebc-905e-47c2da01fce9)
5) Переходим в сваггер нужного сервиса (например, Hospital), нажимаем кнопку Authorize:
![image](https://github.com/user-attachments/assets/a4a7b30c-f565-4559-95c9-76d4fa5442b8)
6) В появившейся форме вводим Bearer <access токен>, нажимаем Authorize:
![image](https://github.com/user-attachments/assets/43e6cbd0-ec72-491b-bba8-26ac2c8eceb5)
7) Нажимаем кнопку close. Авторизация выполнена, теперь можно выполнять запросы от пользователя admin (с остальными пользователями аналогичные действия)
**ВАЖНО: ПРИ ОБНОВЛЕНИИ СТРАНЦЫ СВАГГЕРА АВТОРИЗАЦИЯ НЕ СОХРАНЯЕТСЯ, НУЖНО ВЫПОЛНЯТЬ ПУНКТЫ 1-6 ЗАНОВО**

Пример выполнения некоторых запросов (если есть замечания по запросу, они обычно есть в описании запроса в сваггере):
Изменение администратором аккаунта по id (/Accounts/{id}/):
![11](https://github.com/user-attachments/assets/9e5ca0a0-500d-4b5e-8c40-e645ebee5f22)
![12](https://github.com/user-attachments/assets/8cffb7a9-1150-40d8-86e4-c04ae309ec5d)

Создание записи о новой больнице (/Hospitals/):
![14](https://github.com/user-attachments/assets/9025ab2a-b525-4a3d-b71a-5541f5a34c58)














