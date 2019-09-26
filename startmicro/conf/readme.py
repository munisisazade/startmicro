readme = """
# Readme Flask App
### Create new virtualenviroment on Python 3 ###
Bellow command you can create new virtualenv
```bash
python3 -m venv .venv
```
### Dotenv file make to .env file ###
Create new .env file and source enviroment variables
```bash
cp dotenv .env
source .env
```

### Migrate database ###
Create Postgresql database with migration
```bash
python manage.py db migrate
python manage.py db upgrade
```
### Runserver App ###

```bash
python run.py
```

"""
