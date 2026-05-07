import pytest

from etl_validation_tool.metadata import ColumnMetadata, harmonize_common_columns, normalize_data_type


@pytest.mark.parametrize(
    "raw,expected",
    [
        ("DECIMAL(18,2)", "decimal"),
        ("VaRChAr(100)", "string"),
        ("timestamp_ntz", "timestamp"),
        ("unknown_custom", "string"),
    ],
)
def test_normalize_data_type_variants(raw, expected):
    assert normalize_data_type(raw) == expected


def test_harmonize_common_columns_promotes_numeric_to_decimal():
    source = [ColumnMetadata("id", "int", "integer"), ColumnMetadata("amount", "double", "floating")]
    target = [ColumnMetadata("id", "bigint", "integer"), ColumnMetadata("amount", "decimal(16,2)", "decimal")]
    cast_map = harmonize_common_columns(source, target)

    assert cast_map["id"] == "integer"
    assert cast_map["amount"] == "decimal"


def test_harmonize_dates_to_timestamp_and_missing_columns_ignored():
    source = [ColumnMetadata("dt", "date", "date"), ColumnMetadata("only_src", "varchar", "string")]
    target = [ColumnMetadata("dt", "timestamp", "timestamp"), ColumnMetadata("only_tgt", "int", "integer")]
    cast_map = harmonize_common_columns(source, target)
    assert cast_map == {"dt": "timestamp"}
