```
pip3 install -r requirements.txt
docker run -e POSTGRES_DB="vectorizer" -e POSTGRES_USER="admiral" -e POSTGRES_PASSWORD="spaikbrawlstars" -p 2335:5432 -d postgres:15
export DB_NAME=vectorizer
export DB_USER=admiral
export DB_PASSWORD=spaikbrawlstars
export DB_HOST=localhost
export DB_PORT=2335
export DJANGO_SECRET_KEY=some_secret_key
export DJANGO_DEBUG=True
export IAM_TOKEN=<to generate token: https://yandex.cloud/ru/docs/iam/operations/iam-token/create>
python3 django_project/manage.py runserver
```