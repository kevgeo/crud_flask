# Flask_CRUD

This is a simple CRUD project which involves two Postgres tables, `users` and `posts`. Flask defines the API routes and backend logic. SQLAlchemy ORM is used to interact with Postgres by mapping python classes to database tables.

To start, first install required dependencies with the following command

`pip3 install -r requirements.txt`

[Install Postgres](https://www.postgresql.org/download/) and setup database server with username and password credentials. For instructions to install,

Create a .env(hidden file) which will store your database credentials. Example format like below
```
DB_USER=<username>
DB_PASSWORD=<password>
DB_HOST=localhost
DB_PORT=5432
DB_NAME=<db name>
```

Then create the tables in Postgres by running

`python3 create_tables.py`

Finally run the server by running below command and experiment with the website at `http://127.0.0.1:8000/api/home`

`python3 -m gunicorn "app:create_app()"`
