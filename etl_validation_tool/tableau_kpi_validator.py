from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass(slots=True)
class KPIExpectation:
    name: str
    expected_value: float
    tolerance_pct: float = 0.0


@dataclass(slots=True)
class KPIValidationResult:
    name: str
    expected_value: float
    actual_value: float
    difference_pct: float
    pass_status: bool


class TableauKPIValidator:
    """Compares KPI expectations against Tableau-exported data (CSV).

    This module intentionally uses CSV exports to stay environment-agnostic.
    Teams can integrate Tableau Server API fetch in pipeline before calling this validator.
    """

    @staticmethod
    def _read_csv(path: Path) -> list[dict[str, str]]:
        import csv

        with path.open("r", encoding="utf-8") as fh:
            return list(csv.DictReader(fh))

    def validate_from_csv(
        self,
        csv_path: Path,
        kpi_column: str,
        value_column: str,
        expectations: Iterable[KPIExpectation],
    ) -> list[KPIValidationResult]:
        rows = self._read_csv(csv_path)
        index = {row[kpi_column]: float(row[value_column]) for row in rows}

        results: list[KPIValidationResult] = []
        for item in expectations:
            actual = index[item.name]
            diff_pct = 0.0 if item.expected_value == 0 else abs((actual - item.expected_value) / item.expected_value) * 100
            results.append(
                KPIValidationResult(
                    name=item.name,
                    expected_value=item.expected_value,
                    actual_value=actual,
                    difference_pct=diff_pct,
                    pass_status=diff_pct <= item.tolerance_pct,
                )
            )
        return results
