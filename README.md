MySite

Version

---

Version 1.0

Build and Runtime Requirements

---

python>=3.7
virtualenv

Configuring the Project

---

1. Download repo onto your local machine
2. \$ cd mysite/
3. create two new text file in current directory. (1) "password.txt" (2) "email.txt". Store your email password and email address (must be gmail) respectively.
4. \$ source backend-env/bin/activate
5. \$ python manage.py runserver
6. In a browser (preferably Chrome Incognito) navigate to http://localhost:8000/
7. From there you will need to create an account and activate your account via email (you will get an email from the email provided in "email.txt").

About MySite

---

1.  Live Chatting
2.  User Profiles
3.  Ability to create forum, subforums, posts and comments
4.  Ability to make Friends

Tech Stack

---

1.  Django Framework
2.  MySQL database
3.  Websockets (Django channels https://channels.readthedocs.io/en/latest/ )
4.  Frontend - Javascript, JQuery, HTML, CSS, Bootstrap

Application Architexture

---

The application includes 4 mini app's : accounts, chat, explore, and login. Each app controls a main feature of the application as described below.

1.  Accounts - The accounts mini app allows users to customize there personal information such as recent activity, friendslist, a short bio, and location.
2.  Chat - This app allows you to create chat rooms with your friends.
3.  Explore - This is the main feature of the application and allows users to create forum and subforum topics along with posts in each subforum. Posts can be interacted with via "likes" and "dislikes" and comments.
4.  Login - Handles all user authentication. It allows a user to login or create an account if one does not exist. Account creation requires a full name, username, email and password and must be activated via email. If a username or password is forgotten it can be resest via email.
