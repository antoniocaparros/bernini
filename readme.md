# init db and start project:
`docker-compose up --build`

# check tests
`docker-compose run web python manage.py test`

## url
`localhost:8000/api/`

## schema
`localhost:8000/`

# TO-DO:
- Tests
- Autenticar por Token
- App reutilizables

# users:
- Usuario: admin password: admin --> es admin and staff
- Usuario: staff password: staff --> es staff
- Usuario: prueba password: prueba --> es cliente normal
