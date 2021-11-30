Run this commands to create virtualenv:
    ```
    python3 -m venv venv
    ```
    ```
    . venv/bin/activate
    ```
    ```
    pip install -r requirements.txt
    ```

Run this command to create .env:
    ```
    touch .env
    ```

Write your credentials in .env (example in env_example)

Open postgresql:
    ```
    psql (or sudo -u postgres psql)
    ```

Create database, which you wrote in .env DB_NAME

Run this commands to update your database:
    ```
    python3 manage.py migrate
    ```

Run this command to start server:
    ```
    python3 manage.py runserver
    ```

It can be accessed in http://localhost:8000/

To create superuser run:
    ```
    python3 manage.py createsuperuser
    ```
