# The battle of the hashtags

A django application that periodically checks the number of typos for all tweets that contain a given hashtag over a given period of time. In a "battle", at the end of the battle period, the number of typos are compared and the hashtag with the most typos is the winner.

### requirements
* python 3+

I have purposely not used Python 3.6 new string formatting to ensure ease of installation

### Installation
* clone the project
* (optional) create a virtualenv
* in the project folder, run `pip install -r requirements.txt`
* run migrations `python manage.py migrate`

##### Non production
* create admin account, run `python manage.py createsuperuser`

### How to start the application

##### prerequisits
You will need to set environment variables for the following:
* DJANGO_KEY
* TWITTER_CONSUMER_KEY
* TWITTER_CONSUMER_SECRET
* TWITTER_TOKEN_KEY
* TWITTER_TOKEN_SECRET

once these are set you can start the application by running the following:
```cmd
python manage.py runserver
```

### Lookup battle using battle id
To lookup a battle using a battle id, run the following url structure:
```
http://localhost:8000/api/battles/:id/
```

### Todo
* allow battles to be created using POST requests
* dockerize project
* add a front-end for creating battles
* allow a user to specify other attributes for comparison
