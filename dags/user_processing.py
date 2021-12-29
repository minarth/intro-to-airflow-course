from airflow.models import DAG
# To get available ops, run: airflow providers list
from airflow.providers.sqlite.operators.sqlite import SqliteOperator
from airflow.providers.http.sensors.http import HttpSensor
from datetime import datetime

default_args = {
	'start_date': datetime(2021, 12, 28)
}

with DAG('user_processing', 
	schedule_interval="@daily", 
	default_args=default_args,
	catchup=False) as dag:
	
	# You can test this by running:
	# airflow tasks test user_processing creating_table 2021-12-28
	creating_table = SqliteOperator(
		task_id='creating_table',
		sqlite_conn_id='db_sqlite',   # defined in admin->connections
		sql='''
			CREATE TABLE users (
				firstname TEXT NOT NULL, 
				lastname TEXT NOT NULL, 
				country TEXT NOT NULL, 
				username TEXT NOT NULL, 
				password TEXT NOT NULL,
				email TEXT NOT NULL PRIMARY KEY
			);
		'''		
	)

	# You can test this by running:
	# airflow tasks test user_processing is_api_available 2021-12-28
	is_api_available = HttpSensor(
		task_id='is_api_available',
		http_conn_id='user_api',  # defined in admin->connections
		endpoint='api/'
	)