[![Build Status](https://travis-ci.org/flame0/atom-hw.svg?branch=master)](https://travis-ci.org/flame0/atom-hw)
[![Coverage Status](https://coveralls.io/repos/github/flame0/atom-hw/badge.svg?branch=master)](https://coveralls.io/github/flame0/atom-hw?branch=master)
# Домашнее задание к лекции №3 (L3HW)

Реализовать класс **Task** (задача), содержащий:

-   поле **title** (Заголовок) типа str (строка)
-   поле **state** (Статус выполнения) типа str (строка):
    -   возможные значения - **in_progress** (выполняется) и **ready** (выполнена)
-   поле **estimate** (Срок выполнения) типа datetime.date (дата)
-   конструктор, принимающий на вход поля **title** и **estimate**, поле **state** по умолчанию **in_progress**
-   вычисляемый атрибут **remaining** (Осталось до окончания сроков) типа datetime.timedelta (разница по времени)
    -   формула - **estimate** минус **текущая дата**, если **state** равно **in_progress**, иначе **ноль**
-   вычисляемый атрибут **is_failed** (Задача провалена) типа bool (булевый тип)
    -   формула - если **state** равно **in_progress** и **estimate** меньше **текущая дата**
-   метод **ready**, производящий смену **state** на **ready**

Реализовать класс **Roadmap** (дорожная карта), содержащий:

-   поле **tasks** (задачи) типа list (список), где:
    -   каждый элемент списка - экземпляр класса **Task**
-   конструктор, принимающий (опционально) на вход поле **tasks**, по умолчанию - **пустой список**
-   вычисляемый атрибут **today** типа list (список)
    -   формула - все элементы **tasks**, где **estimate** равно **текущая дата**
-   метод **filter**, принимающий на вход аргумент **state** типа str (строка) и возвращающий в результате все элементы **tasks**, где **task.state** равно **state**

# Домашнее задание к лекции №4 (L4HW)

Реализовать wsgi-приложение выводящее список критичных задач, при этом критичными считаются просроченные задачи и задачи, до окончания срока которых осталось менее трех дней. Cписок задач необходимо получать из приложенного файла dataset.yml в секции dataset (схема описана в секции schema, порядок кортежей данных - **title**, **state**, **estimate**, пример чтения приведен в скрипте parse.py).

# Домашнее задание к лекции №5

В домашнем задании к лекции №3 мы описали класс реализующий сущность **Task** (Задача). Необходимо разработать представление и формы создания и редактирования для этой сущности. В случае успеха или неудачи заполнения форм нужно выводить соответствующие сообщения.

В домашнем задании к лекции №4 мы определили понятие "критичная задача" (критичными считаются просроченные задачи и задачи, до окончания срока которых осталось менее трех дней). В случае успеха заполнения формы необходимо вывести пользователю все поля сущности, если задача является критичной - необходимо веделить ее заголовок красным цветом.

Для решения поставленных задач необходимо применять фреймворк Django и его возможности (маршруты, представления, формы и валидацию форм, стандартные шаблоны).

### Форма создания

Форма создания должна содержать элементы:
-   поле **title** (Заголовок) типа str (строка)
-   поле **estimate** (Срок выполнения) типа datetime.date (дата)
-   кнопка "Сохранить", активирующая отправку формы на сервер

Поля формы создания имеют ограничения:
-   значение поля **estimate** (Срок выполнения) должно быть больше или равна сегодняшнему дню (date.today)
-   значения всех полей должны иметь соответствующий тип

### Форма редактирования

Форма редактирования должна содержать элементы:
-   поле **title** (Заголовок) типа str (строка)
-   поле **state** (Статус выполнения) типа str (строка):
    -   возможные значения - **in_progress** (выполняется) и **ready** (выполнена)
-   поле **estimate** (Срок выполнения) типа datetime.date (дата)
-   кнопка "Сохранить", активирующая отправку формы на сервер

Поля формы создания имеют ограничения:
-   значение поля **state** (Статус выполнения) должно быть одним из возможных значений

## Полезные ссылки

1.  [Машруты, URL dispatcher](https://docs.djangoproject.com/en/1.10/topics/http/urls/)
2.  [Представления, Views](https://docs.djangoproject.com/en/1.10/topics/http/views/)
3.  [Декораторы представлений, View decorators](https://docs.djangoproject.com/en/1.10/topics/http/decorators/)
4.  [Функции представлений, Shortcut functions](https://docs.djangoproject.com/en/1.10/topics/http/shortcuts/)
5.  [Формы, Forms](https://docs.djangoproject.com/en/1.10/topics/forms/)
6.  [Поля форм, Form fields](https://docs.djangoproject.com/en/1.10/ref/forms/fields/)
7.  [Валидация форм, Form validations](https://docs.djangoproject.com/en/1.10/ref/forms/validation/)

# Домашнее задание к лекции №6

В домашнем задании к лекции №3 мы описали классы реализующие сущности **Task** (Задача) и **Roadmap** (Дорожная карта). Необходимо описать Django-модели **Task** и **Roadmap**, с учетом того, что **Roadmap** относится к **Task** как один-ко-многим. Необходимо реорганизовать структуру маршрутов и представления для работы с моделями.

В домашнем задании к лекции №5 мы описали формы для сущности **Task** (Задача), необходимо их обновить с учетом последних изменений (используя Django Model Forms) и также реализовать формы для сущности **Roadmap** (Дорожная карта).

### Представления

1.  Представление **Список дорожных карт**, содержащее:
    -   Список записей **Roadmap** (Дорожная карта), где каждая запись сопровождается:
        -   ссылкой на просмотр задач дорожной карты
        -   ссылкой на удаление дорожной карты и всех ее задач
    -   Ссылку на создание новой записи **Roadmap** (Дорожная карта)
2.  Представление **Список задач**, содержащее:
    -   Список записей **Task** (Задача), отсортированных по статусу и срокам выполнения, где каждая запись сопровождается:
        -   полями задачи **title** (Заголовок), **state** (Статус выполнения) и **estimate** (Срок выполнения)
        -   ссылкой на изменение задачи
        -   ссылкой на удаление задачи
3.  Представление **Создание дорожно карты**
4.  Представление **Удаление дорожной карты и всех ее задач**
5.  Представление **Создание задачи**
6.  Представление **Изменение задачи**
7.  Представление **Удаление задачи**

### Маршруты

Каждая сущность должна быть определена собственным уникальным URL, для реализации этого требования использовать возможности задания параметров для маршрутов.

## Полезные ссылки

1.  [Машруты, URL dispatcher](https://docs.djangoproject.com/en/1.10/topics/http/urls/)
2.  [Подключение СУБД, Install database](https://docs.djangoproject.com/en/1.10/topics/install/#get-your-database-running)
3.  [Модели, Models](https://docs.djangoproject.com/en/1.10/topics/db/models/)
4.  [Формы моделй, Model Forms](https://docs.djangoproject.com/en/1.10/topics/forms/modelforms/)

# Домашнее задание к лекции №7
2	
3	В домашнем задании к лекции №6 мы описали классы моделей реализующие сущности **Task** (Задача) и **Roadmap** (Дорожная карта) и представления для работы с этими сущностями. Необходимо описать класс модели реализующий новую сущность **Scores** (Очки), содержащий:
4	-   ссылочное поле **task** (Задача) на модель **Task** (Задача)
5	-   поле **date** (Время зачисления) типа datetime.datetime (дата и время)
6	-   поле **points** (Количество зачисленных очков) типа decimal.Decimal (число)
7	
8	При завершении задачи (перевод в статус **ready**), мы должны добавлять пользователю некоторое количество очков. Значение должно расчитываться по формуле - (**today** - **create date** / **estimate** - **create date**) + (**estimate** - **create date** / **max estimate**), где:
9	-   **estimate** - ожидаемая дата завершения задачи
10	-   **today** - фактическая дата завершения задачи
11	-   **create date** - дата создания задачи
12	-   **max estimate** - максимально большой интервал времени **estimate** - **create date** зарегистрированный в системе (необходимо выбрать это значение из сохраненных записей модели **Task**)
13	
14	### Статистика
15	
16	Необходимо реализовать новое представление, выводящее пользователю системы статистику по его задачам для каждой дорожной карты задач.
17	
18	Представление должно содержать две таблицы данных:
19	-   Статистика "Созданные/Решенные", где значения сгруппированы по неделям и есть поля:
20	    -   поле **Номер недели** в году типа int (целое число)
21	    -   поле **Интервал дат** типа str (строка), где
22	        -   значение формируется по шаблону "Y-m-d / Y-m-d"
23	        -   начало интервала - первый день недели
24	        -   конец интервала - последний день недели
25	    -   поле **Создано** типа int (целое число), содержащее количество всех задач, созданных в указанный интервал
26	    -   поле **Решено** типа int (целое число), содержащее количество всех задач, переведенных в статус **ready**
27	-   Статистика "Очки", где значения сгруппированы по месяцам и есть поля:
28	    -   поле **Месяц** типа str (строка), где
29	        -   значение формируется по шаблону "Y-m"
30	    -   поле **Зачислено** типа decimal.Decimal (число), содержащее сумму очков, зачисленных в указаный интервал
31	
32	Для решения поставленных задач необходимо применять фреймворк Django и его возможности (модели, аггрегирующие функции, транзакции, маршруты, представления, стандартные шаблоны).
33	
34	## Полезные ссылки
35	
36	1.  [Запросы к СУБД, Queries](https://docs.djangoproject.com/en/1.11/topics/db/queries/)
37	2.  [Аггрегирующие запросы к СУБД, Aggregation](https://docs.djangoproject.com/en/1.11/topics/db/aggregation/)
38	3.  [Транзакции, Database transactions](https://docs.djangoproject.com/en/1.11/topics/db/transactions/)
39	
40	### Самостоятельная работа *
41	
42	Таблицы данных сложно воспринимать, для отображения статистической информации целесобразно использовать графики. Современные веб-приложения при этом активно используют такие javascript-библиотеки как, например, [D3](https://d3js.org/). Проект распространяется под BSD-лицензией, его [исходный код](https://github.com/d3/d3) можно найти на GitHub, там же присуствует и довольно полная [документация](https://github.com/d3/d3/wiki/Tutorials). Огромное количество примеров можно найти на [странице](https://bl.ocks.org/mbostock) Майка Бостока, основного контрибутора проекта D3.
43	
44	![D3.js](https://habrastorage.org/files/273/96e/849/27396e84912546b7b1c7f94ffe50b43f.jpg)
45	
46	#### Примечание
47	
48	\* Работа выполняется по желанию
