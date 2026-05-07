from pathlib import Path

from etl_validation_tool.tableau_kpi_validator import KPIExpectation, TableauKPIValidator


def test_validate_from_csv(tmp_path: Path):
    csv_path = tmp_path / "kpi.csv"
    csv_path.write_text("kpi_name,kpi_value\nRevenue,100\nOrders,50\n", encoding="utf-8")

    expectations = [
        KPIExpectation(name="Revenue", expected_value=100, tolerance_pct=0.0),
        KPIExpectation(name="Orders", expected_value=48, tolerance_pct=5.0),
    ]

    results = TableauKPIValidator().validate_from_csv(csv_path, "kpi_name", "kpi_value", expectations)
    assert len(results) == 2
    assert results[0].pass_status is True
    assert results[1].pass_status is True
