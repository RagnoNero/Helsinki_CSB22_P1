# Helsinki_CSB22_P1

LINK: https://github.com/RagnoNero/Helsinki_CSB22_P1

A course project with several cyber security flaws. This web application is a simple mailbox that allows a user to send messages to another.

Installation guides
Run python -m pip install django.

How to start
Run python manage.py migrate to create a database named db.sqlite3.
Run python manage.py runserver to start the app at http://127.0.0.1:8000/.
Click the "register" link, go to the registration page and create an account.

FLAW 1: SQL Injection
https://github.com/RagnoNero/Helsinki_CSB22_P1/blob/master/notes/views.py#L79-L85

Description: The application uses a SQL query notes_note (title, content, created_at, modified_at, user_id) values("%s","%s","%s","%s","%s")' % (title, content, dt_now, dt_now, request.user.id) to add a new note to the database. Since the query uses string formatting with the % operator, SQL queries included in the content will be executed, which can cause SQL injection.

Reproduction: Log in and go to the /note page, send *"content", "123", "123", 1);delete from notes_note;--* as the note content. Consequently, the query that will be executed is INSERT INTO notes_note (title, content, created_at, modified_at, user_id) VALUES (title, "content", "123", "123", 1);delete from notes_note;--”). This query will delete all the notes in the database.

How to fix it: Eliminate raw queries and use the database-abstraction APIs that Django provides. In the case of creating a new message, Notes.objects.create(...) can protect the application from SQL injection (https://github.com/RagnoNero/Helsinki_CSB22_P1/blob/master/notes/views.py#L87-L88).

FLAW 2: Cross-Site Scripting XSS
https://github.com/RagnoNero/Helsinki_CSB22_P1/blob/master/notes/templates/notes.html#L13

Description: The application does not validate or sanitize the title of the note. Consequently, an adversary can easily include some HTML scripts in the message. These scripts will be executed in the receiver’s browser when he retrieves his messages.

Reproduction: Go to the /note page, set a title to *<script> window.alert(document.cookie) </script>*. When the user goes to the /notes page, his cookie will pop up in the browser. This example script is not really harmful, however, a malicious user can use AJAX to send the cookie to his server.

How to fix it: Do not trust any data that users submitted and use the XSS filtering provided by the template system of Django. In 13. line of notes.html, {{note.title|safe}} means the application trusts the note.title is safe, which disables the XSS protection by Django. Removing *|safe* will enable the XSS filtering, which, for example, converts “<” to “&lt” and “>” to “&gt” so the script cannot be executed in the browser (https://github.com/RagnoNero/Helsinki_CSB22_P1/blob/master/notes/templates/notes.html#L14).

FLAW 3: Broken Authentication
https://github.com/RagnoNero/Helsinki_CSB22_P1/blob/master/notes/views.py#L25

Description: There is no validator in the registration to validate the security level of a password. Consequently, a user can use a well-known password such as “123” or “abc” for his account.

How to fix it: Use regular expressions to validate a password. For example, there can be a validator to check if a password is longer than a specific minimum length and another validator to check if a password contains both uppercase and lowercase letters as well as special symbols such as #, &, and %. There can also be a validator to check if a password is in the list of well-known passwords. Using validators can force a user to create a more completed password. Another option is generating a random password for users, the Django authentication system also provides a make_random_password method (https://docs.djangoproject.com/en/3.1/topics/auth/customizing/#django.contrib.auth.models.BaseUserManager.make_random_password) for the generation of random passwords.

FLAW 4: Sensitive data exposure
https://github.com/RagnoNero/Helsinki_CSB22_P1/blob/master/notes/views.py#L26 and https://github.com/RagnoNero/Helsinki_CSB22_P1/blob/master/notes/views.py#L43

Description: Passwords are not encrypted and are saved as plain text in the database. Once an adversary has access to the database or obtains the user list using SQL injection, he can directly obtain all passwords without cracking any encryption algorithm.

How to fix it: Encrypt passwords before saving them to the database in the registration. I used the md5 method which is not secure now for demonstration purposes. Also, it is desirable to use password management of Django that provides a make_password method (https://docs.djangoproject.com/en/1.8/topics/auth/passwords/#django.contrib.auth.hashers.make_password) for password encryption.

FLAW 5: Broken Access Control
https://github.com/RagnoNero/Helsinki_CSB22_P1/blob/master/notes/views.py#L61 and https://github.com/RagnoNero/Helsinki_CSB22_P1/blob/master/notes/views.py#L107

Description: The application contains a broken access control at the note and remove endpoints. In both examples the id provided in the query parameters are directly used to query/remove the note without proper validation/access control, a user can read or delete the note of other users.

How to fix it: This vulnerability can be fixed by implementing proper access control. In order to prevent users from spoofing their user ids, the user id of any given authenticated request should be determined by its session, not a request parameter (https://github.com/RagnoNero/Helsinki_CSB22_P1/blob/master/notes/views.py#L59 and https://github.com/RagnoNero/Helsinki_CSB22_P1/blob/master/notes/views.py#L105).

FLAW 6: Security Misconfiguration
https://github.com/RagnoNero/Helsinki_CSB22_P1/blob/master/Helsinki_CSB22_P1/settings.py#L26

Description: 1) The application runs in debug mode, which means stack traces will be revealed to the users on the web page if an error happens. 2) The application uses SQLite as its database. Since SQLite is a file-based data management system, anyone who knows the file's location can see its content. 3) settings.py includes the secret key in plain text.

How to fix it: 1) Disable the debug mode by setting DEBUG=False and adding http://127.0.0.1:8000/ to ALLOWED_HOSTS in settings.py. In this way, an error page such as a 404 or 400 page instead of error traces will be shown to users in the case of errors. 2) Use a separate database server such as MySQL and PostgreSQL instead of SQLite so that a separate account (with password) can be set for database maintenance. In this way, if an adversary does not know the password, he cannot see the content of the database even if he can access the server. 3) Save sensitive variables as environment variables in the production environment. The secret key can be retrieved by SECRET_KEY = os.environ[‘SECRET_KEY’].