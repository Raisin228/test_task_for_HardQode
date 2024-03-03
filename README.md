[![ProjectLogo](https://github.com/Raisin228/test_task_for_HardQode/blob/main/photos/Logo.png
)](https://github.com/Raisin228/test_task_for_HardQode)

### Описание

---

Backend вымышленной образовательной платформы. По задумке данная школа специализируется на подготовке разного
рода IT-специалистов, начиная от тестировщиков и заканчивая ML-инженерами👨‍💻 В данном репозитории представлена MVP (
Minimum
Viable Product) версия продукта.

***Краткий перечень реализованного функционала:***  
✓ [Создание/редактирование](#фото-2-добавление-онлайн-курса-) онлайн курса посредством админ.панели Django.  
✓ [Добавление/удаление уроков.](#фото-1-добавление-урока-)  
✓ [Создание/редактирование учебных групп.](#фото-5-группы-существующие-на-платформе-)  
✓ [Добавление новых пользователей на платформу.](#фото-4-все-пользователи-онлайн-школы-) (*P.S: доступно только админу*)  
✓ Автоматическая система распределения участников по группам.  
✓ [API для взаимодействия с внешними сервисами.](#фото-7-документация-к-проекту-swagger-)

ℹ️ **Внимание. Это версия v1.0**

Начинаем!

### Оглавление

---

- [Описание](#описание) - основная задумка проекта и краткий перечень функционала
- [Запуск проекта](#запуск-проекта-на-локальной-машине) - инструкция по развёртыванию проекта
- [Стек технологий](#стек-технологий) - инструменты используемые на проекте
- [Архитектура БД](#архитектура-бд) - схема бд и связи между таблицами
- [Фото проекта](#фото-проекта) - результат, который вы получите при правильной настройке
- [Разработчик @Raisin228](https://github.com/Raisin228)

### Запуск проекта на локальной машине

---

Выполните нижеперечисленную последовательность команд.

1. Скопируйте ссылку на репозиторий с кодом и выполните команду.

```commandline
git clone https://github.com/Raisin228/test_task_for_HardQode.git
```

2. Перейдите в директорию test_task_for_HardQode, создайте и активируйте виртуальное окружение.

```commandline
cd test_task_for_HardQode

python -m venv venv
venv/Scripts/activate
```

3. Установите все библиотеки и зависимости.

```commandline
pip install -r requirements.txt
```

4. Перейдите в директорию где лежит файл manage.py и запустите миграции бд.
```commandline
cd backend

python manage.py migrate
```

5. Загрузите все фикстуры в бд. В них я уже заполнил минимальную базу тестовыми данными.
**Выполняйте команды по очереди!**
```commandline
загрузка пользователей в таблицу auth_users
python manage.py loaddata base_application\fixtures\users.json

подгрузка списка доступных в системе курсов
python manage.py loaddata base_application\fixtures\products.json

подгрузка вшитых уроков
python manage.py loaddata base_application\fixtures\lessons.json

список групп
python manage.py loaddata base_application\fixtures\groups.json 
```

Можете приступать к добавлению пользователей на интерисующие курсы на вкладке 'Продукты' django admin.

P.S: Заранее я зарегистрировал в системе 5 пользователей. Можно потестировать систему на основе этих данных🤞  
username -> password  
* bogdan -> 123 -> is_admin = True
* kirill -> 123 -> is_admin = True
* elizaveta -> Gekon261
* grisha -> Gekon261
* sergey -> Gekon261


### Стек технологий

---

1. [Python 3.12](https://www.python.org/) - язык программирования🐍
2. [SQLite](https://www.sqlite.org/index.html) - реляционная база данных для хранения информации о пользователях.
3. [Django 5.0.2](https://www.djangoproject.com/) - web-framework для python backend разработки.
4. [Swagger](https://docs.swagger.io/spec.html) - инструмент для автоматического документирования API.
5. [Django Rest Framework](https://www.django-rest-framework.org/) - инструмент для создания REST api на базе
Django приложения.


### Архитектура БД

---

<img src="https://github.com/Raisin228/test_task_for_HardQode/blob/main/photos/Database_schema.png">


### Фото проекта

---

###### *Фото №1. Добавление урока.*  
<img src="https://github.com/Raisin228/test_task_for_HardQode/blob/main/photos/adding_lesson.png">

###### *Фото №2. Добавление онлайн курса.*  
<img src="https://github.com/Raisin228/test_task_for_HardQode/blob/main/photos/adding_product.png">

###### *Фото №3. Все курсы системы со стороны админа.*  
<img src="https://github.com/Raisin228/test_task_for_HardQode/blob/main/photos/Django_admin_product.png">

###### *Фото №4. Все пользователи онлайн школы.*  
<img src="https://github.com/Raisin228/test_task_for_HardQode/blob/main/photos/Django_admin_users.png">

###### *Фото №5. Группы существующие на платформе.*  
<img src="https://github.com/Raisin228/test_task_for_HardQode/blob/main/photos/show_all_groups.png">

###### *Фото №6. Документация к проекту [Redoc].*  
<img src="https://github.com/Raisin228/test_task_for_HardQode/blob/main/photos/redoc.png">

###### *Фото №7. Документация к проекту [Swagger].*  
<img src="https://github.com/Raisin228/test_task_for_HardQode/blob/main/photos/swagger.png">

