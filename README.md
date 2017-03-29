# The battle of the hashtags

A django application that periodically checks the number of typos for all tweets that contain a given hashtag over a given period of time. In a "battle", at the end of the battle period, the number of typos are compared and the hashtag with the most typos is the winner.

### requirements
* python 3+

I have purposely not used Python 3.6 new string formatting to ensure ease of installation

### Installation
* clone the project
* create a virtualenv (optional) 
* install requirements - `pip install -r requirements.txt`
* run migrations - `python manage.py migrate`
* collect static content - `python manage.py collectstatic`
* create admin account - `python manage.py createsuperuser`

### How to start the application

##### prerequisits
You will need to set environment variables for the following:
* DJANGO_KEY
* TWITTER_CONSUMER_KEY
* TWITTER_CONSUMER_SECRET
* TWITTER_TOKEN_KEY
* TWITTER_TOKEN_SECRET

Once these are set you can start the application by running the following:
```cmd
python manage.py runserver
```
Then open a new terminal window and navigate to you project path (and activate your virtualenv if you created one) and run the following:
```cmd
python manage.py celery beat
```
That's it! you're now ready to login and start creating battles.

### Create battles
Battle can be created either by an admin user in the admin panel:
```
http://localhost:8000/admin/
```

or by POST request using the following data format:
```json
{
  'name': 'test battle',
  'hashtag_1': {'name': 'london'},
  'hashtag_2': {'name': 'cambridge'},
  'start': '2017-03-01 13:00:00',
  'end': '2017-03-01 14:00:00'
}
```
### Lookup battle using battle id
To lookup a battle using a battle id use the following url structure (replacing :id with the battle id):
```
http://localhost:8000/api/battles/:id/
```

### Todo
* extend the battle serializer to show more detailed tweet info
* dockerize project
* add a front-end for creating battles
* allow a user to specify other attributes for comparison
