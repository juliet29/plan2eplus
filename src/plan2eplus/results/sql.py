from pathlib import Path

from ladybug.datacollection import BaseCollection
from ladybug.sql import SQLiteResult

from plan2eplus.ops.output.interfaces import OutputVariables
from plan2eplus.results.collections import QOIResult, SQLCollection


def get_sql_results(path_to_sql: Path):
    assert path_to_sql.exists(), f"Path {path_to_sql} does not exist"
    assert (
        path_to_sql.suffix == ".sql"
    ), f"Path {path_to_sql} has incorrect suffix, expected a '.sql' file"
    return SQLiteResult(str(path_to_sql))


def validate_request(sql: SQLiteResult, var: str):
    assert sql.available_outputs is not None
    try:
        assert var in sql.available_outputs
        return True
    except AssertionError:
        return False


def create_result_for_qoi(sql: SQLiteResult, var: OutputVariables):
    """Returns a collection for each space"""
    if validate_request(sql, var):
        collections: list[BaseCollection] = sql.data_collections_by_output_name(var)
        if collections:
            return QOIResult.from_sql_collections(
                [SQLCollection(i) for i in collections]
            )
        else:
            raise Exception("No collections found!")

    raise Exception(
        f"Invalid variable request: {var} not in {sql.available_outputs} in {sql}"
    )


def get_qoi(qoi: OutputVariables, path_to_outputs: Path):
    sql = get_sql_results(path_to_outputs)
    return create_result_for_qoi(sql, qoi)
