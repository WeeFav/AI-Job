from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.standard.operators.python import BranchPythonOperator
from airflow.models.param import Param
from scrape_linkedin import scrape_linkedin
from scrape_jobright import scrape_jobright

def branch(jobsite):
    if jobsite == "LinkedIn":
        return "task_scrape_linkedin"
    elif jobsite == "Jobright":
        return "task_scrape_jobright"

with DAG (
    dag_id = 'main_pipeline',
    params={
        'jobsite': Param("LinkedIn", enum=["LinkedIn", "Jobright"]),
        'jobs_to_scrape': Param(10, type="integer")
    },
    render_template_as_native_obj=True
) as dag:
    
    task_branch = BranchPythonOperator(
        task_id='task_branch',
        python_callable=branch,
        op_args=[
            "{{ params.jobsite }}"
        ],
        dag=dag
    )
    
    task_scrape_linkedin = PythonOperator(
        task_id="task_scrape_linkedin",
        python_callable=scrape_linkedin,
        op_args=[
            "{{ params.jobs_to_scrape }}"
        ]        
    )
    
    task_scrape_jobright = PythonOperator(
        task_id="task_scrape_jobright",
        python_callable=scrape_jobright,
        op_args=[
            "{{ params.jobs_to_scrape }}"
        ]        
    )
    
    task_branch >> [task_scrape_linkedin, task_scrape_jobright]