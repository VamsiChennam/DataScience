from __future__ import annotations

from dataclasses import dataclass

from etl_validation_tool.comparator import TableComparator, ValidationResult
from etl_validation_tool.config import ValidationRunConfig
from etl_validation_tool.metadata import MetadataLoader, harmonize_common_columns
from etl_validation_tool.tableau_kpi_validator import KPIValidationResult
from etl_validation_tool.unstructured_validator import UnstructuredValidationResult


@dataclass(slots=True)
class ExtendedValidationReport:
    table_results: list[ValidationResult]
    unstructured_results: list[UnstructuredValidationResult]
    tableau_kpi_results: list[KPIValidationResult]


class ValidationRunner:
    def __init__(self, metadata_loader: MetadataLoader, comparator: TableComparator):
        self.metadata_loader = metadata_loader
        self.comparator = comparator

    def run(self, config: ValidationRunConfig) -> list[ValidationResult]:
        results: list[ValidationResult] = []
        for pair in config.table_pairs:
            source_cols = self.metadata_loader.fetch_columns_from_information_schema(
                pair.source_connection, pair.source_schema, pair.source_table
            )
            target_cols = self.metadata_loader.fetch_columns_from_information_schema(
                pair.target_connection, pair.target_schema, pair.target_table
            )
            cast_map = harmonize_common_columns(source_cols, target_cols)
            results.append(self.comparator.compare(pair, cast_map, repartition_count=config.repartition_count))
        return results
