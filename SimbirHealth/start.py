import os
import django

# Установить настройки Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from Account.models import User
from django.contrib.auth.hashers import make_password
from Document.models import FirstConfig

if not (FirstConfig.objects.exists()):
    User_new = User.objects.create(
        username="admin",
        password=make_password("admin"),
        first_name="Иван",
        last_name="Иванов",
        is_superuser=1,
        is_staff=1
    )
    User_new = User.objects.create(
        username="manager",
        password="manager",
        first_name="Виктор",
        last_name="Викторович",
        is_manager=1
    )
    User_new = User.objects.create(
        username="doctor",
        password="doctor",
        first_name="Максим",
        last_name="Максимович",
        is_doctor=1
    )
    User_new = User.objects.create(
        username="user",
        password="user",
        first_name="Александр",
        last_name="Александрович",
    )
    f_config = FirstConfig.objects.create(
        is_made=True
    )
else:
    print(f'Первоначальная настройка не требуется')
