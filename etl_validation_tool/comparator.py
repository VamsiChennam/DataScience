from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Iterable

if TYPE_CHECKING:
    from pyspark.sql import DataFrame, SparkSession

from etl_validation_tool.config import TablePair


@dataclass(slots=True)
class ValidationResult:
    table_pair: str
    source_count: int
    target_count: int
    mismatch_count: int
    pass_status: bool
    generated_sql: str


class TableComparator:
    def __init__(self, spark: "SparkSession", jdbc_connections):
        self.spark = spark
        self.jdbc_connections = jdbc_connections

    def load_table(self, connection_name: str, schema: str, table: str) -> "DataFrame":
        jdbc = self.jdbc_connections[connection_name]
        return (
            self.spark.read.format("jdbc")
            .option("url", jdbc.url)
            .option("dbtable", f"{schema}.{table}")
            .option("user", jdbc.user)
            .option("password", jdbc.password)
            .option("driver", jdbc.driver)
            .option("fetchsize", str(jdbc.fetchsize))
            .load()
        )

    def compare(
        self,
        table_pair: TablePair,
        cast_map: dict[str, str],
        repartition_count: int = 512,
    ) -> ValidationResult:
        from pyspark.sql import functions as F

        source = self.load_table(table_pair.source_connection, table_pair.source_schema, table_pair.source_table)
        target = self.load_table(table_pair.target_connection, table_pair.target_schema, table_pair.target_table)

        source_casted = apply_casts(source, cast_map).repartition(repartition_count)
        target_casted = apply_casts(target, cast_map).repartition(repartition_count)

        source_count = source_casted.count()
        target_count = target_casted.count()

        all_compare_columns = table_pair.compare_columns or sorted(cast_map.keys())

        source_keyed = source_casted.select(*(table_pair.join_keys + all_compare_columns))
        target_keyed = target_casted.select(*(table_pair.join_keys + all_compare_columns))

        mismatch = (
            source_keyed.alias("s")
            .join(target_keyed.alias("t"), on=table_pair.join_keys, how="fullouter")
            .where(build_mismatch_condition(all_compare_columns, F))
        )

        mismatch_count = mismatch.count()
        generated_sql = build_sql_preview(table_pair, all_compare_columns)
        return ValidationResult(
            table_pair=f"{table_pair.source_connection}:{table_pair.source_fqn} => {table_pair.target_connection}:{table_pair.target_fqn}",
            source_count=source_count,
            target_count=target_count,
            mismatch_count=mismatch_count,
            pass_status=(source_count == target_count and mismatch_count == 0),
            generated_sql=generated_sql,
        )


def apply_casts(df: "DataFrame", cast_map: dict[str, str]) -> "DataFrame":
    from pyspark.sql import functions as F

    out = df
    for col_name, cast_type in cast_map.items():
        if col_name in out.columns:
            out = out.withColumn(col_name, F.col(col_name).cast(cast_type))
    return out


def build_mismatch_condition(compare_columns: Iterable[str], F):
    condition = None
    for col_name in compare_columns:
        part = F.coalesce(F.col(f"s.{col_name}").cast("string"), F.lit("__NULL__")) != F.coalesce(
            F.col(f"t.{col_name}").cast("string"), F.lit("__NULL__")
        )
        condition = part if condition is None else (condition | part)
    return condition if condition is not None else F.lit(False)


def build_sql_preview(table_pair: TablePair, compare_columns: list[str]) -> str:
    key_join = " AND ".join([f"s.{k}=t.{k}" for k in table_pair.join_keys])
    compare_predicates = " OR ".join([
        f"COALESCE(CAST(s.{c} AS VARCHAR), '__NULL__') <> COALESCE(CAST(t.{c} AS VARCHAR), '__NULL__')"
        for c in compare_columns
    ])
    return (
        f"SELECT * FROM {table_pair.source_fqn} s FULL OUTER JOIN {table_pair.target_fqn} t ON {key_join} "
        f"WHERE {compare_predicates};"
    )
