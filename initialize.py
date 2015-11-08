python manage.py runserver 0.0.0.0:8000
python manage.py makemigrations polls



Change your models (in models.py).
Run python manage.py makemigrations to create migrations for those changes
Run python manage.py migrate to apply those changes to the database.


First we’ll need to create a user who can login to the admin site. Run the following command:

$ python manage.py createsuperuser