from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pyspark.sql import DataFrame, SparkSession


@dataclass(slots=True)
class SampleDataConfig:
    rows: int = 100_000_000  # 10 crore
    partitions: int = 2000
    seed: int = 17


class SampleDataFactory:
    """Generates synthetic ETL source/target tables for stress and regression tests."""

    def __init__(self, spark: "SparkSession"):
        self.spark = spark

    def generate_structured_pair(self, config: SampleDataConfig) -> tuple["DataFrame", "DataFrame"]:
        from pyspark.sql import functions as F

        base = self.spark.range(0, config.rows, 1, numPartitions=config.partitions)
        source = (
            base.withColumnRenamed("id", "order_id")
            .withColumn("customer_id", (F.col("order_id") % 1_000_000).cast("long"))
            .withColumn("order_total", (F.col("order_id") * F.lit(0.93)).cast("decimal(18,2)"))
            .withColumn("order_status", F.when(F.col("order_id") % 7 == 0, F.lit("HOLD")).otherwise(F.lit("BOOKED")))
            .withColumn("updated_at", F.current_timestamp())
        )

        target = (
            source.withColumn("order_total", F.col("order_total").cast("double"))
            .withColumn("customer_id", F.col("customer_id").cast("int"))
        )
        return source, target

    def generate_unstructured_pair(self, config: SampleDataConfig) -> tuple["DataFrame", "DataFrame"]:
        from pyspark.sql import functions as F

        base = self.spark.range(0, config.rows, 1, numPartitions=config.partitions)
        source = (
            base.withColumnRenamed("id", "doc_id")
            .withColumn("payload_json", F.to_json(F.struct(F.col("doc_id").alias("id"), (F.col("doc_id") % 5).alias("tier"))))
            .withColumn("payload_text", F.concat(F.lit("Invoice-"), F.col("doc_id")))
        )
        target = source.withColumn("payload_text", F.upper(F.col("payload_text")))
        return source, target
