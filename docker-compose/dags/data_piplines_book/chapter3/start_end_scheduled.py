from datetime import datetime
from pathlib import Path

import pandas as pd
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator

dag = DAG(
    dag_id="start_end_scheduled",
    start_date=datetime(year=2020, month=10, day=16),
    end_date=datetime(year=2020, month=10, day=19),
    schedule_interval="@daily",
)

# First fetch and store the events from the API
fetch_events = BashOperator(
    task_id="fetch_events",
    bash_command=(
        "mkdir -p /data/start_end && "
        "curl -o /data/start_end/events.json http://10.39.0.245:5000/events"
    ),
    dag=dag,
)

# Load the events, process, and write results to CSV
def _calculate_stats(input_path, output_path):
    """Calculates event statistics."""

    events = pd.read_json(input_path)
    stats = events.groupby(["date", "user"]).size().reset_index()

    Path(output_path).parent.mkdir(exist_ok=True)
    stats.to_csv(output_path, index=False)

# Calculate stats
calculate_stats = PythonOperator(
    task_id="calculate_stats",
    python_callable=_calculate_stats,
    op_kwargs={"input_path": "/data/start_end/events.json", "output_path": "/data/start_end/stats.csv"},
    dag=dag,
)

# Set order of execution
fetch_events >> calculate_stats
