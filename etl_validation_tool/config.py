from dataclasses import dataclass, field
from typing import List, Optional


@dataclass(slots=True)
class JdbcConfig:
    name: str
    url: str
    user: str
    password: str
    driver: str
    fetchsize: int = 200000


@dataclass(slots=True)
class TablePair:
    source_connection: str
    source_schema: str
    source_table: str
    target_connection: str
    target_schema: str
    target_table: str
    join_keys: List[str]
    compare_columns: Optional[List[str]] = None

    @property
    def source_fqn(self) -> str:
        return f"{self.source_schema}.{self.source_table}"

    @property
    def target_fqn(self) -> str:
        return f"{self.target_schema}.{self.target_table}"


@dataclass(slots=True)
class ValidationRunConfig:
    run_id: str
    table_pairs: List[TablePair] = field(default_factory=list)
    sample_rows_for_debug: int = 50
    repartition_count: int = 512
