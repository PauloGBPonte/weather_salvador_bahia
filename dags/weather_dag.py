from datetime import datetime, timedelta
# pyrefly: ignore [missing-import]
from airflow.decorators import dag, task
from pathlib import Path
import sys, os

sys.path.insert(0, '/opt/airflow')

from src.extract_data import extract_weather_data
from src.load_data import load_data_to_bigquery
from src.transform_data import data_transformations
from dotenv import load_dotenv

env_path = Path(__file__).parent.parent / 'config' / '.env'
load_dotenv(dotenv_path=env_path)


API_KEY = os.getenv('API_KEY')
url = f'http://api.openweathermap.org/data/2.5/weather?q=Salvador,BR&units=metric&appid={API_KEY}'

@dag(
    dag_id='weather_pipeline',
    default_args={
        'owner': 'airflow',
        'depends_on_past': False,
        'retries': 2,
        'retry_delay': timedelta(minutes=5)
    },
    description='Pipeline ETL - Clima Salvador',
    schedule='0 */1 * * *',
    start_date=datetime(2026, 2, 7),
    catchup=False,
    tags=['weather', 'etl']
)
def weather_pipeline():
    @task
    def extract():
        extract_weather_data(url)

    @task
    def transform():
        df = data_transformations()
        df.to_parquet('/opt/airflow/data/temp_data.parquet', index=False)

    @task
    def load():
        import pandas as pd
        df = pd.read_parquet('/opt/airflow/data/temp_data.parquet')
        load_data_to_bigquery(df)  # apenas df, sem o nome da tabela

    # Encadeamento: define a ordem de execução das tasks
    extract() >> transform() >> load()


weather_pipeline()