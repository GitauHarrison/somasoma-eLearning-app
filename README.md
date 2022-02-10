![GitHub Open Issues](https://img.shields.io/github/issues/GitauHarrison/somasoma-eLearning-app) ![GitHub Closed Issues](https://img.shields.io/github/issues-closed/GitauHarrison/somasoma-eLearning-app) ![GitHub Pull Request Open](https://img.shields.io/github/issues-pr/GitauHarrison/somasoma-eLearning-app) ![GitHub Pull Request Closed](https://img.shields.io/github/issues-pr-closed/GitauHarrison/somasoma-eLearning-app) ![GitHub forks](https://img.shields.io/github/forks/GitauHarrison/somasoma-eLearning-app) ![GitHub Stars](https://img.shields.io/github/stars/GitauHarrison/somasoma-eLearning-app)

# somaSoma eLearning Application

This is a sample eLearning application used to demonstrate how interactive virtual classes can take place. The application users are teacher, student and  parent. There is also an admin user who has some super powers in the application.

![Student Dashboard](app/static/images/student_dashboard.png)

The application is built into two broad categories:
 - Website
   - [x] General information about course offerings
   - [x] Payment for course offerings
   - [x] Registration of students and their parents
   - [x] Public events
   - [x] Blog articles
   - [x] Anonymous user can leave comments on blog articles
   <br>
 - eLearning Application
    - [x] Only accessible upon payment and full parent and student registration
    - [x] Login details sent to parents and students via email
    - [x] Students can learn their courses here
    - [ ] Parents can view student progress
    - [x] Teachers can create courses and manage students
## Users

These are the custom roles and responsibilites of the users in the application:

### Admin

* Maintains the application
  - [x]  Registers teachers
  - [x] The only one who can delete teacher, parent and student accounts
  - [x] Can see all the registration details of teachers, parents and students
* Manages the content used by anonymous users of the application
  - [x] Update course offerings
  - [x] Comments moderation on student stories
  - [x] Student stories 

Comimg soon...
- Can see the usage statistics of the application by:
  - [ ] Teachers
  - [ ] Parents
  - [ ] Students

### Teacher

* General abilities:
  - [x] Can explore the application to find and follow other teachers
  - [x] Can see list of all students enrolled for the course they will be teaching
  - Can view individual student's profile:
    - [x] Personal registration details
    - [x] Student's individual comments in the eLearning community
    - [ ] Student's learning analytics
  - [x] Can only view what all students say in the eLearning community
<br>

* Manages individual lessons:
  - [x] Provides overview of course content
  - [x] Create lesson chapters for a course they registered for
  - [x] Can update course table of contents on the go
  - [x] Creates lesson objectives
  - [x] Creates learning objectives per chapter for each student
  - [x] Creates quizzes for each chapter
  - [x] Creates overall quiz for the course
<br>

* Student management:
  - [x] Moderation of student's comments in each course chapter
  - [x] Assesses student's achievements in each course chapter (automatic by the application)
  - [x] Assesses student's achievements in the overall course (automatic by the application)
<br>

* Event Management
  - [x] Teacher can create (and delete) events for students and the general public to attend
<br>

* Blog Management
  - [x] Teacher can only create blogs seen in the blogs page
  - [x] Teacher can allow the blog created to be posted in the public blog page of the application
  * Only the admin can delete these blogs written by teachers

### Student

* Course (resitricted to the course they registered for)
  - [x] Can enrol for only one course at a time
  - [x] Can do the overall quiz for the enrolled course
  - [x] Can post comments in each course chapter
<br>

* General
  - [x] Can explore all other students in the application
  - [x] Can follow or unfollow other students
  - Can view individual student's profile:
    - [x] Personal registration details
    - [x] Student's individual comments in the eLearning community
<br>

* Learning Analytics
  - Can view their own learning analytics:
    - [x] Each chapter's learning objectives
    - [x] Each chapter's quiz results
    - [x] Overall course quiz results
  - Can see how other students have achieved:
    - [ ] Each chaper objectives
    - [ ] Each chapter quizzes
    - [ ] Overall course quiz

### Parent

Coming soon...

## Features

- Student/Parent/Teacher/Admin registration and authentication
- Teacher/Admin authorization to create courses, manage students, and update application content
- Two-factor authentication
<br>

- Email notifications of new registrations and comments posted
- Credit card payment
- Scheduling for virtual classes
- Comment moderation
- Localhost testing on another device
- Basic email validation
- Beautiful phone number fields
- Profile popup on username:hover
- Sending and receiving private messages
- User notifications when they receive private messages
- Restriction of access to other lesson chapters if threshold of lesson objectives achieved is not met (80%)

Comming soon:
- [ ] Video conferencing facility
- [ ] Live language translation
- [ ] Data visualization of student performance
- [x] Markdown editing in forms
- [x] Google reCaptcha on forms for extra security aganist spam
- [x] Interactive tables (sorting, searching and pagination)

## Tools Used

- Python for programming
- Flask for web development
- SQLAlchemy for database management
- Bootstrap for styling and cross-browser responsiveness
- Flask-Moment for date and time formatting
- Flask-WTF for form management
- Flask-Mail for email notifications
- Flask-Login to manage user sessions
- Flask-Migrate to manage database migrations
- Stripe API for credit card payment (test mode)
- Twilio Verify API for two-factor authentication
- Ngrok for localhost testing
- Email validator for email addresses
- Phonenumber package for phone number formatting
- Python-dotenv to access environment variables
- DatatableJS for interactive tables
- Flask Pagedown for markdown editing
- Jquery and Ajax for profile popup and new message notification
- Google reCaptcha for extra security aganist spam
- Calendly for scheduling virtual classes


## License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Application Design

This application is currently on its **second** iteration. Over the months, I have reconsidered the design of the application and have added some new features.

- [Version 1 Design](https://www.figma.com/proto/uG0hCD0uuAYbWZIhjf6fPz/somasoma-eLearning-app?node-id=179%3A2&scaling=min-zoom&page-id=0%3A1) 

- [Version 2 Design](https://www.figma.com/proto/AzhdESXorALZD9F0rPUeEs/somasoma_version3_student?node-id=5%3A17&scaling=min-zoom&page-id=0%3A1&starting-point-node-id=5%3A17&show-proto-sidebar=1)

Kindly note that the current application may be miles ahead of the design seen in the latest version. During development, I may have added or discarded some things as the idea of the final application grows.


## Contributors

[![GitHub Contributors](https://img.shields.io/github/contributors/GitauHarrison/somasoma-eLearning-app)](https://github.com/GitauHarrison/somasoma-eLearning-app/graphs/contributors)

## Deployment

- [somaSoma eLearning App on Linode](www.bolderlearner.com) (currently live)
- [somaSoma eLearning App on Heroku]() (coming soon)
- [somaSoma eLearning App on Docker]() (coming soon)

## Testing the Application Locally

* Clone this repo:
```python
$ git clone git@github.com:GitauHarrison/somasoma-eLearning-app.git
```

* Move into the cloned directory:

```python
$ cd somasoma-eLearning-app
```

* Create and activate your virtual environment:

```python
$ mkvirtualenv somasoma-elearning # I am using virtualenvwrapper
```

* Install project dependencies within your active virtual environment:

```python
(somasoma-elearning)$ pip3 install -r requirements.txt
```

* Environment variables:
    * Create a file called `.env` in the root directory of the project
      ```python
      (somasoma-elearning)$ touch .env
      ```
    * Add the following lines to the file as seen in `.env-template`:
      ```python
      SECRET_KEY=
      TWILIO_ACCOUNT_SID=
      TWILIO_AUTH_TOKEN=
      TWILIO_VERIFY_SERVICE_ID=
      MAIL_SERVER=
      MAIL_PORT=
      MAIL_USE_TLS=
      MAIL_USERNAME=
      MAIL_PASSWORD=
      ADMINS=
      STRIPE_SECRET_KEY=
      STRIPE_PUBLISHABLE_KEY=
      STRIPE_WEBHOOK_SECRET=
      UPLOAD_PATH=
      ```
    * I am using Twilio Verify API and Stripe. Learn how to use them using the guides below:
      - [Twilio Verify API](https://github.com/GitauHarrison/notes/blob/master/how_to_use_stripe_for_payment.md)
      - [Stripe API](https://github.com/GitauHarrison/notes/blob/master/two_factor_authentication/twilio_verify_2fa.md)
* Start the flask server:

```python
(somasoma-elearning)$ flask run
```

* Access the application on http://127.0.0.1:5000/

## Using the Application

* [See video]() (as soon as project is complete)

## References

Big of an application, I have used several technologies to add features and put everything together. I have taken a note of some of these things and you can check them out for yourself to learn more.

1. [Starting A Flask Server](https://github.com/GitauHarrison/notes/blob/master/start_flask_server.md)
2. [Uploading files to a flask database](https://github.com/GitauHarrison/notes/blob/master/upload_files_to_database.md)
3. [Profile popup on hover](https://github.com/GitauHarrison/notes/blob/master/flask_popover/popover.md)
4. [Private messaging and user notifications](https://github.com/GitauHarrison/notes/blob/master/flask_popover/user_notifications.md)
5. [Deployment on Heroku](https://github.com/GitauHarrison/notes/blob/master/deploy_to_heroku.md)
6. [Deployment on Docker](https://github.com/GitauHarrison/notes/blob/master/deploy_to_docker.md)
7. [Deployment on Linode](https://github.com/GitauHarrison/notes/blob/master/deploy_to_linode.md)
8. [Comment moderation](https://github.com/GitauHarrison/notes/blob/master/comment_moderation.md)
9. [Two-factor authentication](https://github.com/GitauHarrison/notes/blob/master/two_factor_authentication/twilio_verify_2fa.md)
10. [Beautiful and interactive tables](https://github.com/GitauHarrison/notes/blob/master/flask_tables.md)
11. [Localhost testing](https://github.com/GitauHarrison/notes/blob/master/localhost_testing.md)
12. [Markdown editing in forms](https://github.com/GitauHarrison/notes/blob/master/handling_rich_text.md)
13. [Stripe integration](https://github.com/GitauHarrison/notes/blob/master/how_to_use_stripe_for_payment.md)
14. [Web form protection using captcha](https://github.com/GitauHarrison/notes/blob/master/recaptcha.md)

<hr>

[![forthebadge](https://forthebadge.com/images/badges/open-source.svg)](https://forthebadge.com) [![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)](https://forthebadge.com) [![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com) [![forthebadge](https://forthebadge.com/images/badges/uses-css.svg)](https://forthebadge.com) [![forthebadge](https://forthebadge.com/images/badges/uses-js.svg)](https://forthebadge.com)