from datetime import datetime, timedelta

try:
    from airflow import DAG
    from airflow.operators.empty import EmptyOperator
    from airflow.operators.python import PythonOperator
    from pipelines.load.warehouse_loader import load_warehouse_models
    from apps.data_generator.main import main as generate_synthetic_data
    from pipelines.extract.extract_postgres_to_raw import extract_postgres_to_raw
    from pipelines.quality.run_quality_checks import main as run_data_quality_checks
    from pipelines.transform.bronze_to_silver import convert_all_bronze_to_silver
    from pipelines.transform.raw_to_bronze import convert_all_raw_to_bronze
    from pipelines.transform.silver_to_gold import build_all_gold_datasets

    SOURCE_TABLES = [
        "users",
        "sellers",
        "categories",
        "products",
        "product_inventory",
        "orders",
        "order_items",
        "payments",
        "shipments",
        "returns",
        "click_events",
        "cart_events",
    ]

    default_args = {
        "owner": "data-platform",
        "depends_on_past": False,
        "retries": 1,
        "retry_delay": timedelta(minutes=5),
    }

    with DAG(
        dag_id="ecommerce_data_pipeline",
        description="End-to-end ecommerce data pipeline from PostgreSQL to raw, bronze, silver, gold and quality checks.",
        default_args=default_args,
        start_date=datetime(2026, 1, 1),
        schedule="@daily",
        catchup=False,
        tags=["ecommerce", "data-platform", "data-quality"],
    ) as dag:
        start = EmptyOperator(task_id="start")

        generate_data = PythonOperator(
            task_id="generate_data",
            python_callable=generate_synthetic_data,
        )

        extract_postgres_data = PythonOperator(
            task_id="extract_postgres_data",
            python_callable=extract_postgres_to_raw,
        )

        write_raw_layer = EmptyOperator(
            task_id="write_raw_layer",
        )

        transform_raw_to_bronze = PythonOperator(
            task_id="transform_raw_to_bronze",
            python_callable=convert_all_raw_to_bronze,
            op_kwargs={"table_names": SOURCE_TABLES},
        )

        transform_bronze_to_silver = PythonOperator(
            task_id="transform_bronze_to_silver",
            python_callable=convert_all_bronze_to_silver,
            op_kwargs={"table_names": SOURCE_TABLES},
        )

        run_quality_checks = PythonOperator(
            task_id="run_quality_checks",
            python_callable=run_data_quality_checks,
        )

        build_gold_tables = PythonOperator(
            task_id="build_gold_tables",
            python_callable=build_all_gold_datasets,
        )

        load_warehouse = PythonOperator(
            task_id="load_warehouse",
            python_callable=load_warehouse_models,
        )

        end = EmptyOperator(task_id="end")

        (
            start
            >> generate_data
            >> extract_postgres_data
            >> write_raw_layer
            >> transform_raw_to_bronze
            >> transform_bronze_to_silver
            >> run_quality_checks
            >> build_gold_tables
            >> load_warehouse
            >> end
        )

except ImportError:
    # Allows static checks without Airflow installed locally.
    pass