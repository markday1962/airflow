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
docker run --name airflow-postgres -e POSTGRES_PASSWORD=mysecretpassword -e POSTGRES_USER=airflow \
    -e POSTGRES_DB=airflow -p 5432:5432 -d postgres
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
http://localhost:31080/admin/
```

## Create first DAG
DAG's define our piplines and their location is defined in the airflow.cfg file
```
# The folder where your airflow pipelines live, most likely a
# subfolder in a code repository
# This path must be absolute
dags_folder = /home/markday/code/src/airflow/code/myairflow/dags
```
In our code directory create a python package called dags, the Airflow scheduler automatically looks in the dags folder 
for pipelines, once created create a dag file called my_first_dag.py and populate it with the following.
```
from airflow import DAG
from datetime import datetime, timedelta

default_arguments = {
    'owner': 'airflow',
    'start_date': datetime(2019, 5, 15, 0, 0, 0),
    'retries': 3,
    'retry_delay': timedelta(minutes=10)
}

dag = DAG(dag_id='my_first_dag',
          max_active_runs=5,
          schedule_interval='0 * * * *',
          default_args=default_arguments,
          catchup=False)
```
If the scheduler is running, my_first_dag will be visible in the web console `http://localhost:31080/admin/`

## Plugin structures
https://www.astronomer.io/guides/airflow-importing-custom-hooks-operators/

## Create python packages
$AIRFLOW_HOME/myairflow
$AIRFLOW_HOME/myairflow/lib
$AIRFLOW_HOME/myairflow/lib/airflow/plugins
$AIRFLOW_HOME/myairflow/lib/airflow/hooks
$AIRFLOW_HOME/myairflow/lib/airflow/operators
$AIRFLOW_HOME/myairflow/lib/airflow/sensors

## Creating our first plugin
Airflow has a simple plugin manager built-in that can integrate external features.
In $AIRFLOW_HOME/myairflow/lib/airflow/plugins, create a file called my_plugin.py and add the following code.
```
from airflow.plugins_manager import AirflowPlugin


class MyFirstPlugin(AirflowPlugin):
    name = 'my_first_plugin'
```

## Creating our first operator
An operator represents a single, ideally idempotent, task. Operators determine what actually executes when your DAG runs.
https://airflow.apache.org/docs/stable/howto/operator/index.html
In $AIRFLOW_HOME/myairflow/lib/airflow/operators, create my_first_operator.py and add the following code.
```
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
import logging as log


class MyFirstOperator(BaseOperator):

    @apply_defaults
    def __init__(self, param, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.param = param

    def execute(self, context):
        log.info(self.param)
```

## Populate DAGS
We now have a plugin that contains one operator, we can now add out newly created operator to our DAG, open my_first_dag.py
and import the newly created operator
```
from myairflow.lib.airflow.operators.my_first_operator import MyFirstOperator
```
add the following to the end of the file
```
...
task1 = MyFirstOperator(task_id='task_id1', param='some random text', dag=dag) # the param text will be printed by our operator

task1 # task dependency
```

## Creating our first sensor
An Airflow Sensor is a special type of Operator, typically used to monitor a long running task on another system.
In $AIRFLOW_HOME/myairflow/lib/airflow/sensors, create my_first_operator.py and add the following code.

```
from airflow.operators.sensors import BaseSensorOperator
from datetime import datetime


class MyFirstSensor(BaseSensorOperator):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def poke(self, context):
        current_minute = datetime.now().minute
        if current_minute % 2 != 0:
            return False
        task_instance = context['task_instance']
        task_instance.xcom_push('minute', current_minute)
        return True
```

##Updating the DAG
Import MyFirstSensor and add our second task (task2) and make it dependent on task1
```
from myairflow.lib.airflow.sensors.my_first_sensor import MyFirstSensor
...
    task2 = MyFirstSensor(task_id='task_id2', poke_interval=30)
    task2 >> task1
```

## Creating our first XCOM
XComs let tasks exchange messages, allowing more nuanced forms of control and shared state. The name is an abbreviation 
of “cross-communication”. XComs are principally defined by a key, value, and timestamp, but also track attributes 
like the task/DAG that created the XCom and when it should become visible. Any object that can be pickled can be 
used as an XCom value, so users should make sure to use objects of appropriate size.
In $AIRFLOW_HOME/myairflow/lib/airflow/sensors, create my_first_sensor.py and update the MyFirstSensor to push the minute 
value from our sensor
```
class MyFirstSensor(BaseSensorOperator):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def poke(self, context):
        current_minute = datetime.now().minute
        if current_minute % 2 != 0:
            return False
        task_instance = context['task_instance']                #xcom
        task_instance.xcom_push('minute', current_minute)       #xcom
        return True
```
Now the my_first_operator.py is updated to pull the minute value from task2 and log the value
```
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
import logging as log


class MyFirstOperator(BaseOperator):

    @apply_defaults
    def __init__(self, param, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.param = param

    def execute(self, context):
        task_instance = context['task_instance']
        minute = task_instance.xcom_pull('task_id2', key='minute')
        log.info(minute)
        log.info(self.param)
```

## Advanced techniques 
Airflow allows for more complex pipelines, in the next example we explored a branching pipeline.
In In $AIRFLOW_HOME/myairflow/dags create a new pipeline called branching.py and add the following code.
```
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import BranchPythonOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2019, 6, 27, 0, 0, 0),
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}


def some_condition():
    a = 1
    if a > 2:
        return 'second_pipeline'
    return 'first_pipeline'


dag = DAG(dag_id='branching',
          default_args=default_args,
          max_active_runs=4,
          schedule_interval='0 * * * *',
          catchup=False)

start_task = DummyOperator(task_id='start_task', dag=dag)

branch = BranchPythonOperator(task_id='validation', python_callable=some_condition, dag=dag)

first_pipeline = DummyOperator(task_id='first_pipeline', dag=dag)

second_pipeline = DummyOperator(task_id='second_pipeline', dag=dag)

first_pipeline_next_step = DummyOperator(task_id='first_pipeline_next_step', dag=dag)
second_pipeline_next_step = DummyOperator(task_id='second_pipeline_next_step', dag=dag)

start_task >> branch
branch >> first_pipeline >> first_pipeline_next_step
branch >> second_pipeline >> second_pipeline_next_step
```
The DummyOperator does literally nothing. It can be used to group tasks in a DAG. The task is evaluated by the scheduler 
but never processed by the executor.

## REST API
Airflow exposes an REST API. It is available through the webserver. Endpoints are available at /api/experimental/
https://airflow.apache.org/docs/stable/rest-api-ref.html

## Monitoring Airflow
Airflow can push metrics to a statsd service http://github.com/statsd/statsd, allowing metrics to be sent to a backend service like 
Graphite
```
docker run -d --name graphite --restart=always -p 80:80 -p 2003-2004:2003-2004  -p 2023-2024:2023-2024 \
-p 8125:8125/udp -p 8126:8126
```





