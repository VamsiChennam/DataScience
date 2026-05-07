import json
from pathlib import Path

from etl_validation_tool.config import TablePair
from etl_validation_tool.testcase_generator import generate_pytest_module, generate_testcase_manifest


def test_generate_manifest_and_pytest_module(tmp_path: Path):
    pair = TablePair(
        source_connection="src",
        source_schema="a",
        source_table="t1",
        target_connection="tgt",
        target_schema="b",
        target_table="t2",
        join_keys=["id"],
        compare_columns=["col1"],
    )
    manifest = generate_testcase_manifest([pair], tmp_path / "manifest.json")
    content = json.loads(manifest.read_text(encoding="utf-8"))
    assert content[0]["test_id"] == "AUTO_TC_0001"

    pytest_file = generate_pytest_module(manifest, tmp_path / "test_generated.py")
    assert "test_generated_cases_have_join_keys" in pytest_file.read_text(encoding="utf-8")
