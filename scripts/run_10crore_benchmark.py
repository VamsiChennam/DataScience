"""Benchmark harness for 10 crore (100M) ETL validation dry-run with synthetic data.

Usage:
  python scripts/run_10crore_benchmark.py --rows 100000000 --partitions 2000
"""

from __future__ import annotations

import argparse
import json
import time

from pyspark.sql import SparkSession

from etl_validation_tool.sample_data import SampleDataConfig, SampleDataFactory
from etl_validation_tool.unstructured_validator import UnstructuredDataValidator


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--rows", type=int, default=100_000_000)
    parser.add_argument("--partitions", type=int, default=2000)
    args = parser.parse_args()

    spark = (
        SparkSession.builder.appName("etl-10crore-benchmark")
        .config("spark.sql.shuffle.partitions", str(args.partitions))
        .config("spark.default.parallelism", str(args.partitions))
        .getOrCreate()
    )

    factory = SampleDataFactory(spark)
    config = SampleDataConfig(rows=args.rows, partitions=args.partitions)

    started = time.time()
    source, target = factory.generate_unstructured_pair(config)
    result = UnstructuredDataValidator().compare(source, target)
    elapsed = time.time() - started

    print(json.dumps({"rows": args.rows, "elapsed_seconds": elapsed, **result.__dict__}, indent=2))
    spark.stop()


if __name__ == "__main__":
    main()
