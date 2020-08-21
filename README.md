# airflow
Export airflow home directory
```
mkdir code && cd code
export AIRFLOW_HOME=~/code/src/airflow/code
echo $AIRFLOW_HOME
```
Update ~/.bashrc
```
export AIRFLOW_HOME=~/code/src/airflow/code
source ~/.bashrc
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

Open airflow.cfg and amend the following values
```
executor = LocalExecutor
sql_alchemy_conn = postgresql+psycopg2://airflow:mysecretpassword@localhost:5416/airflow
```
Apply the airflow db changes
```
airflow resetdb
```
Connect to the database and in the Schemas/public you will see the airflow tables

Start Scheduler, open a new terminal
```
cd $AIRFLOW_HOME
source venv/bin/activate
airflow scheduler
```

Start Webserver, open a new terminal, then connect to the UI via a browser
```
cd $AIRFLOW_HOME
source venv/bin/activate
airflow webserver -p 31080
http://localhost:31008/admin/
```
