## Starting your web project

This file is meant to assist with starting your Django project. Note that a Django project will necessarily involve a more sophisticated set of tools than either of the other projects. Django will do a lot of the heavy lifting for you, but that doesn't mean it isn't happening, and therefore it can still easily break your project if you aren't sufficiently aware of what you are doing!

### A Web App

A web application has a few key components:
- Server - A computer that is a running your Django application and responds to http requests.
- Database - A sophisticated application in its own right, a database is a software tool that manages a data set in a way that supports rapid additions, updates, relationships, and lookups.SQLite by default in Django.
  - Databases manage all of the persistent information needed for a web application to run. For example, facebook's database will store all of your messages as text, and images you upload as pictures. These things aren't stored in (server) program memory for any significant portion of time.
- Client - A requester who interacts with your server, typically a browser that both generates appropriate http requests and renders the result in a human readable / interactive form.

Django and the book will lead you to use a few other tools:
- A virtual environment - This is a contained folder that allows you to install python packages which are only accessible from within the virtual environment.
- manage.py - This is a special script that allows you to interact with your web application through Django's interface.
- The views/urls/models architecture:
  - views.py - in any app, this is the code that is responsible for responding to a request and returning something for the client to view (e.g. an html page).
    - Templates are a helpful tool for programmatically generating said web pages using python and some HTML.
  - urls.py - in any app, this determines how requests get routed to views.py functions.
  - models.py - in any app, this determines what data is stored in your database, in a slightly more rigorous definition of class attributes than vanilla python.

### Startup

#### Virtual Environment

You'll need to make a virtual environment to follow along with the book (and it's good practice for project development). Basically all that means is doing the below steps and pip installing Django in that environment. You will need to do this the first time you start a project and any time you copy over the files from a checkpoint.

Linux / WSL:

```bash
python -m venv ll_env
source ll_env\bin\activate
```

Windows:

```cmd
python -m venv ll_env
ll_env\Scripts\Activate
```

If the above fails for permissions errors, try the below and then reattempt to activate the venv:

```cmd
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

You'll see something like this in your terminal when successful:

```cmd
(ll_env) PS C:\Users\bruce.wayne...>
```

To exit a virtual environment:

```bash
deactivate
```

Next, install Django:

```bash
pip install --upgrade pip
pip install django
```

If running manage.py doesn't work after doing the above, you may need to preface the above commands with `python -m` in a windows environment.

#### Starting a project and basic commands

(Inside your virtual environment)
To start from a completely blank slate, use the following (change ll_project to whatever your project will be called, or keep it if following along with the book examples). The second command makes a new app. _If you are copying the files over from a checkpoint or resuming work, you wont need to do the below which creates the initial files._

```bash
django-admin startproject ll_project .
python manage.py startapp learning_logs
```

The following three commands tell Django to update the database with whatever changes you've made to any models.py files, then run the server:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

#### Django Admin Site + Django Shell

The **admin site** is covered on page 381 of your textbook. It is a convenient GUI / Web interface to inspect and modify the state of your database (you can, for example, see users and other data, or change it). You cannot, however, change your website itself from here.

The **Django shell** allows you to programmatically (from the command line) interact with your database in exactly the same way you will interact with it from your views.py or other python scripts that form your Django app. You enter it as follows (see example usage on page 386):

```bash
python manage.py shell
```