# somasoma eLearning App

![Open Source Love svg1](https://badges.frapsoft.com/os/v1/open-source.svg?v=103) ![GitHub Open Issues](https://img.shields.io/github/issues/GitauHarrison/somasoma-eLearning-app) ![GitHub Closed Issues](https://img.shields.io/github/issues-closed/GitauHarrison/somasoma-eLearning-app) ![GitHub Pull Request Open](https://img.shields.io/github/issues-pr/GitauHarrison/somasoma-eLearning-app) ![GitHub Pull Request Closed](https://img.shields.io/github/issues-pr-closed/GitauHarrison/somasoma-eLearning-app) ![GitHub forks](https://img.shields.io/github/forks/GitauHarrison/somasoma-eLearning-app) ![GitHub Stars](https://img.shields.io/github/stars/GitauHarrison/somasoma-eLearning-app) ![GitHub License](https://img.shields.io/github/license/GitauHarrison/somasoma-eLearning-app)

## Overview
My intention with this project is to record my ideas on how to go about creating an e-learning site for school-attending learners. It will have a student side and a teacher side. The teacher uploads content and he or she can monitor the progress of the student. It is more less a simple **online school concept**.

## Features

* Client Registration and Authentication
* Teacher Registration and Authentication
* Two-factor Authentication
* Database Management
* Email Notification
* Credit Card Payment

Coming Soon ...

* Comment Moderation
* In-app Video Conferencing Facilities
* Data Visualization
* Lesson scheduling
* Live language translation
* Text search
* Live App Email Notification

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
* Flask Mail for email support
* Stripe for online payment

Coming soon ...

* Twilio Programmable Video
* Calendly for scheduling
* Language Translation API
* Elasticsearch
* Twilio SendGrid for live app email support

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


## Email Support

* Both client and teacher will receive email notifications about their registration. 
* The client's parent gets an additional email about payment to ensure that the registration process is complete

Comming soon ...

* The client's parent will receive an email containing an attached payment reciept
* Whenever a student posts a comment in the class, the teacher will be notified via email about that particular comment
* The teacher will see the comment before other students for moderation. The teacher can _allow_ or _delete_ the student's comment
* If comment is allowed to appear in the class page, the student will be notified via email that their comment is now live. A link to check their live comment will be provided in the email.

NOTE:

Locally, email support is handled by `flask-mail` and it works well. However, on the deployed app, `flask-mail` email support does not work. I intend to use Twilio SendGrid to handle email support on the deployed app.

## Contributors

[![GitHub Contributors](https://img.shields.io/github/contributors/GitauHarrison/somasoma-eLearning-app)](https://github.com/GitauHarrison/somasoma-eLearning-app/graphs/contributors)

## References

* If you are not familiar with Flask, I recommend that you begin [here](https://github.com/GitauHarrison/notes/tree/master/web_development/personal_blog).
* Learn what `virtualenvwrapper` is and how to use it [here](https://github.com/GitauHarrison/notes/blob/master/virtualenvwrapper_setup.md).
* In a [previous article](https://github.com/GitauHarrison/notes/blob/master/twilio_sendgrid.md), I explained how Twilio SendGrid can be integrated into the app.
* Learn how to implement two-factor authentication in your flask app [here](https://github.com/GitauHarrison/notes/tree/master/two_factor_authentication).
* Check how _stripe_ can be added to a flask app [here](https://github.com/GitauHarrison/notes/blob/master/how_to_use_stripe_for_payment.md).


<hr>

[![ForTheBadge built-with-love](http://ForTheBadge.com/images/badges/built-with-love.svg)](https://github.com/GitauHarrison/)