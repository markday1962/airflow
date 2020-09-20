## Setting up a local airflow development environment

Create the airflow home environment
```
pwd
mkdir -p airflow/code
AIRFLOW_HOME=$PWD/airflow/code
echo $AIRFLOW_HOME
```
One the environment variable has been created update .bashrc to make it permanent

Installing virtualenv
```
cd $AIRFLOW_HOME
pip3 install virtual env
#sudo /usr/bin/easy_install virtualenv
virtualenv venv
source venv/bin/activate
```

Adding dependencies
In the virtual environment create the requirements.txt ile and add the following
```
apache-airflow[kubernetes, statsd, crypto]==1.10.5
psycopg-binary
werkzeug
flask-bcrypt
```
```
pip3 install -r requirements.txt
```
Now set some environment variables
```
export LANGUAGE=en_US.UTF-8
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8
```

### Initialise Postgresql
https://hub.docker.com/_/postgres
```
docker run --name postgres -e POSTGRES_PASSWORD=1q2w3e -e POSTGRES_USER=airflow -e POSTGRES_DB=airflow -p 5416:5432 -d postgres
```
## Initialise Airflow
```
airflow initdb
```
With airflow initialised our working directory will have a number of config files and a log directory
```
airflow.cfg
unittests.cfg
airflow.db
```
Update the airflow.cfg with the following settings
```
# executor = SequentialExecutor
executor = LocalExecutor

# sql_alchemy_conn = sqlite:////Users/markday/Training/airflow/code/airflow.db
sql_alchemy_conn = postgresql+psycopg2://airflow:1q2w3e@localhost:5416/airflow
```
Once the cfg has been updated the db must be reset replying Y to dropping the tables
```
airflow resetdb
```

Running the airflow scheduler
```
cd $AIRFLOW_HOME
source venv/bin/activate
airflow scheduler
```

Running the airflow webserver
```
cd $AIRFLOW_HOME
source venv/bin/activate
airflow webserver
```
