from airflow import DAG
from elasticsearch_plugin.hooks.elastic_hook import ElasticHook
from elasticsearch_plugin.operators.postgres_to_elastic import PostgresToElasticOperator
from airflow.operators.python import PythonOperator

from datetime import datetime

default_args = {
	'start_date': datetime(2022, 2, 2)
}


def _print_es_info():
	hook = ElasticHook()
	print(hook.info())

# wrong name :(
with DAG('elasticsearch_default', schedule_interval='@daily', 
	default_args=default_args, catchup=False) as dag:
		print_es_info = PythonOperator(
			task_id='print_es_info',
			python_callable=_print_es_info
		) 

		connections_to_es = PostgresToElasticOperator(
			task_id='connections_to_es',
			sql='SELECT * FROM connection',
			index='connections'
		)

		print_es_info >> connections_to_es