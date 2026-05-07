from __future__ import annotations

import argparse
import json
from pathlib import Path

from etl_validation_tool.comparator import TableComparator
from etl_validation_tool.config import JdbcConfig, TablePair, ValidationRunConfig
from etl_validation_tool.metadata import MetadataLoader
from etl_validation_tool.management_store import TestManagementStore
from etl_validation_tool.runner import ValidationRunner
from etl_validation_tool.sample_data import SampleDataConfig, SampleDataFactory
from etl_validation_tool.tableau_kpi_validator import KPIExpectation, TableauKPIValidator
from etl_validation_tool.testcase_generator import generate_pytest_module, generate_testcase_manifest
from etl_validation_tool.unstructured_validator import UnstructuredDataValidator


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def run_structured_validation(args, spark) -> list[dict]:
    connections = {row["name"]: JdbcConfig(**row) for row in load_json(args.connections)}
    pairs = [TablePair(**row) for row in load_json(args.table_mapping)]

    metadata_loader = MetadataLoader(spark, connections)
    comparator = TableComparator(spark, connections)
    runner = ValidationRunner(metadata_loader, comparator)

    run_config = ValidationRunConfig(run_id=args.run_id, table_pairs=pairs)
    results = runner.run(run_config)

    store = TestManagementStore(args.output / "test_management.db")
    for idx, pair in enumerate(pairs, start=1):
        tc_id = f"AUTO_TC_{idx:04d}"
        store.register_test_case(tc_id, f"Validate {pair.source_fqn} vs {pair.target_fqn}", f"{pair.source_fqn}->{pair.target_fqn}", "Auto")
    for idx, result in enumerate(results, start=1):
        store.save_result(args.run_id, f"AUTO_TC_{idx:04d}", result)

    manifest = generate_testcase_manifest(pairs, args.output / "generated_testcases.json")
    generate_pytest_module(manifest, args.output / "test_generated_cases.py")

    payload = [result.__dict__ for result in results]
    (args.output / "validation_results.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return payload


def run_unstructured_validation(args, spark) -> dict:
    config = SampleDataConfig(rows=args.unstructured_rows, partitions=args.unstructured_partitions)
    source, target = SampleDataFactory(spark).generate_unstructured_pair(config)
    result = UnstructuredDataValidator().compare(source, target)
    payload = result.__dict__
    (args.output / "unstructured_validation_results.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return payload


def run_tableau_kpi_validation(args) -> list[dict]:
    expectations = [KPIExpectation(**row) for row in load_json(args.kpi_expectations)]
    results = TableauKPIValidator().validate_from_csv(
        csv_path=args.tableau_export_csv,
        kpi_column=args.tableau_kpi_column,
        value_column=args.tableau_value_column,
        expectations=expectations,
    )
    payload = [r.__dict__ for r in results]
    (args.output / "tableau_kpi_validation_results.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description="ETL table validation runner")
    parser.add_argument("--connections", type=Path)
    parser.add_argument("--table-mapping", type=Path)
    parser.add_argument("--run-id", type=str, default="RUN_LOCAL")
    parser.add_argument("--output", type=Path, default=Path("artifacts"))

    parser.add_argument("--run-unstructured", action="store_true")
    parser.add_argument("--unstructured-rows", type=int, default=1_000_000)
    parser.add_argument("--unstructured-partitions", type=int, default=200)

    parser.add_argument("--run-tableau-kpi", action="store_true")
    parser.add_argument("--tableau-export-csv", type=Path)
    parser.add_argument("--tableau-kpi-column", type=str, default="kpi_name")
    parser.add_argument("--tableau-value-column", type=str, default="kpi_value")
    parser.add_argument("--kpi-expectations", type=Path)

    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)

    from pyspark.sql import SparkSession

    spark = (
        SparkSession.builder.appName("etl-validation")
        .config("spark.sql.shuffle.partitions", "2000")
        .config("spark.default.parallelism", "2000")
        .getOrCreate()
    )

    report: dict[str, object] = {}
    if args.connections and args.table_mapping:
        report["structured"] = run_structured_validation(args, spark)

    if args.run_unstructured:
        report["unstructured"] = run_unstructured_validation(args, spark)

    if args.run_tableau_kpi:
        if not args.tableau_export_csv or not args.kpi_expectations:
            raise ValueError("--run-tableau-kpi requires --tableau-export-csv and --kpi-expectations")
        report["tableau_kpi"] = run_tableau_kpi_validation(args)

    (args.output / "complete_validation_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    spark.stop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
