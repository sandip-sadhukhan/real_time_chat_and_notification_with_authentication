## Real Time Chat and Notification

It is a real time chat & notification application with authentication among multiple users and admin.

- HTML
- CSS
- Javascript
- Bootstrap
- Django
- Channels
- Redis

### How to run locally

1. First clone the repo
2. Start the backend

```bash
$ cd backend
# activate a virtual env
$ python -m venv env
$ env\Scripts\activate
# install all the dependencies
$ pip install -r requirements.txt
# run the redis server
$ redis-server
# run the django server
$ django manage.py migrate
$ django mange.py runserver
```
