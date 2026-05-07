from etl_validation_tool.comparator import build_sql_preview
from etl_validation_tool.config import TablePair


def test_build_sql_preview_contains_join_and_compare_predicates():
    pair = TablePair(
        source_connection="src",
        source_schema="sales",
        source_table="orders",
        target_connection="tgt",
        target_schema="dw",
        target_table="orders_f",
        join_keys=["order_id"],
        compare_columns=["amount", "status"],
    )
    sql = build_sql_preview(pair, ["amount", "status"])

    assert "FULL OUTER JOIN" in sql
    assert "s.order_id=t.order_id" in sql
    assert "s.amount" in sql and "t.status" in sql
