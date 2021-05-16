# eLearning App

![Open Source Love svg1](https://badges.frapsoft.com/os/v1/open-source.svg?v=103) ![GitHub Open Issues](https://img.shields.io/github/issues/GitauHarrison/somasoma-eLearning-app) ![GitHub Closed Issues](https://img.shields.io/github/issues-closed/GitauHarrison/somasoma-eLearning-app) ![GitHub Pull Request Open](https://img.shields.io/github/issues-pr/GitauHarrison/somasoma-eLearning-app) ![GitHub Pull Request Closed](https://img.shields.io/github/issues-pr-closed/GitauHarrison/somasoma-eLearning-app) ![GitHub forks](https://img.shields.io/github/forks/GitauHarrison/somasoma-eLearning-app) ![GitHub Stars](https://img.shields.io/github/stars/GitauHarrison/somasoma-eLearning-app) ![GitHub License](https://img.shields.io/github/license/GitauHarrison/somasoma-eLearning-app)

## Overview
My intention with this project is to record my ideas on how to go about creating an e-learning site for school-attending learners. It will have a student side and a teacher side. The teacher uploads content and he or she can monitor the progress of the student. It is more less a simple **online school concept**.

## Features

* Client Registration and Authentication
* Teacher Registration and Authentication
* Two-factor Authentication
* Database Management

Comming Soon ...

* Comment Moderation
* In-app Video Conferencing Facilities
* Data Visualization
* Lesson scheduling
* Live language translation
* Text search

## Tools Used

* Flask web framework
* Python for programing
* Twilio Verify API for two-factor authenctication
* SQLite database
* Flask migrate to manage database migrations
* Flask login to handle login sessions
* Flask wtforms for secure web form creation
* Flask bootstrap for cross-browser responsiveness and styling
* Heroku for deployment

Coming soon ...

* Twilio Programmable Video
* Calendly for scheduling
* Language Translation API
* Elasticsearch

## Design

* [Somasoma eLearning App](https://www.figma.com/proto/uG0hCD0uuAYbWZIhjf6fPz/somasoma-eLearning-app?node-id=179%3A2&scaling=min-zoom&page-id=0%3A1) on Figma

## Deployed Application
* [somasoma eLearning](https://somasoma-elearning-app.herokuapp.com/) on Heroku


## Testing The Application Locally

* Clone this repo:
```
$ git clone git@github.com:GitauHarrison/somasoma-eLearning-app.git
```

* Move into the cloned directory:

```
$ cd somasoma-eLearning-app
```

* Create and activate your virtual environment:

```
$ mkvirtualenv somasoma-elearning # I am using virtualenvwrapper
```

* Install project dependencies within your active virtual environment:

```
(somasoma-elearning)$ pip3 install -r requirements.txt
```

* Start the flask server:

```
(somasoma-elearning)$ flask run
```

* Access the application on http://127.0.0.1:5000/

## Using The Application Locally

**As a student:**

![Student](app/static/images/somasoma_student.gif)

* Navigate to [_client registration page_](http://127.0.0.1:5000/auth/register/client)
* Create a new client (ensure you provide valid phone number and email)
* Check the flash messages and follow the instructions given
* You will be required to provide an authentication token sent to your phone before logging into your account
* Once logged into the student account, click on_Start Lesson_ button
* In the lesson page, you can paste a comment
* In the navbar _Profile_ link, you can check your own profile, all your posts
* Clicking another student's name will display that student's profile
* Secure your account by [_logging out_](http://127.0.0.1:5000/logout) when done

**As a teacher:**

![Teacher](app/static/images/somasoma_teacher.gif)

* Navigate to [_client registration page_](http://127.0.0.1:5000/auth/register/teacher)
* Create a new teacher (ensure you provide valid phone number and email)
* Check the flash messages and follow the instructions given
* You will be required to provide an authentication token sent to your phone before logging into your account
* Once logged into the teacher account, you will directed to your teacher profile
* In the navbar _Profile_ link, you can check your own profile, all your posts
* Secure your account by [_logging out_](http://127.0.0.1:5000/logout) when done

## Contributors

[![GitHub Contributors](https://img.shields.io/github/contributors/GitauHarrison/somasoma-eLearning-app)](https://github.com/GitauHarrison/somasoma-eLearning-app/graphs/contributors)<hr>





[![ForTheBadge built-with-love](http://ForTheBadge.com/images/badges/built-with-love.svg)](https://github.com/GitauHarrison/)