python manage.py makemigrations
python manage.py migrate
python manage.py loaddata initial_data/user.json
python manage.py loaddata initial_data/products.json
python manage.py loaddata initial_data/carts.json
python manage.py runserver 0.0.0.0:8000