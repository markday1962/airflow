from datetime import datetime
from pathlib import Path

import pandas as pd
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator

dag = DAG(
    dag_id="unscheduled",
    start_date=datetime(2015, 6, 1),
    schedule_interval=None,
)

# First fetch and store the events from the API
fetch_events = BashOperator(
    task_id="fetch_events",
    bash_command=(
        "mkdir -p /data/unscheduled && "
        "curl -o /data/unscheduled/events.json http://10.39.0.245:5000/events"
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
    op_kwargs={"input_path": "/data/unscheduled/events.json", "output_path": "/data/unscheduled/stats.csv"},
    dag=dag,
)

# Set order of execution
fetch_events >> calculate_stats