MySite

Version
____________________    
Version 1.0



Build and Runtime Requirements
________________________




Configuring the Project
________________________



About MySite
_________________________
1.  Live Chatting
2.  User Profiles
3.  Ability to create forum, subforums, posts and comments
4.  Ability to make Friends


Tech Stack
_________________________
1.  Django Framework
2.  MySQL database
3.  Websockets (Django channels https://channels.readthedocs.io/en/latest/ )
4.  Frontend - Javascript, JQuery, HTML, CSS, Bootstrap

Application Architexture
_________________________
The application includes 4 mini app's : accounts, chat, explore, and login. Each app controls a main feature of the application as described below.
1.  Accounts - The accounts mini app allows users to customize there personal information such as recent activity, friendslist, a short bio, and location. 
2.  Chat - 
3.  Explore - This is the main feature of the application and allows users to create forum and subforum topics along with posts in each subforum. Posts can be interacted with via "likes" and "dislikes" and comments.
4.  Login - Handles all user authentication. It allows a user to login or create an account if one does not exist. Account creation requires a full name, username, email and password and must be activated via email. If a username or password is forgotten it can be     resest via email.