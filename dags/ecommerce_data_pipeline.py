from datetime import datetime

try:
    from airflow import DAG
    from airflow.operators import EmptyOperator

    with DAG(
        dag_id="ecommerce_data_pipeline",
        start_date=datetime(2026, 1, 1),
        schedule="@daily",
        catchup=False,
        tags=["ecommerce", "data-platform"],
    ) as dag:
        start = EmptyOperator(task_id="start")
        extract = EmptyOperator(task_id="extract_operational_data")
        transform = EmptyOperator(task_id="transform_data_lake_layers")
        quality = EmptyOperator(task_id="run_data_quality_checks")
        load = EmptyOperator(task_id="load_warehouse_models")
        end = EmptyOperator(task_id="end")

        start >> extract >> transform >> quality >> load >> end

except ImportError:
    # Allows static checks without Airflow installed.
    pass

