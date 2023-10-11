# Mitto: Open Source Messenger

>Mitto is an open-source  messenger currently in development. This monorepo contains both the API and the frontend of the application.

### Author:
Danil Khabibullin 609-31m khabibullin@edu.surgu.ru
___

## Mitto's API 
It is RESTful API implemented by using FastAPI python framework.
+ Used authorization scheme: a pair of JWT (access + refresh)

## Mitto's frontend
It is single page application implemented by Angular/rxjs/TS stack 

## Prerequisites
+ Python
+ Node.js and npm
+ Angular CLI


## Цель проекта:
+ Изучение работы проектов со сложними ахритектурами
+ Готовых к работе с высокой нагрузкой

## Функции проекта:
+ Выделенный отдельный сервис для автоизации
+ Наличие кэща базы данных
+ Наличие брокера сообщений
+ Наличие "настоящей" параллельности
+ Интеграция с cybernates

## План на семестр
+ Внедрения кэша для базы данных
+ Вынесения авторизации в отдельный сервис
+ Добавление брокера сообщений

## Было сделано:
+ Создано приложение чат в виде монолита
+ В приложении присутствует база данных postgres
+ В приложении присутствует сервис авторизации (внутри монолита)