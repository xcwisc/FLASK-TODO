# FLASK-TODO
This simple todo app is made to me to learn the `Flask` framework. It has basic user authentication and server side template rendering.

## Install Dependency
```bash
pip install -r requirements.txt
```

## Config
1. Make a file called config.py at the project's root directory.
2. Inside the file, make a class like this
```python3
class Config(object):
    SECRET_KEY = <YOUR_SECRET_KEY>
    RECAPTCHA_PUBLIC_KEY = <YOUR_RECAPTCHA_PUBLIC_KEY>
    RECAPTCHA_PRIVATE_KEY = <YOUR_RECAPTCHA_PRIVATE_KEY>
    SQLALCHEMY_DATABASE_URI = <YOUR_SQLALCHEMY_DATABASE_URI>

    # flask-mail config
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS: False
    MAIL_USE_SSL = True
    MAIL_USERNAME = <YOUR_MAIL_USERNAME>
    MAIL_PASSWORD = <YOUR_MAIL_PASSWORD>
```

## Create DB
To create DB, run:
```bash
$ python
>>> from app.models import db,User,Post
>>> db.create_all()
```

## Run locally
To test on your local machine, run:
```bash
python run.py
```
Navigate to http://localhost:3000/. The app will automatically reload if you change any of the source files.
