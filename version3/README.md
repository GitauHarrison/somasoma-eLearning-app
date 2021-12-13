# Somasoma eLearning Application

This is a sample eLearning application used to demonstrate how interactive virtual classes can take place. The people involved in this proeject will be a teacher, a student and a parent.

The student will be able to create a virtual class and a teacher will join the student's class. A parent will have access to the student's progress. Lesson content are made available to students for their won perusal.

Besides student-teacher interaction, there is also student-student interaction. This kind of interaction is referred to as _community_ in the application. Students can communicate with each other either about the lesson content (made available through a comments section in each lesson chapter) or in the _community center_ where discussions are open-ended and not limited to class-specific content.

## Features

- Student registration and authentication
- Teacher registration and authentication
- Parent registration and authentication
- Two-factor authentication
- Email notifications
- Credit card payment
- Scheduling for virtual classes
- Comment moderation

Comming soon:
- Video conferencing facility
- Live language translation
- Data visualization
- Live language translation

## Tools Used

- Python for programming
- Flask for web development
- SQLAlchemy for database management
- Bootstrap for styling
- Flask-WTF for form management
- Flask-Mail for email notifications
- Flask-Babel for internationalization
- Flask-Login for user authentication


## License

- MIT License

## Application Design

- [Somasoma eLearning Application on Figma](https://www.figma.com/proto/AzhdESXorALZD9F0rPUeEs/somasoma_version3_student?node-id=5%3A17&scaling=min-zoom&page-id=0%3A1&starting-point-node-id=5%3A17&show-proto-sidebar=1)

## Contributors

[![GitHub Contributors](https://img.shields.io/github/contributors/GitauHarrison/somasoma-eLearning-app)](https://github.com/GitauHarrison/somasoma-eLearning-app/graphs/contributors)

## Deployment

- [Somasoma]() on Heroku
- [Somasoma]() on Docker

## Testing the Application Locally

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

## Using the Application

### Student

- Explore the course you are interested in from the [landing page]().
- [Apply]() for a virtual class.
- Complete [registration]().
- [Enrol]() by making payment.
- Check your email for a confirmation email _(On Heroku this feature does not work)_.
- Click on the confirmation link to access your virtual classes.
- [Login]() to your virtual class.
- [Start]() your course.
- If you have a question or need clarification, leave a comment in the _comments section_ below each lesson chapter. The teacher will respond to your comment.
- You can create a new virtual class or join an existing one by clicking on the links in the _Live Class_ tab.
- Discover other students in the _community_ by clicking the _Community_ tab.
- You can learn more about another student by clicking on their names to see their profile.
- _Follow_ or _unfollow_ other students.
- You can manage your account by clicking on the _Account_ tab.
- See your _progress_ by clicking on the _Analytics_ tab.
- Once done, remember to [logout]().


<hr>

[![ForTheBadge built-with-love](http://ForTheBadge.com/images/badges/built-with-love.svg)](https://github.com/GitauHarrison/)