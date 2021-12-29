from airflow.models import DAG
from datetime import datetime

default_args = {
	'start_date': datetime(2021, 12, 28)
}

with DAG('user_processing', 
	schedule_interval="@daily", 
	start_date=default_args,
	catchup=False) as dag:
	# define tasks/ops

