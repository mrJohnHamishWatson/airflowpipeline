from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime
import os

dag_directory = os.path.dirname(os.path.abspath(__file__))


# Определение DAG
dag = DAG(
    'e_dag',
    description='Dag with extract step',
    schedule_interval=None,
    start_date=datetime(2023, 1, 1),
    catchup=False
)


install_deps = BashOperator(
    task_id='install_dependencies',
    bash_command=f'pip install -r {dag_directory}/extract_test_cli/requirements.txt',
    dag=dag
)

# Определение второго оператора PythonOperator
run_reddit = BashOperator(
    task_id='run_reddit',
    bash_command=f"python3 {dag_directory}/extract_test_cli/main.py get_reddit 10 memes ",
    dag=dag
)

run_flickr = BashOperator(
    task_id='run_flickr',
    bash_command=f"python3 {dag_directory}/extract_test_cli/main.py get_flickr 10 memes ",
    dag=dag
)

run_unsplash = BashOperator(
    task_id='run_unsplash',
    bash_command=f"python3 {dag_directory}/extract_test_cli/main.py get_unsplash 10 memes ",
    dag=dag
)

install_second_deps = BashOperator(
    task_id='install_second_deps',
    bash_command=f'pip install -r {dag_directory}/transform/requirements.txt',
    dag=dag
)

run_transform = BashOperator(
    task_id='run_transform',
    bash_command=f"python3 {dag_directory}/transform/transform.py transform ",
    dag=dag
)
# Установка зависимостей между задачами
run_reddit >> run_flickr >> run_unsplash >> install_second_deps >> run_transform
