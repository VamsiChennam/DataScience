from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pyspark.sql import DataFrame


@dataclass(slots=True)
class UnstructuredValidationResult:
    compared_rows: int
    exact_payload_matches: int
    normalized_text_matches: int
    json_schema_compatible_rows: int
    pass_status: bool


class UnstructuredDataValidator:
    """Validates semi/unstructured columns after structured table validation."""

    def compare(self, source: "DataFrame", target: "DataFrame", key_col: str = "doc_id") -> UnstructuredValidationResult:
        from pyspark.sql import functions as F

        joined = source.alias("s").join(target.alias("t"), on=[key_col], how="inner")

        exact_payload_matches = joined.where(F.col("s.payload_json") == F.col("t.payload_json")).count()
        normalized_text_matches = joined.where(
            F.lower(F.col("s.payload_text")) == F.lower(F.col("t.payload_text"))
        ).count()

        json_schema_compatible_rows = joined.where(
            F.get_json_object(F.col("s.payload_json"), "$.id").isNotNull()
            & F.get_json_object(F.col("t.payload_json"), "$.id").isNotNull()
            & F.get_json_object(F.col("s.payload_json"), "$.tier").isNotNull()
            & F.get_json_object(F.col("t.payload_json"), "$.tier").isNotNull()
        ).count()

        compared_rows = joined.count()
        pass_status = (
            compared_rows > 0
            and exact_payload_matches == compared_rows
            and normalized_text_matches == compared_rows
            and json_schema_compatible_rows == compared_rows
        )
        return UnstructuredValidationResult(
            compared_rows=compared_rows,
            exact_payload_matches=exact_payload_matches,
            normalized_text_matches=normalized_text_matches,
            json_schema_compatible_rows=json_schema_compatible_rows,
            pass_status=pass_status,
        )
