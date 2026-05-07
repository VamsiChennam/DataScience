from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Dict, Iterable

from etl_validation_tool.config import JdbcConfig

if TYPE_CHECKING:
    from pyspark.sql import SparkSession


@dataclass(slots=True)
class ColumnMetadata:
    column_name: str
    data_type: str
    normalized_type: str


TYPE_GROUP_MAP: Dict[str, str] = {
    "tinyint": "integer",
    "smallint": "integer",
    "int": "integer",
    "integer": "integer",
    "bigint": "integer",
    "numeric": "decimal",
    "decimal": "decimal",
    "float": "floating",
    "real": "floating",
    "double": "floating",
    "double precision": "floating",
    "char": "string",
    "varchar": "string",
    "text": "string",
    "string": "string",
    "boolean": "boolean",
    "date": "date",
    "datetime": "timestamp",
    "timestamp": "timestamp",
    "timestamp_ntz": "timestamp",
}


class MetadataLoader:
    """Loads and normalizes table metadata from JDBC sources."""

    def __init__(self, spark: "SparkSession", jdbc_connections: dict[str, JdbcConfig]):
        self.spark = spark
        self.jdbc_connections = jdbc_connections

    def fetch_columns_from_information_schema(
        self,
        connection_name: str,
        schema: str,
        table: str,
    ) -> list[ColumnMetadata]:
        jdbc = self.jdbc_connections[connection_name]
        query = (
            "(SELECT column_name, data_type FROM information_schema.columns "
            f"WHERE table_schema = '{schema}' AND table_name = '{table}' "
            "ORDER BY ordinal_position) c"
        )
        frame = (
            self.spark.read.format("jdbc")
            .option("url", jdbc.url)
            .option("dbtable", query)
            .option("user", jdbc.user)
            .option("password", jdbc.password)
            .option("driver", jdbc.driver)
            .load()
        )
        return [
            ColumnMetadata(
                column_name=row["column_name"],
                data_type=row["data_type"],
                normalized_type=normalize_data_type(row["data_type"]),
            )
            for row in frame.collect()
        ]


def normalize_data_type(raw_data_type: str) -> str:
    cleaned = raw_data_type.lower().split("(")[0].strip()
    return TYPE_GROUP_MAP.get(cleaned, "string")


def harmonize_common_columns(
    source_columns: Iterable[ColumnMetadata],
    target_columns: Iterable[ColumnMetadata],
) -> dict[str, str]:
    """Returns common column => canonical cast type for fair comparison."""
    source_map = {c.column_name.lower(): c.normalized_type for c in source_columns}
    target_map = {c.column_name.lower(): c.normalized_type for c in target_columns}
    common = source_map.keys() & target_map.keys()

    result: dict[str, str] = {}
    for col in sorted(common):
        s = source_map[col]
        t = target_map[col]
        if s == t:
            result[col] = s
        elif "string" in {s, t}:
            result[col] = "string"
        elif {s, t} <= {"integer", "decimal", "floating"}:
            result[col] = "decimal"
        elif {s, t} <= {"date", "timestamp"}:
            result[col] = "timestamp"
        else:
            result[col] = "string"
    return result
