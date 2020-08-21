# airflow
Export airflow home directory
```
mkdir code && cd code
export AIRFLOW_HOME=$PWD
echo $AIRFLOW_HOME
```

## Installing dependencies
```
sudo apt install python3-virtualenv
```
Create virtual environment
```
virtualenv venv
source venv/bin/activate
touch requirements.txt
```
Add requirements to requirements.txt
```
apache-airflow[kubernetes, statsd, crypto]
psycopg2-binary
flask-bcrypt
```
Install dependencies
```
pip install -r requirements.txt
```
Set env variables related to the locale settings
```
export LANGUAGE=en_US.UTF8
export LANG=en_US.UTF8
export LC_ALL=en_US.UTF8
```
Pull docker postgres image
```
docker run --name airflow-postgres -e POSTGRES_PASSWORD=mysecretpassword -e POSTGRES_USER=airflow -e POSTGRES_DB=airflow -p 5432:5432 -d postgres
```
## Initialise Airflow
https://airflow.apache.org/docs/stable/start.html
```
airflow initdb
```
