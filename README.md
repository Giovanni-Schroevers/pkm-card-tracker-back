# pkm-card-trader-back

## Back-end setup

- Install python 3.7 and pip
- Run `pip install -r requirements.txt`
- Create a database
- Copy the `.env.example` and rename it to `.env`
- Edit the `.env` to match your settings
- Run `py manage.py migrate` to migrate your database
- Run `py manage.py loaddata data` to seed your database
- Run `py manage.py runserver` to start the dev server

Troubleshooting:
- Errors with the mysqlclient while installing the requirements
    - Download the cp37 version applicable to you https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysqlclient
    - Install it using `pip install [path-to-file]`
