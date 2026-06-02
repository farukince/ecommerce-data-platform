import json
from datetime import datetime
from pathlib import Path

from pipelines.quality.data_quality_checks import run_all_quality_checks


QUALITY_REPORTS_PATH = Path("data_lake/quality_reports")


def write_quality_report(results: list[dict]) -> Path:
    QUALITY_REPORTS_PATH.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y_%m_%d_%H%M%S")
    output_path = QUALITY_REPORTS_PATH / f"quality_report_{timestamp}.json"

    summary = {
        "generated_at": datetime.now().isoformat(),
        "total_checks": len(results),
        "passed_checks": sum(1 for result in results if result["status"] == "passed"),
        "failed_checks": sum(1 for result in results if result["status"] == "failed"),
        "results": results,
    }

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(summary, file, ensure_ascii=False, indent=2)

    return output_path


def main() -> None:
    print("Starting data quality checks...")

    check_results = run_all_quality_checks()
    result_dicts = [result.to_dict() for result in check_results]

    for result in result_dicts:
        print(
            f"Check={result['check_name']} | "
            f"Table={result['table_name']} | "
            f"Status={result['status']} | "
            f"Failed rows={result['failed_rows']} | "
            f"Total rows={result['total_rows']}"
        )

    output_path = write_quality_report(result_dicts)

    failed_checks = [result for result in result_dicts if result["status"] == "failed"]

    print(f"Quality report created: {output_path}")

    if failed_checks:
        print("Some data quality checks failed.")
    else:
        print("All data quality checks passed.")


if __name__ == "__main__":
    main()