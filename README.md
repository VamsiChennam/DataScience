# ETL Testing Automation Workbench (PySpark + PyTest + Streamlit)

This project provides a scalable ETL testing automation framework for:

- Structured source-vs-target table validation (same DB + cross DB).
- Auto DDL metadata extraction and datatype harmonization.
- Auto testcase generation and local test-management tracking.
- Unstructured data validation after target table checks.
- Tableau KPI validation after target validation completes.

## Key capabilities

- Reads column metadata from `information_schema.columns` and auto aligns datatypes.
- Uses PySpark reconciliation logic suitable for 10 crore (100M+) tables.
- Supports bulk table selection through UI checkboxes + `Select all`.
- Generates testcase assets and pytest checks automatically.
- Stores testcase and test-run history in SQLite (ALM/TestRail-like local tracking).
- Validates unstructured payloads (`payload_json`, `payload_text`) with normalization checks.
- Validates Tableau KPIs from dashboard CSV export against KPI expectations with tolerance.

## Design references (web tools)

- QuerySurge: https://www.querysurge.com/solutions/etl-testing
- Great Expectations: https://docs.greatexpectations.io/
- OpenMetadata quality tests: https://docs.open-metadata.org/latest/how-to-guides/data-quality-observability/quality

## Project layout

```text
etl_validation_tool/
  cli.py
  comparator.py
  config.py
  management_store.py
  metadata.py
  runner.py
  sample_data.py
  tableau_kpi_validator.py
  testcase_generator.py
  ui_app.py
  unstructured_validator.py
scripts/
  run_10crore_benchmark.py
tests/
  test_comparator_sql.py
  test_metadata.py
  test_tableau_kpi_validator.py
  test_testcase_generator.py
```

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Structured validation CLI

```bash
python -m etl_validation_tool.cli \
  --connections connections.json \
  --table-mapping table_mapping.json \
  --run-id RUN_20260425_001
```

## Unstructured validation CLI

```bash
python -m etl_validation_tool.cli \
  --run-unstructured \
  --unstructured-rows 1000000 \
  --unstructured-partitions 200
```

## Tableau KPI validation CLI

```bash
python -m etl_validation_tool.cli \
  --run-tableau-kpi \
  --tableau-export-csv tableau_export.csv \
  --kpi-expectations kpi_expectations.json
```

Example `kpi_expectations.json`:

```json
[
  {"name": "Revenue", "expected_value": 1000000, "tolerance_pct": 1.0},
  {"name": "Orders", "expected_value": 52000, "tolerance_pct": 2.0}
]
```

## 10-crore sample benchmark harness

```bash
python scripts/run_10crore_benchmark.py --rows 100000000 --partitions 2000
```

> Note: Running full 100M in local laptop/dev containers may require larger cluster resources.

## UI

```bash
streamlit run etl_validation_tool/ui_app.py
```

UI supports:
- Mapping upload.
- Checkbox table selection + Select All.
- Structured testcase generation.
- Test management registration.
- Tableau KPI validation from uploaded files.

## Testing matrix

### Unit tests (automated in this repo)

```bash
pytest -q
```

Covers:
- datatype normalization/harmonization variants,
- SQL preview generation,
- testcase generation,
- KPI validator behavior.

### Performance/scale tests (manual / cluster)

- 1M rows smoke benchmark.
- 10M rows pre-prod benchmark.
- 100M rows (10 crore) full benchmark with cluster sizing.

### Unstructured tests

- exact JSON payload equality,
- case-insensitive text equality,
- required JSON path/key presence.

### Tableau KPI tests

- KPI-level tolerance checks,
- pass/fail status per KPI,
- report artifact generation.
